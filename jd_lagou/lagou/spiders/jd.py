# -*- coding: utf-8 -*-
import scrapy
import json
from lagou.items import LagouItem
from scrapy.http import Request
from twisted.internet.error import TimeoutError
from scrapy.exceptions import IgnoreRequest
import os
import datetime
import urllib


class LagoupositionSpider(scrapy.Spider):
    name = "jd_lagou"
    totalPageCount = 0
    curpage = 1
    cur = 0
    myurl = 'http://www.lagou.com/jobs/positionAjax.json?'
    file = open(os.path.join(os.getcwd(),"jobs.txt"),'rb')
    kds = ','.join(file.readlines()).split(',')
    kd = kds[0]
    urls = []
    for kd in kds:
        for pn in range(1,301):
            url = myurl + 'kd=' + urllib.quote(kd) + '&' + 'pn=' + str(pn)
            urls.append(url)

    start_urls = urls

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse, errback=self.errback)
            #return [scrapy.http.FormRequest(self.myurl,errback=self.errback,dont_filter=True,meta={'dont_retry':True},
            #                               formdata={'pn':str(self.curpage),'kd':self.kd},callback=self.parse)]

    def errback(self, failure):
        raise IgnoreRequest("ignore this request")

    def parse(self, response):
        try:
            jdict = json.loads(response.body)
            jcontent = jdict["content"]
            jposresult = jcontent["positionResult"]
            jresult = jposresult["result"]
            if jresult:
                self.totalPageCount = jposresult['totalCount'] / 15 + 1
                for each in jresult:
                    item = LagouItem()
                    item['crawltime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    item['city']=each['city']
                    item['companyName'] = each['companyName']
                    item['companySize'] = each['companySize']
                    item['positionName'] = each['positionName']
                    item['positionType'] = each['positionType']
                    item['positionURL'] = "http://www.lagou.com/jobs/"+str(each['positionId'])+'.html'
                    item['updatetime'] = each['createTime'][0:10]
                    sal = each['salary']
                    sal = sal.split('-')
                    #print sal
                    if len(sal) == 1:
                        item['salaryMax'] = int(sal[0][:sal[0].find('k')])
                    else:
                        item['salaryMax'] = int(sal[1][:sal[1].find('k')])
                    item['salaryMin'] = int(sal[0][:sal[0].find('k')])
                    item['positionAdvantage'] = each['positionAdvantage']
                    item['companyLabelList'] = each['companyLabelList']
                    item['keyword'] = self.kd
                    yield Request(item['positionURL'],meta={'pitem':item, 'dont_retry':True},
                                  callback=self.parsedetail,errback=self.errback)
        except BaseException as e :
            print e
    def parsedetail(self,response):
        item = response.meta['pitem']
        item['jobdetail'] = ''.join(response.xpath('//dd[@class="job_bt"]//text()').extract())
        return item
