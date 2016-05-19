# coding = utf-8

from scrapy.http.request.form import Request
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.crawler import Crawler
from jobtong.items import JobtongItem


class CompInfo(Spider):
    name = "jobtong"
    allowed_domains = ["jobtong.com"]

    def start_requests(self):
        for i in range(1, 37927):  # 37926
            url = "http://www.jobtong.com/e/"+ str(i)
            yield Request(url,
                          meta={
                              'dont_retry': True
                          },
                          callback=self.parse)

    def parse(self, response):
        selector = Selector(response)
        item = JobtongItem()
        item['url'] = response.url
        item['complogo'] = selector.xpath('//img[@class="img-circle"]/@src').extract()
        item['compabbr'] = selector.xpath('//div[@class="header"]/h1/text()').extract()
        item['compintro'] = selector.xpath('//div[@class="box introduce"]/div/text()').extract()
        item['slogon'] = selector.xpath('//div[@class="header"]/h3/text()').extract()
        item['city'] = selector.xpath('//div[@class="tags"]/span/text()').extract()[0]
        item['scale'] = selector.xpath('//div[@class="tags"]/span/text()').extract()[1]
        item['comptype'] = selector.xpath('//div[@class="tags"]/span/text()').extract()[2]
        item['industry'] = selector.xpath('//div[@class="tags"]/span/text()').extract()[3]
        item['compfullname'] = selector.xpath('//div[@class="sidebar"]//p/text()').extract()[0]
        item['compwebsite'] = selector.xpath('//div[@class="sidebar"]//a/text()').extract()
        item['location'] = selector.xpath('//div[@class="sidebar"]//p/text()').extract()[1]
        return item