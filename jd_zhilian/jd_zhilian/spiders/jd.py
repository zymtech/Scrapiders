# -*- coding = utf-8 -*-

from scrapy import Spider
from scrapy.http import Request
import datetime
import urllib
import os
from scrapy.exceptions import IgnoreRequest
from jd_zhilian.items import JdZhilianItem


class jd(Spider):
    name = "jd_zhilian"
    allowed_domain = ["zhaopin.com"]
    #start_urls = ["http://sou.zhaopin.com/jobs/searchresult.ashx?p=1"]

    datafile = os.path.join(os.getcwd(),"jobs.txt")
    jobkws = ' '.join(open(datafile,'rb').readlines()).split(' ')

    baseurl = "http://sou.zhaopin.com/jobs/searchresult.ashx?"
    urls = []
    for kw in jobkws:
        url = baseurl + 'kw=' + urllib.quote(kw)
        urls.append(url)

    def start_requests(self):
        for url in self.urls:
            yield Request(url , callback=self.parse0, errback=self.errback)

    def errback(self, failure):
        raise IgnoreRequest("ignore this request")

    def parse0(self, response):
        #pagestr = response.xpath
        #page = re.search
        #for i in range(1, str(page)+1):
        for i in range(1, 301):
            url = response.url + '&' + 'p=' + str(i)
            yield Request(url, callback=self.parse, errback=self.errback)

    def parse(self, response):
        url_data = response.xpath('//div[@id="newlist_list_content_table"]//td[@class="zwmc"]//a/@href').extract()
        for company_url in url_data:
            yield Request(company_url,callback=self.parse2, errback=self.errback)

    def parse2(self, response):

        item = JdZhilianItem()
        item['joblink'] = response.url
        item['companyname'] = response.xpath('//div[@class="inner-left fl"]/h2/a/text()').extract()[0]
        item['salary'] = response.xpath('//ul[@class="terminal-ul clearfix"]//strong/text()').extract()[0]
        item['workplace'] = response.xpath('//ul[@class="terminal-ul clearfix"]//strong/a/text()').extract()[0] +\
                    response.xpath('//ul[@class="terminal-ul clearfix"]//strong/text()').extract()[1]
        item['updatetime'] =  response.xpath('//span[@id="span4freshdate"]/text()').extract()[0]
        #item['jobtype'] = response.xpath('//ul[@class="terminal-ul clearfix"]//strong/text()').extract()[2]
        item['workexperience'] = response.xpath('//ul[@class="terminal-ul clearfix"]//strong/text()').extract()[3]
        item['education'] = response.xpath('//ul[@class="terminal-ul clearfix"]//strong/text()').extract()[4]
        item['jobcategory'] = response.xpath('//ul[@class="terminal-ul clearfix"]//strong/a/text()').extract()[-1]
        item['crawltime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # job requirement
    #    require_data = response.xpath(
    #        '//body/div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[1]/p//text()').extract()
    #    item['jobdetails'] = ''
    #    for i in require_data:
    #        i_middle = re.sub(r'<.*?>', r'', i, re.S)
    #        item['jobdetails'] += re.sub(r'\s*', r'', i_middle, re.S)
        item['jobdetails'] = '<br>'.join(response.xpath('//div[@class="tab-inner-cont"]//p/text()').extract())

    # company address
        company_sel = response.xpath(
            '//body/div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[last()]//text()').extract()
        item['companyinfo'] = ''
        for sel in company_sel:
            item['companyinfo'] += sel
        #company_data = re.search(r'<h2>\s*(.*?)\s*<a', company_data[0], re.S).group(1)

        return item


