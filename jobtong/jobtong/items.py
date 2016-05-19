# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobtongItem(scrapy.Item):
    url = scrapy.Field()
    complogo = scrapy.Field()
    compabbr = scrapy.Field()
    compintro = scrapy.Field()
    slogon = scrapy.Field()
    city = scrapy.Field()
    scale = scrapy.Field()
    comptype = scrapy.Field()
    industry = scrapy.Field()
    compfullname = scrapy.Field()
    compwebsite = scrapy.Field()
    location = scrapy.Field()
