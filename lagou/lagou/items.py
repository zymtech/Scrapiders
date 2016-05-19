# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    url = scrapy.Field()
    compabbr = scrapy.Field()
    compbelief = scrapy.Field()
    compintro = scrapy.Field()
    compwebsite = scrapy.Field()
    complogo = scrapy.Field()
    industry = scrapy.Field()
    investinfo = scrapy.Field()
    scale = scrapy.Field()
    city = scrapy.Field()
    tag = scrapy.Field()
    location = scrapy.Field()
    managernames = scrapy.Field()
    managertitles = scrapy.Field()
    managerphotos = scrapy.Field()
    managerintro = scrapy.Field()
    historydateday = scrapy.Field()
    historydateyear = scrapy.Field()
    historyevent = scrapy.Field()
    historyeventlink = scrapy.Field()
    #interate = scrapy.Field()
    inteproc = scrapy.Field()
    inteposition = scrapy.Field()
    intetime = scrapy.Field()
    compphoto = scrapy.Field()
    productname = scrapy.Field()
    productimg = scrapy.Field()
    producttags = scrapy.Field()
    productlinks = scrapy.Field()
    productintro = scrapy.Field()


