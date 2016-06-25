# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    companyname = scrapy.Field()
    joblink = scrapy.Field()
    salary = scrapy.Field()
    workplace = scrapy.Field()
    updatetime = scrapy.Field()
    jobtype = scrapy.Field()
    workexperience = scrapy.Field()
    education = scrapy.Field()
    recrunumbers = scrapy.Field()
    jobcategory = scrapy.Field()
    jobdetails = scrapy.Field()
    crawltime = scrapy.Field()
    companyinfo = scrapy.Field()
