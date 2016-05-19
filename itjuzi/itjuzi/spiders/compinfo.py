# coding = utf-8

from scrapy.http.request.form import Request
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.crawler import Crawler
from itjuzi.items import ItjuziItem


class CompInfo(Spider):
    name = "itjuzi"
    allowed_domains = ["itjuzi.com"]
    # start_urls = ["https://www.itjuzi.com/company/1"]

    def start_requests(self):
        for i in range(1,28589): #28598
            url = "https://www.itjuzi.com/company/"+str(i)
            yield Request(url,
                          callback=self.parse)

    def parse(self, response):
        selector = Selector(response)
        item = ItjuziItem()
        item['url'] = response.url
        item['compabbr'] = selector.xpath('//div[@class="rowhead"]//span[@class="title"]/b/text()').extract_first().strip()
        item['complogosrc'] = selector.xpath('//div[@class="rowhead"]/div[@class="pic"]/img').extract()[0][10:][:-2]
        item['industry'] = selector.xpath('//div[@class="info-line"]/span[@class="scope c-gray-aset"]/a/text()').extract()
        item['city'] = selector.xpath('//div[@class="info-line"]/span[@class="loca c-gray-aset"]/a/text()').extract()
        item['location'] = selector.xpath('//div/ul[@class="list-block aboutus"]/li/span/text()').extract()[2]
        item['compwebsite'] = selector.xpath('//div[@class="link-line"]/a[@href]/text()').extract()
        item['comptag'] = selector.xpath('//div[@class="tagset dbi c-gray-aset"]/a/span/text()').extract()
        item['compintro'] = selector.xpath('//div[@class="des"]/text()').extract()
        item['compfull'] = selector.xpath('//div[@class="des-more"]/div/span/text()')[0].extract()
        item['foundtime'] = selector.xpath('//div[@class="des-more"]/div/span/text()')[1].extract()
        item['opestatus'] = selector.xpath('//div[@class="des-more"]/div/span/text()')[2].extract()
        item['teamname'] = selector.xpath('//ul[@class="list-prodcase limited-itemnum"]/li//a[@class="title"]/b/span/text()').extract()[::2]
        item['teamtitle'] = selector.xpath('//ul[@class="list-prodcase limited-itemnum"]/li//a[@class="title"]/b/span/text()').extract()[1::2]
        item['teamicon'] = selector.xpath('//ul[@class="list-prodcase limited-itemnum"]//span[@class="usericon"]').extract() # need re process
        item['teamintro']  = selector.xpath('//ul[@class="list-prodcase limited-itemnum"]/li//p/text()').extract()
        item['usercomment'] = selector.xpath('//div[@class="commit"]/div[@class="right"]/p/text()').extract()[0::4]
        item['milestoneevent'] = selector.xpath('//ul[@class="list-milestone timelined limited-itemnum"]/li/p/text()').extract()
        item['milestonetime'] = selector.xpath('//ul[@class="list-milestone timelined limited-itemnum"]/li/p/span/text()').extract()
        item['investment'] = "@"
        for i,j in enumerate(response.xpath('//table[@class="list-round-v2"]//tr')):
            item['investment'] = item['investment'] + ''.join(j.xpath('.//span[@class="date c-gray"]/text()').extract()) + '|' +\
                                 ''.join(j.xpath('.//span[@class="round"]/a/text()').extract()) + '|' + \
                                 ''.join(j.xpath('.//span[@class="finades"]//a/text()').extract()) + '|' +\
                                 '+'.join(j.xpath('./td[4]/a/text()').extract()) + '@'
        #item['invesround'] = selector.xpath('//table[@class="list-round-v2"]//span[@class="round"]/a/text()').extract()
        #item['investime'] = selector.xpath('//table[@class="list-round-v2"]//span[@class="date c-gray"]/text()').extract()
        #item['invesamount'] = selector.xpath('//table[@class="list-round-v2"]//span[@class="finades"]//a/text()').extract()
        #item['investor'] = selector.xpath('//table[@class="list-round-v2"]//tr//td[4]//a/text()').extract()

        return item

