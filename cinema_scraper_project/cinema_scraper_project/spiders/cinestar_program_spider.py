import scrapy
from cinema_scraper_project.items import CinestarProgramItem
from datetime import datetime, timedelta


class CinestarProgramSpiderSpider(scrapy.Spider):
    name = 'cinestar_program_spider'
    allowed_domains = ['www.cinestar.cz']
    start_urls = ['http://www.cinestar.cz/cz/']

    custom_settings = {
        'FEEDS': {'cinestar_program_data.json': {'format': 'json', 'overwrite': True}},
        'FEED_EXPORT_ENCODING': 'utf-8'
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
        cinemas = response.css('ul.nav li')
        for cinema in cinemas:
            cinema_cinestar_url = 'https://www.cinestar.cz' + cinema.css('a').attrib['href']
            #if cinema_cinestar_url == 'https://www.cinestar.cz/cz/praha5/domu': # https://www.cinestar.cz/cz/liberec/domu https://www.cinestar.cz/cz/praha5/domu
            yield response.follow(cinema_cinestar_url, callback=self.parse_cinema_page)

    def parse_cinema_page(self, response):
        global cinemas_dict
        cinema_id = response.xpath("//script[@type='text/javascript']/text()").get().split(';')[1].split()[-1]
        cinemas_dict[cinema_id] = [x for x in response.css('td.cinema ::text').get().split('   ') if x != ''][1] + (', České Budějovice' if response.css('tr.contact-city td ::text').get() == 'České Budějovice' else '') # ', ' + response.css('tr.contact-city td ::text').get()
        if self.days_ahead is None:
            days_ahead = 15
        else:
            days_ahead = self.days_ahead + 1
        for i in range(days_ahead):
            date = str(datetime.now().date() + timedelta(days=i))
            cin_day_page_url = 'https://www.cinestar.cz/cz/?option=com_csevents&view=eventsforday&date=' + date + '&cinema=' + cinema_id + '&titleId=0&format=raw&tpl=program'
            #if cin_day_page_url == 'https://www.cinestar.cz/cz/?option=com_csevents&view=eventsforday&date=2023-08-21&cinema=11&titleId=0&format=raw&tpl=program': # https://www.cinestar.cz/cz/?option=com_csevents&view=eventsforday&date=2023-08-21&cinema=11&titleId=0&format=raw&tpl=program https://www.cinestar.cz/cz/?option=com_csevents&view=eventsforday&date=2023-08-17&cinema=11&titleId=0&format=raw&tpl=program
            yield response.follow(cin_day_page_url, callback=self.parse_day_page)

    def parse_day_page(self, response):
        global cinemas_dict
        cinema_id = response.url.split('cinema=')[1].split('&')[0]
        date_id = response.url.split('date=')[1].split('&')[0]
        date = response.css('h3::text').get()
        movies = response.css('tr.even') + response.css('tr.odd')
        for movie in movies:
            movie_title_long = movie.css('td.tdTitle span.title a::text').get()
            movie_title = movie.css('td.tdTitle span.title a::text').get().replace(' DABING', '').replace(' TITULKY', '').replace(' ATMOS', '').replace(' TDL', '').replace(' GC', '').replace(' ČSFD', '').replace(' PRO SENIORY', '').replace(' CZ', '')
            movie_url = 'https://www.cinestar.cz' + movie.css('td.tdTitle span.title a').attrib['href']
            movie_img = movie.css('td.tdTitle img').attrib['src']
            if 'CZ' in movie_title_long:
                dab_tit = 'Dabing'
                rating = 'N/A'
                rating_detail = 'N/A'
                if movie.css('td.tdTitle span.desc span.play-param').get() is not None:
                    rating = movie.css('td.tdTitle span.desc span.play-param')[0].css('a::text').get()
                    rating_detail = movie.css('td.tdTitle span.desc span.play-param')[0].css('div.detail::text').get().split('        ')[1].replace('\t', '')
            else:
                dab_tit = 'N/A'
                rating = 'N/A'
                rating_detail = 'N/A'
                #if movie.css('td.tdTitle span.desc span.play-param').get() is not None:
                if len(movie.css('td.tdTitle span.desc span.play-param')) == 2:
                    dab_tit = movie.css('td.tdTitle span.desc span.play-param')[0].css('a::text').get()
                    rating = movie.css('td.tdTitle span.desc span.play-param')[1].css('a::text').get()
                    rating_detail = movie.css('td.tdTitle span.desc span.play-param')[1].css('div.detail::text').get().split('        ')[1].replace('\t', '')
                elif len(movie.css('td.tdTitle span.desc span.play-param')) == 1:
                    if movie.css('td.tdTitle span.desc span.play-param').css('div.detail::text').get() is not None:
                        rating = movie.css('td.tdTitle span.desc span.play-param').css('a::text').get()
                        rating_detail = movie.css('td.tdTitle span.desc span.play-param').css('div.detail::text').get().split('        ')[1].replace('\t', '')
                    else:
                        dab_tit = movie.css('td.tdTitle span.desc span.play-param').css('a::text').get()
            uhd = 0
            if movie.css('td.tdTitle span.desc span.ctyrik span::text').get() is not None: uhd = 1
            premiere = 0
            if movie.css('td.tdTitle span.desc span.premiera span::text').get() is not None: premiere = 1
            new = 0
            if movie.css('td.tdTitle span.desc span.premiera div.detail::text').get() is not None: new = 1 # movie.css('td.tdTitle span.desc span.premiera div.detail::text').get().split('        ')[1].replace('\t', '')
            times = movie.css('td')[1:]
            for time_td in times:
                #if time.css('span'):
                for time in time_td.xpath("span"):
                    if time.css('span a::text').get() is None:
                        projected = 1
                        time_start = time.css('span::text').get().replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
                        time_url = ''
                    else:
                        projected = 0
                        time_start = time.css('span a::text').get()
                        time_url = time.css('span a').attrib['href']
                    time_end = time.css('span div.detail em')[2].css('::text').get()
                    cinema_hall = time.css('span div.detail em')[0].css('::text').get()
                    length = time.css('span div.detail em')[1].css('::text').get()
                    item = CinestarProgramItem()
                    item['cinema_id'] = cinema_id
                    item['cinema_name3'] = cinemas_dict[cinema_id]
                    item['date_id'] = date_id
                    item['date'] = date
                    item['movie_title'] = movie_title
                    item['movie_title_long'] = movie_title_long
                    item['movie_url'] = movie_url
                    item['movie_img'] = movie_img
                    item['dab_tit'] = dab_tit
                    item['rating'] = rating
                    item['rating_detail'] = rating_detail
                    item['uhd'] = uhd
                    item['premiere'] = premiere
                    item['new'] = new
                    item['projected'] = projected
                    item['cinema_hall'] = cinema_hall
                    item['time_start'] = time_start
                    item['time_end'] = time_end
                    item['time_url'] = time_url
                    item['length'] = length
                    yield item