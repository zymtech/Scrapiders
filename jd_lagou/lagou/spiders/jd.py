# -*- coding: utf-8 -*-
import scrapy
import json
from lagou.items import LagouItem
from scrapy.http import Request
import os


class LagoupositionSpider(scrapy.Spider):
    name = "jd_lagou"
    totalPageCount = 0
    curpage = 1
    cur = 0
    myurl = 'http://www.lagou.com/jobs/positionAjax.json?'
    file = open(os.path.join(os.getcwd(),"jobs.txt"),'rb')
    kds = ','.join(file.readlines()).split(',')
    kd = kds[0]
    def start_requests(self):
        return [scrapy.http.FormRequest(self.myurl,
                                       formdata={'pn':str(self.curpage),'kd':self.kd},callback=self.parse)]

    def parse(self, response):
        item = LagouItem()
        jdict = json.loads(response.body)
        jcontent = jdict["content"]
        jposresult = jcontent["positionResult"]
        jresult = jposresult["result"]
        self.totalPageCount = jposresult['totalCount'] / jposresult['pageSize'] + 1
        for each in jresult:
            item['city']=each['city']
            item['companyName'] = each['companyName']
            item['companySize'] = each['companySize']
            item['positionName'] = each['positionName']
            item['positionType'] = each['positionType']
            item['positionURL'] = "http://www.lagou.com/jobs/"+str(each['positionId'])+'.html'
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
            yield Request(item['positionURL'],meta={'pitem':item}, callback=self.parsedetail)
        if self.curpage <= self.totalPageCount:
            self.curpage += 1
            yield scrapy.http.FormRequest(self.myurl,
                                        formdata = {'pn': str(self.curpage), 'kd': self.kd},callback=self.parse)
        elif self.cur < len(self.kds)-1:
            self.curpage = 1
            self.totalPageCount = 0
            self.cur += 1
            self.kd = self.kds[self.cur]
            yield scrapy.http.FormRequest(self.myurl,
                                        formdata = {'pn': str(self.curpage), 'kd': self.kd},callback=self.parse)

    def parsedetail(self,response):
        item = response.meta['pitem']
        item['jobdetail'] = ''.join(response.xpath('//dd[@class="job_bt"]//text()').extract())
        return item
