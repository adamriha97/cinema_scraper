import scrapy
from cinema_scraper_project.items import CinemacityProgramItem
from datetime import datetime, timedelta
import json


class CinemacityProgramSpiderSpider(scrapy.Spider):
    name = 'cinemacity_program_spider'
    allowed_domains = ['www.cinemacity.cz']
    start_urls = ['https://www.cinemacity.cz/sitemap.xml'] # http://www.cinemacity.cz/

    custom_settings = {
        'FEEDS': {'cinemacity_program_data.json': {'format': 'json', 'overwrite': True}},
        'FEED_EXPORT_ENCODING': 'utf-8',
        'MONGODB_COLLECTION': 'cinemacity_program',
        'ITEM_PIPELINES': {
            "cinema_scraper_project.pipelines.MongoDBPipeline": 710
        }
        }
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        spider = cls(settings)
        spider._set_crawler(crawler)
        return spider

    def __init__(self, settings):
        self.days_ahead = settings.get('DAYS_AHEAD_TO_SCRAPE')

    def parse(self, response):
        global cinemas_dict
        cinemas_dict = {}
        cinemas = [u.split('</loc>')[0] for u in str(response.body).split('<loc>') if 'https://www.cinemacity.cz/cinemas/' in u]
        for cinema in cinemas:
            cinema_cinemacity_url = cinema
            #if cinema_cinestar_url == 'https://www.cinestar.cz/cz/praha5/domu': # https://www.cinestar.cz/cz/liberec/domu https://www.cinestar.cz/cz/praha5/domu
            yield response.follow(cinema_cinemacity_url, callback=self.parse_cinema_page)

    def parse_cinema_page(self, response):
        global cinemas_dict
        cinema_id = response.url.split('/')[-1]
        cinemas_dict[cinema_id] = response.css('span.selectedCinema::text').get().strip()
        if self.days_ahead is None:
            days_ahead = 15
        else:
            days_ahead = self.days_ahead + 1
        for i in range(days_ahead):
            date = str(datetime.now().date() + timedelta(days=i))
            cin_day_page_url = 'https://www.cinemacity.cz/cz/data-api-service/v1/quickbook/10101/film-events/in-cinema/' + cinema_id + '/at-date/' + date + '?attr=&lang=cs_CZ'
            #if cin_day_page_url == 'https://www.cinemacity.cz/cz/data-api-service/v1/quickbook/10101/film-events/in-cinema/1034/at-date/2023-08-15?attr=&lang=cs_CZ':
            yield response.follow(cin_day_page_url, callback=self.parse_day_page)

    def find_film_by_id(self, target_id, json_data):
        for item in json_data:
            if item['id'] == target_id:
                return item
        return None

    def parse_day_page(self, response):
        global cinemas_dict
        data = json.loads(response.body)
        films = data['body']['films']
        events = data['body']['events']
        for event in events:
            film = self.find_film_by_id(event['filmId'], films)
            item = CinemacityProgramItem()
            item['event_id'] = event['id']
            item['cinema_id'] = event['cinemaId']
            item['cinema_name3'] = cinemas_dict[event['cinemaId']]
            item['date_id'] = event['businessDay']
            item['date'] = datetime.strptime(event['businessDay'], "%Y-%m-%d").strftime("%d.%m.%Y")
            item['movie_id'] = event['filmId']
            item['movie_title'] = film['name']
            item['movie_url'] = film['link']
            item['movie_img'] = film['posterLink']
            item['movie_vid'] = film['videoLink']
            item['movie_release_year'] = film['releaseYear']
            if 'dubbed' in event['attributeIds']:
                item['dab_tit'] = 'Dabing'
            elif 'subbed' in event['attributeIds']:
                item['dab_tit'] = 'Titulky'
            else:
                item['dab_tit'] = 'N/A'
            item['cinema_hall'] = event['auditoriumTinyName']
            item['cinema_hall_long'] = event['auditorium']
            item['time_start'] = datetime.strptime(event['eventDateTime'], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")
            item['time_url'] = event['bookingLink']
            item['length'] = film['length']
            item['sold_out'] = event['soldOut']
            item['movie_attrs'] = film['attributeIds']
            item['event_attrs'] = event['attributeIds']
            yield item