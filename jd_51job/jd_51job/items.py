# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.item import Field


class Jd51JobItem(scrapy.Item):
    title = Field()
    joblink = Field()
    company = Field()
    updatetime = Field()
    salary = Field()
    city = Field()
    jobdetail = Field()
