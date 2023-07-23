import scrapy
from cinema_scraper_project.items import MovieCinestar 


class CinestarSpiderSpider(scrapy.Spider):
    name = "cinestar_spider"
    allowed_domains = ["www.cinestar.cz"]
    start_urls = ["https://www.cinestar.cz/cz/"]

    def parse(self, response):
        global cinema_name, cinema_url
        cinemas = response.css('ul.nav li')
        for cinema in cinemas:
            yield{
                'cinema_name': cinema.css('a::text').get(),
                'cinema_url': 'https://www.cinestar.cz' + cinema.css('a').attrib['href']
            }
            cinema_name = cinema.css('a::text').get()
            cinema_url = 'https://www.cinestar.cz' + cinema.css('a').attrib['href']
            cinema_page_url = 'https://www.cinestar.cz' + cinema.css('a').attrib['href']
            yield response.follow(cinema_page_url, callback=self.parse_cinema_page)

    def parse_cinema_page(self, response):
        cinema_id = response.xpath("//script[@type='text/javascript']/text()").get().split(';')[1].split()[-1]
        movies = response.css("div.movies-carousel div a")
        for movie in movies:
            if movie.css("img").attrib['src'].split('/')[1] != 'files':
                movie_cinestar = MovieCinestar()
                movie_cinestar['movie_id'] = movie.attrib['href'].split('/')[-1].split('-')[0]
                movie_cinestar['movie_title'] = movie.css("div.title::text").get()
                movie_cinestar['movie_premiere'] = movie.css("span.day::text").get() + ' ' + movie.css("span.month::text").get()
                movie_cinestar['movie_url'] = 'https://www.cinestar.cz' + movie.attrib['href']
                movie_cinestar['movie_img'] = movie.css("img").attrib['src']
                movie_cinestar['cinema_id'] = cinema_id
                movie_cinestar['cinema_name2'] = [x for x in response.css('td.cinema ::text').get().split('   ') if x != ''][1] + ', ' + response.css('tr.contact-city td ::text').get()
                movie_cinestar['cinema_url'] = response.url
                yield movie_cinestar