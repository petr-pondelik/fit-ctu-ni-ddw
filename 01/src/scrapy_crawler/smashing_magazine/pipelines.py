import json
from typing import List, Set, Dict

import pymongo
from pymongo.cursor import Cursor
from pymongo.database import Database


class MongoPipeline(object):

    collection_name = 'smashingmagazinearticles'

    mongo_uri: str
    mongo_db: str
    client: pymongo.MongoClient
    db: Database

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        # initializing spider
        # opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[self.collection_name].drop()
        self.db['tags'].drop()

    def close_spider(self, spider):
        # clean up when spider is closed
        articles: Cursor = self.db[self.collection_name].find()
        tagsStats: Dict[str, float] = {}
        articlesCnt = 0

        for article in articles:
            tags: List[str] = article["tags"]
            for tag in tags:
                tagParsed = tag.strip().lower()
                try:
                    tagsStats[tagParsed] += 1
                except KeyError:
                    tagsStats[tagParsed] = 1
            articlesCnt += 1

        for key, val in tagsStats.items():
            tagsStats[key] = (val/articlesCnt) * 100

        for key, val in tagsStats.items():
            self.db['tags'].insert({
                'label': key,
                'y': val
            })

        self.client.close()

    def process_item(self, item, spider):
        # how to handle each post
        self.db[self.collection_name].insert(dict(item))
        return item
