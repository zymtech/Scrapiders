# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Field

class JdChinahrItem(scrapy.Item):
    title = Field()
    joblink = Field()
    jobdetail = Field()
    updatetime = Field()
    salary = Field()
    cityandedu = Field()
    company = Field()
    crawltime = Field()
