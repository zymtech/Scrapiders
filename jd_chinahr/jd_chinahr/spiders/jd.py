# -*- coding: UTF-8 -*-

import scrapy
import os
import datetime

from jd_chinahr.items import JdChinahrItem
from scrapy.http import Request

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class JdChinahrSpider(scrapy.Spider):
    name = "jd_chinahr"
    allowed_domain = ["chinahr.com"]

    datafile = open(os.path.join(os.getcwd(), "href.txt"),'rb')
    urls = ''.join(datafile.readlines()).split(' ')
    urlcount = 0
    url = urls[urlcount]

    def start_requests(self):
        return [Request(self.url, callback=self.parse)]

    def parse(self, response):
        item = JdChinahrItem()
        try:
            for i in range(19):
                item['title'] = response.xpath('//div[@class="jobList"]//span[@class="e1"]//a[@class="ur"]//text()').extract()[i]
                item['joblink'] = response.xpath('//div[@class="jobList"]//span[@class="e1"]//a/@href').extract()[i]
                item['updatetime'] = response.xpath('//div[@class="jobList"]//li[@class="l1"]//span[@class="e2"]/text()').extract()[i]
                item['salary'] = response.xpath('//div[@class="jobList"]//li[@class="l2"]//span[@class="e2"]/text()').extract()[i]
                item['cityandedu'] = response.xpath('//div[@class="jobList"]//li[@class="l2"]//span[@class="e1"]/text()').extract()[i]
                item['company'] = response.xpath('//div[@class="jobList"]//li[@class="l1"]//span[@class="e3 cutWord"]/a/text()').extract()[i]
                if item['updatetime'] == u'今天':
                    item['updatetime'] = datetime.date.today().strftime("%Y/%m/%d")
                elif item['updatetime'] == u'昨天':
                    item['updatetime'] = (datetime.date.today()-datetime.timedelta(days=1)).strftime("%Y/%m/%d")
                yield Request(item['joblink'], meta={'pitem':item},callback=self.parse_jobdetail)
        except IndexError:
            pass

        next_page = response.xpath('//div[@class="pageList"]/a[last()]/@href')

        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)
        else:
            self.urlcount += 1
            url = self.urls[self.urlcount]
            yield scrapy.Request(url, self.parse)

    def parse_jobdetail(self,response):
        item = response.meta['pitem']
        item['jobdetail'] = '<br>'.join(response.xpath(('//div[@class="job_intro_info"]/text()')).extract()).encode('utf-8')
        return item

