# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CinemaScraperProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CinCinestar(scrapy.Item):
    cinema_name = scrapy.Field()
    cinema_url = scrapy.Field()

class CinMovCinestar(scrapy.Item):
    movie_id = scrapy.Field()
    movie_title = scrapy.Field()
    movie_premiere = scrapy.Field()
    movie_url = scrapy.Field()
    movie_img = scrapy.Field()
    cinema_id = scrapy.Field()
    cinema_name2 = scrapy.Field()
    cinema_url = scrapy.Field()


class CinMovDayCinestar(scrapy.Item):
    movie_id = scrapy.Field()
    cinema_id = scrapy.Field()
    date_id = scrapy.Field()
    date = scrapy.Field()
    version = scrapy.Field()
    dab_tit = scrapy.Field()
    cinema_hall = scrapy.Field()
    time_start = scrapy.Field()
    time_end = scrapy.Field()
    time_url = scrapy.Field()

class CinestarProgramItem(scrapy.Item):
    cinema_id = scrapy.Field()
    cinema_name3 = scrapy.Field()
    date_id = scrapy.Field()
    date = scrapy.Field()
    movie_title = scrapy.Field()
    movie_title_long = scrapy.Field()
    movie_url = scrapy.Field()
    movie_img = scrapy.Field()
    dab_tit = scrapy.Field()
    rating = scrapy.Field()
    rating_detail = scrapy.Field()
    uhd = scrapy.Field()
    premiere = scrapy.Field()
    new = scrapy.Field()
    projected = scrapy.Field()
    cinema_hall = scrapy.Field()
    time_start = scrapy.Field()
    time_end = scrapy.Field()
    time_url = scrapy.Field()
    length = scrapy.Field()