# -*- coding : uft-8 -*-

import scrapy
import urllib

from jd_51job.items import Jd51JobItem
from scrapy.http import Request
from scrapy.exceptions import IgnoreRequest
import os
import datetime
import re


class Jd51JobSpider(scrapy.Spider):
    name = "jd_51job"
    allowed_domain = ["51job.com"]

    datafile = os.path.join(os.getcwd(),"jobs_51job.txt")
    keywords = ' '.join(open(datafile,'rb').readlines()).split(' ')
    keywordcount = 0
    keyword = keywords[keywordcount]
    keywordcode = urllib.quote(keyword)

    start_url = "http://search.51job.com/jobsearch/search_result.php?"
    urls = []
    for kw in keywords:
        url = start_url + 'keyword=' + urllib.quote(keyword)
        urls.append(url)

    def start_requests(self):
        for url in self.urls:
            yield scrapy.http.Request(url, callback=self.parse0, errback=self.errback)

    def parse0(self, response):
        print response.url
        pagestr = response.xpath('//div[@class="dw_page"]//span[@class="td"]/text()').extract()[0]
        page = re.search("[0-9]+",pagestr).group()  # unicode
        for i in range(1,int(page)+1):
            url = response.url + '&' + 'curr_page=' + str(i)
            yield scrapy.Request(url, callback=self.parse, errback=self.errback)

    def errback(self, response):
        raise IgnoreRequest("ignore this request")

    def parse(self, response):
        try:
            joblink = response.xpath('//div[@id="resultList"]/div[@class="el"]//p//span//a/@href').extract()
            title = response.xpath('//div[@id="resultList"]/div[@class="el"]//p[@class="t1 "]//a/text()').extract()
            company = response.xpath('//div[@id="resultList"]/div[@class="el"]//span[@class="t2"]/a/text()').extract()
            updatetime = response.xpath('//div[@id="resultList"]/div[@class="el"]//span[@class="t5"]/text()').extract()
            salary = response.xpath('//div[@id="resultList"]/div[@class="el"]//span[@class="t4"]/text()').extract()
            city = response.xpath('//div[@id="resultList"]/div[@class="el"]//span[@class="t3"]/text()').extract()
            for i in range(49):
                item = Jd51JobItem()
                item['joblink'] = str(joblink[i])
                item['title'] = title[i]
                item['company'] = company[i]
                item['updatetime'] = datetime.datetime.now().strftime("%Y") + '-' + updatetime[i]
                item['salary'] = salary[i]
                item['city'] = city[i]
                #item['crawltime'] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
                item['crawltime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield Request(item['joblink'], meta={'pitem':item},callback=self.parse_jobdetail)

        except BaseException as e :
            print e

    def parse_jobdetail(self,response):
        item = response.meta['pitem']
        try:
            item['jobdetail'] = '<br>'.join(response.xpath('//div[@class="bmsg job_msg inbox"]/text()').extract()).encode('utf8')
        except BaseException:
            pass
        return item