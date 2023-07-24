import scrapy
from cinema_scraper_project.items import MovieCinestar 
from datetime import datetime, timedelta


class CinestarSpiderSpider(scrapy.Spider):
    name = "cinestar_spider"
    allowed_domains = ["www.cinestar.cz"] # , "books.toscrape.com"
    start_urls = ["https://www.cinestar.cz/cz/"] # http://books.toscrape.com/

    custom_settings = {
        'FEEDS': {'cinestar_data.json': {'format': 'json', 'overwrite': True}}
        }

    #def parse(self, response):
    #    yield{
    #        'test': response.css('h1::text').get()
    #    }

    def parse(self, response):
        cinemas = response.css('ul.nav li')
        for cinema in cinemas:
            yield{
                'cinema_name': cinema.css('a::text').get(),
                'cinema_url': 'https://www.cinestar.cz' + cinema.css('a').attrib['href']
            }
            #cinema_name = cinema.css('a::text').get()
            #cinema_url = 'https://www.cinestar.cz' + cinema.css('a').attrib['href']
            cinema_page_url = 'https://www.cinestar.cz' + cinema.css('a').attrib['href']
            if cinema_page_url == 'https://www.cinestar.cz/cz/praha5/domu': # https://www.cinestar.cz/cz/liberec/domu
                yield response.follow(cinema_page_url, callback=self.parse_cinema_page)

    def parse_cinema_page(self, response):
        cinema_id = response.xpath("//script[@type='text/javascript']/text()").get().split(';')[1].split()[-1]
        movies = response.css("div.movies-carousel div a")
        for movie in movies:
            if movie.css("img").attrib['src'].split('/')[1] != 'files':
                movie_id = movie.attrib['href'].split('/')[-1].split('-')[0]
                movie_cinestar = MovieCinestar()
                movie_cinestar['movie_id'] = movie_id
                movie_cinestar['movie_title'] = movie.css("div.title::text").get()
                movie_cinestar['movie_premiere'] = movie.css("span.day::text").get() + ' ' + movie.css("span.month::text").get()
                movie_cinestar['movie_url'] = 'https://www.cinestar.cz' + movie.attrib['href']
                movie_cinestar['movie_img'] = movie.css("img").attrib['src']
                movie_cinestar['cinema_id'] = cinema_id
                movie_cinestar['cinema_name2'] = [x for x in response.css('td.cinema ::text').get().split('   ') if x != ''][1] + ', ' + response.css('tr.contact-city td ::text').get()
                movie_cinestar['cinema_url'] = response.url
                yield movie_cinestar

                days_ahead = 1
                for i in range(days_ahead):
                    date = str(datetime.now().date() + timedelta(days=i))
                    cin_mov_day_page_url = 'https://www.cinestar.cz/cz/?option=com_csevents&view=eventsbyhalls&date=' + date + '&cinema=' + cinema_id + '&titleId=' + movie_id + '&format=raw&tpl='
                    yield response.follow(cin_mov_day_page_url, callback=self.parse_day_page)

    def parse_day_page(self, response):
        movie_id = response.url.split('titleId=')[1].split('&')[0]
        cinema_id = response.url.split('cinema=')[1].split('&')[0]
        date_id = response.url.split('date=')[1].split('&')[0]
        date = response.css('h3::text').get()
        table_titles = response.css('div.tableTitle')
        for i, table_title in enumerate(table_titles):
            version = table_title.css('::text').get()
            table_title_class = table_title.attrib['class']
            if response.xpath(f"//div[@class='{table_title_class}']/following-sibling::p/text()").get() == 'Dabing':
                dab_tit = 'Dabing'
            else:
                dab_tit = 'Titulky'
            table = response.xpath(f"//div[@class='{table_title_class}']/following-sibling::table")[0]
            for j in range(len(table.css('a'))):
                time_url = table.css('a')[j].attrib['href']
                time_start = table.css('a::text')[j].get()
                time_end = table.css('div.detail')[j].css('em::text')[1].get()
                cinema_hall = table.css('div.detail')[j].css('em::text')[0].get()
                yield{
                    'movie_id': movie_id,
                    'cinema_id': cinema_id,
                    'date_id': date_id,
                    'date': date,
                    'version': version,
                    'dab/tit': dab_tit,
                    'cinema_hall': cinema_hall,
                    'time_start': time_start,
                    'time_end': time_end,
                    'time_url': time_url
                }
            if response.xpath(f"//div[@class='{table_title_class}']/following-sibling::p/text()").get() != 'Dabing':
                if (response.xpath(f"//div[@class='{table_title_class}']/following-sibling::p/following-sibling::p/text()").get() == 'Dabing' and 
                    (i+1 == len(table_titles) or 
                     response.xpath(f"//div[@class='{table_title_class}']/following-sibling::p/following-sibling::p/following-sibling::div/text()").get() == table_titles[i+1].css('::text').get())):
                    dab_tit = 'Dabing'
                    table = response.xpath(f"//div[@class='{table_title_class}']/following-sibling::p/following-sibling::p/following-sibling::table")[0]
                    for j in range(len(table.css('a'))):
                        time_url = table.css('a')[j].attrib['href']
                        time_start = table.css('a::text')[j].get()
                        time_end = table.css('div.detail')[j].css('em::text')[1].get()
                        cinema_hall = table.css('div.detail')[j].css('em::text')[0].get()
                        yield{
                            'movie_id': movie_id,
                            'cinema_id': cinema_id,
                            'date_id': date_id,
                            'date': date,
                            'version': version,
                            'dab/tit': dab_tit,
                            'cinema_hall': cinema_hall,
                            'time_start': time_start,
                            'time_end': time_end,
                            'time_url': time_url
                        }




            #yield{
            #    'movie_id': movie_id,
            #    'cinema_id': cinema_id,
            #    'date_id': date_id,
            #    'date': date,
            #    'version': version
            #}