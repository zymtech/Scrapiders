# coding = utf-8

from scrapy.http.request.form import Request
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.crawler import Crawler
from lagou.items import LagouItem


class CompInfo(Spider):
    name = "lagou"
    allowed_domains = ["lagou.com"]
    # start_urls = ["http://www.lagou.com/gongsi/101548.html"]

    def start_requests(self):
        for i in range(1, 119390):  # 119389
            url = "http://www.lagou.com/gongsi/"+ str(i) + '.html'
            yield Request(url,
                          meta={
                              'dont_redirect': True
                          },
                          callback=self.parse)

    def parse(self, response):
        selector = Selector(response)
        item = LagouItem()
        item['url'] = response.url
        item['compabbr'] = selector.xpath('//div[@class="company_main"]//h1//a/text()').extract()
        item['compbelief'] = selector.xpath('//div[@class="company_word"]/text()').extract()
        item['compintro'] = selector.xpath('//span[@class="company_content"]//p/text()').extract()
        item['compwebsite'] = selector.xpath('//div[@class="company_main"]//h1//a/@href').extract()
        item['complogo'] = selector.xpath('//div[@class="top_info_wrap"]//img/@src').extract()
        item['industry'] = selector.xpath('//div[@class="item_container"]//div[@class="item_content"]//ul//li//span/text()').extract()[-4]
        item['investinfo'] = selector.xpath('//div[@class="item_container"]//div[@class="item_content"]//ul//li//span/text()').extract()[-3]
        item['scale'] = selector.xpath('//div[@class="item_container"]//div[@class="item_content"]//ul//li//span/text()').extract()[-2]
        item['city'] = selector.xpath('//div[@class="item_container"]//div[@class="item_content"]//ul//li//span/text()').extract()[-1]
        item['managernames'] = selector.xpath('//ul[@class="manager_list"]//p[@class="item_manager_name"]/span/text()').extract()
        item['managertitles'] = selector.xpath('//ul[@class="manager_list"]//p[@class="item_manager_title"]/text()').extract()
        item['managerphotos'] = selector.xpath('//ul[@class="manager_list"]//img[@class="item_manger_photo_show"]/@src').extract()
        item['managerintro'] = selector.xpath('//div[@class="item_manager_content"]//p/text()').extract()
        item['tag'] = selector.xpath('//li[@class="con_ul_li"]/text()').extract()
        item['historydateday'] = selector.xpath('//p[@class="date_day"]/text()').extract()
        item['historydateyear'] = selector.xpath('//p[@class="date_year"]/text()').extract()
        item['historyevent'] = selector.xpath('//p[@class="desc_title desc_hover clearfix"]//a/text()').extract()
        item['historyeventlink'] = selector.xpath('//p[@class="desc_title desc_hover clearfix"]//a/@href').extract()[::2]
        item['location'] = selector.xpath('//span[@class="li_title_text ellipsis"]/text()').extract()[0]
        #item['interate'] = selector.xpath
        item['inteproc'] = selector.xpath('//div[@class="interview-process"]/text()').extract()
        item['inteposition'] = selector.xpath('//a[@class="job-name"]/text()').extract()
        item['intetime'] = selector.xpath('//span[@class="review-date"]/text()').extract()
        item['compphoto'] = ["""http://www.lagou.com/""" + i.extract() for i in selector.xpath('//ul[@class="company_img"]//li/@data-item')]
        item['productname'] = selector.xpath('//div[@id="company_products"]//div[@class="product_details"]//a/text()').extract()[::3]
        item['producttags'] = '@'
        for i in selector.xpath('//div[@class="item_content"]//ul[@class="clearfix"]'):
            item['producttags'] = item['producttags'] + ','.join(i.xpath('./li/text()').extract()) + '@'
        item['productlinks'] = selector.xpath('//div[@id="company_products"]//div[@class="product_details"]//a/@href').extract()[::2]
        item['productimg'] = selector.xpath('//div[@id="company_products"]//div[@class="item_content"]//img/@src').extract()
        item['productintro'] = selector.xpath('//div[@id="company_products"]//div[@class="product_profile"]/text()').extract()

        return item
