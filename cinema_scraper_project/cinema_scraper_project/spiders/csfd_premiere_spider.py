import scrapy
from cinema_scraper_project.items import CSFDMovieItem


class CsfdPremiereSpiderSpider(scrapy.Spider):
    name = 'csfd_premiere_spider'
    allowed_domains = ['www.csfd.cz']
    start_urls = ['http://www.csfd.cz/']

    custom_settings = {
        'FEEDS': {'csfd_premiere_data.json': {'format': 'json', 'overwrite': True}},
        'FEED_EXPORT_ENCODING': 'utf-8',
        'MONGODB_COLLECTION': 'csfd_premiere',
        'ITEM_PIPELINES': {
            "cinema_scraper_project.pipelines.MongoDBPipeline": 735
        }
        }
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        spider = cls(settings)
        spider._set_crawler(crawler)
        return spider

    def __init__(self, settings):
        self.years = settings.get('YEARS_OF_PREMIERES')

    def parse(self, response):
        for year in self.years:
            csfd_premieres_url = 'https://www.csfd.cz/kino/prehled/?year=' + str(year)
            yield response.follow(csfd_premieres_url, callback=self.parse_premieres_page)
    
    def parse_premieres_page(self, response):
        premieres = response.css('a.film-title-name')
        for premiere in premieres:
            csfd_movie_url = 'https://www.csfd.cz/' + premiere.attrib['href']
            yield response.follow(csfd_movie_url, callback=self.parse_movie_page)
    
    def parse_movie_page(self, response):
        movie_id_csfd = response.url.split('/')[-3]
        movie_title = response.css('div.film-header-name h1::text').get().replace('\n', '').replace('\t', '')
        movie_url = response.url
        rating_csfd = response.css('div.film-rating-average::text').get().replace('\n', '').replace('\t', '')
        movie_img = 'https:' + response.css('div.film-posters img').attrib['src']
        info = response.css('div.film-info-content')
        movie_genres = info.css('div.genres::text').get().split(' / ')
        movie_origin_country = info.css('div.origin::text').get().split(', ')[0].split(' / ')
        movie_origin_year = info.css('div.origin span::text').get().split(',')[0]
        length = info.css('div.origin').get().split('</span>')[1].split('\n')[0]
        premiere_date = response.css('section.box-premieres span::text').get().replace('\t', '').split('\n')[1]
        distribution = response.css('section.box-premieres span::text').get().replace('\t', '').split('\n')[2]
        item = CSFDMovieItem()
        item['movie_id_csfd'] = movie_id_csfd
        item['movie_title'] = movie_title
        item['movie_url'] = movie_url
        item['rating_csfd'] = rating_csfd
        item['movie_img'] = movie_img
        item['movie_genres'] = movie_genres
        item['movie_origin_country'] = movie_origin_country
        item['movie_origin_year'] = movie_origin_year
        item['length'] = length
        item['premiere_date'] = premiere_date
        item['distribution'] = distribution
        item['creators'] = {}
        creators = info.css('div.creators div')
        for creator in creators:
            item['creators'][creator.css('h4::text').get().replace(':', '')] = creator.css('a::text').getall()
        yield item