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