# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):
    url = scrapy.Field()   # url of company info, http://www.itjuzi.com/company/12121
    compabbr = scrapy.Field()  # abbreviation of company name
    compfull = scrapy.Field()  # company fullname
    complogosrc = scrapy.Field()  # company logo
    comptag = scrapy.Field()   # tag
    industry = scrapy.Field()  # industry that the company belong to, list format
    city = scrapy.Field()      # city, list format
    compwebsite = scrapy.Field()  # url of company 's website
    compintro = scrapy.Field()  # introduction of the company
    foundtime = scrapy.Field()  # founded time
    location = scrapy.Field()   # location from contact information on sidebar
    opestatus = scrapy.Field()  # operational status
    milestoneevent = scrapy.Field()  # milestone, event and time store separately
    milestonetime = scrapy.Field()  # milestone
    usercomment = scrapy.Field()  # comment from user
    investment = scrapy.Field()
    teamicon = scrapy.Field()    # photo of main members in the team,list
    teamtitle = scrapy.Field()   # title of the member,list
    teamname = scrapy.Field()    # name,list
    teamintro = scrapy.Field()  #  introduction of members,list
