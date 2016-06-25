# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings


class JdChinahrPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_NAME']
        clint = pymongo.MongoClient(host, port)
        tdb = clint[dbname]
        self.post = tdb[settings['MONGODB_TABLE']]

    def process_item(self, item, spider):
        bookinfo = dict(item)
        self.post.update(
            {"joblink": bookinfo['joblink']},
            {"$set":{
                "title" : bookinfo['title'],
                "jobdetail" : bookinfo['jobdetail'],
                "salary" : bookinfo['salary'],
                "cityandedu" : bookinfo['cityandedu'],
                "company" : bookinfo['company'],
                "crawltime" : bookinfo['crawltime'],
                "updatetime" : bookinfo['updatetime']}
            },
            upsert=True
        )
        return item
