# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CinemaScraperProjectPipeline:
    def process_item(self, item, spider):
        return item

class CinestarSpiderPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## ids to int
        ids = ['movie_id', 'cinema_id']
        for id in ids:
            value = adapter.get(id)
            adapter[id] = int(value)

        return item


import pymongo
import sys
from .items import CinestarProgramItem, CinemacityProgramItem, AeroProgramItem, CSFDProgramItem, CSFDMovieItem

class MongoDBPipeline:

    #collection = ''

    def __init__(self, settings):
        self.mongodb_uri = settings.get('MONGODB_URI')
        self.mongodb_db = settings.get('MONGODB_DATABASE', 'items')
        self.collection = settings.get('MONGODB_COLLECTION')
        if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    #def __init__(self, mongodb_uri, mongodb_db):
    #    self.mongodb_uri = mongodb_uri
    #    self.mongodb_db = mongodb_db
    #    if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")

    #@classmethod
    #def from_crawler(cls, crawler):
    #    return cls(
    #        mongodb_uri=crawler.settings.get('MONGODB_URI'),
    #        mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
    #    )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if self.collection == 'cinestar_program':
            data = dict(CinestarProgramItem(item))
        elif self.collection == 'cinemacity_program':
            data = dict(CinemacityProgramItem(item))
        elif self.collection == 'aero_program':
            data = dict(AeroProgramItem(item))
        elif self.collection == 'csfd_program':
            data = dict(CSFDProgramItem(item))
        elif self.collection == 'csfd_premiere':
            data = dict(CSFDMovieItem(item))
        self.db[self.collection].insert_one(data)
        return item