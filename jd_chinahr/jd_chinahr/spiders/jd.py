# -*- coding: UTF-8 -*-

import scrapy
import os
import datetime

from jd_chinahr.items import JdChinahrItem
from scrapy.http import Request
from scrapy.exceptions import IgnoreRequest

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class JdChinahrSpider(scrapy.Spider):
    name = "jd_chinahr"
    allowed_domain = ["chinahr.com"]

    datafile = open(os.path.join(os.getcwd(), "href.txt"),'rb')
    joburls = ''.join(datafile.readlines()).split(' ')
    urlcount = 0
    urls = []
    for joburl in joburls:
        for page in range(1, 176):
            url = joburl + str(page)
            urls.append(url)

    def start_requests(self):
        for url in self.urls:
            yield Request(url, callback=self.parse, errback=self.errback)

    def errback(self, failure):
        raise IgnoreRequest("ignore this request")

    def parse(self, response):
        try:
            for i in range(19):
                item = JdChinahrItem()
                item['title'] = response.xpath('//div[@class="jobList"]//span[@class="e1"]//a[@class="ur"]//text()').extract()[i]
                item['joblink'] = response.xpath('//div[@class="jobList"]//span[@class="e1"]//a/@href').extract()[i]
                item['updatetime'] = response.xpath('//div[@class="jobList"]//li[@class="l1"]//span[@class="e2"]/text()').extract()[i]
                item['salary'] = response.xpath('//div[@class="jobList"]//li[@class="l2"]//span[@class="e2"]/text()').extract()[i]
                item['cityandedu'] = response.xpath('//div[@class="jobList"]//li[@class="l2"]//span[@class="e1"]/text()').extract()[i]
                item['company'] = response.xpath('//div[@class="jobList"]//li[@class="l1"]//span[@class="e3 cutWord"]/a/text()').extract()[i]
                item['crawltime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if item['updatetime'] == u'今天':
                    item['updatetime'] = datetime.date.today().strftime("%Y-%m-%d")
                elif item['updatetime'] == u'昨天':
                    item['updatetime'] = (datetime.date.today()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                else:
                    item['updatetime'] = datetime.datetime.now().strftime("%Y") + '-' + item['updatetime']
                yield Request(item['joblink'], meta={'pitem':item},callback=self.parse_jobdetail, errback=self.errback)

        except BaseException as e:
            print e

    def parse_jobdetail(self,response):
        item = response.meta['pitem']
        try:
            item['jobdetail'] = '<br>'.join(response.xpath(('//div[@class="job_intro_info"]/text()')).extract()).encode('utf-8')
        except BaseException:
            pass
        return item

