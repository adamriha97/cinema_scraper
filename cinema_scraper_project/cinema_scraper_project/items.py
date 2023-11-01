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

class CinemacityProgramItem(scrapy.Item):
    event_id = scrapy.Field()
    cinema_id = scrapy.Field()
    cinema_name3 = scrapy.Field()
    date_id = scrapy.Field()
    date = scrapy.Field()
    movie_id = scrapy.Field()
    movie_title = scrapy.Field()
    movie_url = scrapy.Field()
    movie_img = scrapy.Field()
    movie_vid = scrapy.Field()
    movie_release_year = scrapy.Field()
    dab_tit = scrapy.Field()
    cinema_hall = scrapy.Field()
    cinema_hall_long = scrapy.Field()
    time_start = scrapy.Field()
    time_url = scrapy.Field()
    length = scrapy.Field()
    sold_out = scrapy.Field()
    movie_attrs = scrapy.Field()
    event_attrs = scrapy.Field()

class AeroProgramItem(scrapy.Item):
    event_id = scrapy.Field()
    event_url = scrapy.Field()
    cinema_name3 = scrapy.Field()
    date_orig = scrapy.Field() #* je potreba upravit format
    movie_title = scrapy.Field()
    movie_img = scrapy.Field()
    movie_imgs = scrapy.Field()
    movie_vid = scrapy.Field()
    dab_tit = scrapy.Field()
    cinema_hall = scrapy.Field()
    time_start = scrapy.Field()
    length = scrapy.Field()
    price = scrapy.Field()
    calendar_url = scrapy.Field()
    movie_attrs = scrapy.Field()
    movie_info = scrapy.Field()
    movie_score_urls = scrapy.Field()

class AeroProgramItemSimple(scrapy.Item):
    event_id = scrapy.Field()
    event_url = scrapy.Field()
    cinema_name3 = scrapy.Field()
    date_orig = scrapy.Field() #* je potreba upravit format
    movie_title = scrapy.Field()
    dab_tit = scrapy.Field()
    cinema_hall = scrapy.Field()
    time_start = scrapy.Field()
    price = scrapy.Field()
    movie_attrs = scrapy.Field()

class CSFDProgramItem(scrapy.Item):
    cinema_name = scrapy.Field()
    cinema_city = scrapy.Field()
    cinema_fullname = scrapy.Field()
    cinema_tel = scrapy.Field()
    cinema_address = scrapy.Field()
    movie_id_csfd = scrapy.Field()
    cinema_url = scrapy.Field()
    date = scrapy.Field()
    movie_title = scrapy.Field()
    movie_url = scrapy.Field()
    dab_tit = scrapy.Field()
    rating_csfd_color = scrapy.Field()
    time_starts = scrapy.Field()

class CSFDMovieItem(scrapy.Item):
    movie_id_csfd = scrapy.Field()
    movie_title = scrapy.Field()
    movie_url = scrapy.Field()
    rating_csfd = scrapy.Field()
    movie_img = scrapy.Field()
    movie_genres = scrapy.Field()
    movie_origin_country = scrapy.Field()
    movie_origin_year = scrapy.Field()
    length = scrapy.Field()
    premiere_date = scrapy.Field()
    distribution = scrapy.Field()
    creators = scrapy.Field()