# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class MongoPipeline(object):

    collection_name = 'itjuzi'

    def __init__(self,mongo_uri,mongo_port,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_port=crawler.settings.get("MONGO_PORT"),
            mongo_db=crawler.settings.get("MONGO_DATABASE")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri,self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        exist = self.db[self.collection_name].find_one({'url':item['url']})
        if not exist:
            self.db[self.collection_name].insert(dict(item))
        else:
            exist.pop('_id')
            for key in exist:
                if exist[key] == item[key]:
                    pass
                else:
                    self.db[self.collection_name].update({'url':item['url']},{'$set':{key:item[key]}})
                    print "信息变动的公司", item['compabbr']
                    print "url", item['url']
                    print "变动的位置", key
                    print "原内容", exist[key]
                    print "更新后", item[key]
        return item
