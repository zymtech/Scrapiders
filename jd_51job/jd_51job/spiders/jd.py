# -*- coding : uft-8 -*-

import scrapy
import urllib

from jd_51job.items import Jd51JobItem
from scrapy.http import Request
import os

website_possible_httpstatus_list = [407,403]

class Jd51JobSpider(scrapy.Spider):
    name = "jd_51job"
    allowed_domain = ["51job.com"]

    datafile = os.path.join(os.getcwd(),"jobs_51job.txt")
    keywords = ' '.join(open(datafile,'rb').readlines()).split(' ')
    keywordcount = 0
    keyword = keywords[keywordcount]
    keywordcode = urllib.quote(keyword)

    start_url = "http://search.51job.com/jobsearch/search_result.php?"

    def banned(self, response):
        if response.status in website_possible_httpstatus_list:
            return True
        else:
            return False

    def start_requests(self):
        return [scrapy.http.Request(self.start_url + 'keyword='+self.keywordcode, callback=self.parse)]

    def parse(self, response):

        if self.banned(response):
            yield scrapy.Request(
                url=response.url,
                meta={"change_proxy":True},
                callback=self.parse
            )

        item = Jd51JobItem()
        try:
            for i in range(49):
                item['joblink'] = response.xpath('//div[@id="resultList"]/div[@class="el"]//p//span//a/@href').extract()[i]
                item['title'] = response.xpath('//div[@id="resultList"]/div[@class="el"]//p[@class="t1 "]//a/text()').extract()[i]
                item['company'] = response.xpath('//div[@id="resultList"]/div[@class="el"]//span[@class="t2"]/a/text()').extract()[i]
                item['updatetime'] = response.xpath('//div[@id="resultList"]/div[@class="el"]//span[@class="t5"]/text()').extract()[i]
                item['salary'] = response.xpath('//div[@id="resultList"]/div[@class="el"]//span[@class="t4"]/text()').extract()[i]
                item['city'] = response.xpath('//div[@id="resultList"]/div[@class="el"]//span[@class="t3"]/text()').extract()[i]
                yield Request(item['joblink'], meta={'pitem':item},callback=self.parse_jobdetail)
        except IndexError:
            pass

        next_page = response.xpath('//table[@class="searchPageNav"]/tr/td[last()]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)
        else:
            self.keywordcount += 1
            if self.keywordcount < len(self.keywords):
                self.keyword = self.keywords[self.keywordcount]
                url = self.start_url + "keyword="+ urllib.quote(self.keyword)
                yield scrapy.Request(url, self.parse)

    def parse_jobdetail(self,response):
        item = response.meta['pitem']
        item['jobdetail'] = '<br>'.join(response.xpath('//div[@class="bmsg job_msg inbox"]/text()').extract()).encode('utf8')
        return item