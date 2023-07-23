# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CinemaScraperProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MovieCinestar(scrapy.Item):
    movie_id = scrapy.Field()
    movie_title = scrapy.Field()
    movie_premiere = scrapy.Field()
    movie_url = scrapy.Field()
    movie_img = scrapy.Field()
    cinema_id = scrapy.Field()
    cinema_name2 = scrapy.Field()
    cinema_url = scrapy.Field()
