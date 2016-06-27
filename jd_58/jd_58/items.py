# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Jd58Item(scrapy.Item):
    title = scrapy.Field()
    joblink = scrapy.Field()
    jobdetail = scrapy.Field()
    crawltime = scrapy.Field()
    salary = scrapy.Field()
    company = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    companyintro = scrapy.Field()
    updatetime = scrapy.Field()
