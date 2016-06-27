# -*- coding: utf-8 -*-

import scrapy
import os
import datetime

from jd_58.items import Jd58Item
from scrapy.http import Request
from scrapy.exceptions import IgnoreRequest


class Jd58Spider(scrapy.Spider):
    name = 'jd_58'
    allowed_domain = ['58.com']

    datefile = open(os.path.join(os.getcwd(), "58_jobs.txt"), 'rb')
    jobnames = ''.join(datefile.readlines()).split(' ')
    citycode = ['bj', 'sh', 'gz', 'sz', 'tj', 'wh', 'hz', 'nj', 'cq', 'cs']
    urls = []
    urlcount = 0
    for city in citycode:
        for job in jobnames:
            for i in range(1, 71):
                url = 'http://' + city + '.58.com/' + job + '/pn' + str(i)
                urls.append(url)

    start_urls = urls

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse, errback=self.errback)

    def errback(self, exceptions):
        raise IgnoreRequest("ignore this request")

    def parse(self, response):
        try:
            for i in range(66):
                item = Jd58Item()
                item['title'] = response.xpath('//div[@class="infolist"]//dt/a/text()').extract()[i]
                item['joblink'] = response.xpath('//div[@class="infolist"]//dt/a/@href').extract()[i]
                item['crawltime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield Request(item['joblink'], meta={'pitem': item}, callback=self.parse_detail)
        except BaseException as e :
            print e
        #if self.urlcount < len(self.urls):
        #    yield Request(self.url[self.urlcount], callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['pitem']
        try:
            item['company'] = ""
            item['salary'] = ''
            item['updatetime'] = ''
            item['jobdetail'] = ''.join(response.xpath('//div[@class="posMsg borb"]//text()').extract())
            item['salary'] = response.xpath('//div[@class="posinfo"]//span[@class="salaNum"]/strong/text()').extract()[0]
            item['company'] = response.xpath('//a[@class="companyName"]/text()').extract()[0]
            item['experience'] = response.xpath('//div[@class="fl"]/text()').extract()[3]
            item['education'] = response.xpath('//div[@class="posinfo"]//div[@class="fl"]/text()').extract()[1]
            item['companyintro'] = ''.join(response.xpath('//div[@class="compIntro"]//p/text()').extract())
            item['updatetime'] = response.xpath('//div[@class="headCon"]//strong[@class="f12"]/text()').extract()[0]
            if item['updatetime'] == u'今天':
                item['updatetime'] = datetime.datetime.now().strftime("%Y-%m-%d")
            else:
                item['updatetime'] = datetime.datetime.now().strftime("%Y") + '-' + item['updatetime']
        except BaseException:
            pass
        return item


