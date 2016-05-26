# -*- coding = utf-8 -*-

import pymongo
from scrapy import Spider
from scrapy.http import Request
import re


class jd(Spider):
    name = "jd_zhilian"
    allowed_domain = ["zhaopin.com"]
    start_urls = ["http://sou.zhaopin.com/jobs/searchresult.ashx?p=1"]

    def parse(self, response):
        url_data = response.xpath('//div[@id="newlist_list_content_table"]//td[@class="zwmc"]//a/@href').extract()
        for company_url in url_data:
            yield Request(company_url,callback=self.parse2)

        next_page_url = response.xpath('//body/div[@class="main"]/div[@class="search_newlist_main"]/div[@class="newlist_main"]/form[@name="frmMain"]/div[@class="clearfix"]/div[@class="newlist_wrap fl"]/div[@class="pagesDown"]/ul/li[@class="pagesDown-pos"]/a/@href').extract()
        if next_page_url:
            yield Request(next_page_url[0],callback=self.parse)
        else:
            pass

    def parse2(self, response):
        # job treatment
        try:
            pay_data = response.xpath(
                '//body/div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li//text()').extract()
            salary = pay_data[1]
            workplace = pay_data[3]
            pubdate = pay_data[5]
            jobtype = pay_data[7]
            workexperience = pay_data[9]
            education = pay_data[11]
            recrunumbers = pay_data[13]
            jobcategory = pay_data[15]
        except:
            pass
        # job requirement
        try:
            require_data = response.xpath(
                '//body/div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[1]/p//text()').extract()
            require_data_middle = ''
            for i in require_data:
                i_middle = re.sub(r'<.*?>', r'', i, re.S)
                require_data_middle = require_data_middle + re.sub(r'\s*', r'', i_middle, re.S)
        except:
            pass
        # company address
        try:
            company_sel = response.xpath(
                '//body/div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[last()]//text()').extract()
            company_data = ''
            for sel in company_sel:
                company_data += sel
            #company_data = re.search(r'<h2>\s*(.*?)\s*<a', company_data[0], re.S).group(1)
        except:
            pass
        # information url
        company_url = str(response)[5:-1]

        conn = pymongo.MongoClient('127.0.0.1',27017)
        db = conn.zhaopin
        employee = db.jd
        employee.insert({"url":company_url, "salary": salary,
                         "workpalce":workplace, "pubdate":pubdate, "jobtype": jobtype,
                         "workexperience": workexperience, "education": education,
                         "recrunumbers": recrunumbers, "jobcategory": jobcategory,
                         "jobdetails":require_data_middle,"company_info":company_data})




