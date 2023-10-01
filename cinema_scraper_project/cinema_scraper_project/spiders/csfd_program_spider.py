import scrapy
from cinema_scraper_project.items import CSFDProgramItem


class CsfdProgramSpiderSpider(scrapy.Spider):
    name = 'csfd_program_spider'
    allowed_domains = ['www.csfd.cz']
    start_urls = ['https://www.csfd.cz/kino/?period=today&district=1'] # http://www.csfd.cz/

    custom_settings = {
        'FEEDS': {'csfd_program_data.json': {'format': 'json', 'overwrite': True}},
        'FEED_EXPORT_ENCODING': 'utf-8',
        'MONGODB_COLLECTION': 'csfd_program',
        'ITEM_PIPELINES': {
            "cinema_scraper_project.pipelines.MongoDBPipeline": 730
        }
        }

    def parse(self, response):
        districts = response.xpath("//select[@name='district']/option")
        for district in districts:
            csfd_district_url = 'https://www.csfd.cz/kino/?period=all&district=' + str(district.attrib['value'])
            yield response.follow(csfd_district_url, callback=self.parse_district_page)
    
    def parse_district_page(self, response):
        cinemas = response.css('div#snippet--cinemas section.box')
        for cinema in cinemas:
            cinema_name = cinema.css('header h2::text').get().split(' - ')[1]
            cinema_city = cinema.css('header h2::text').get().split(' - ')[0]
            cinema_fullname = cinema.css('header h2::text').get()
            cinema_tel = None
            cinema_address = cinema.css('header div.box-header-action::text').get().replace('\n', '').replace('\t', '')
            if 'tel' in cinema_address:
                cinema_tel = cinema_address.split('tel. ')[1].split(', ')[0]
                cinema_address = ", ".join(cinema_address.split(', ')[1:])
            cinema_url = None
            if len(cinema.css('header div')) > 1:
                cinema_url = cinema.css('header div.cinema-logo a').attrib['href']
            days = cinema.css('div.box-sub-header')
            programs = cinema.css('div.box-content')
            for day, program in zip(days, programs):
                date = day.css('::text').get().replace('\n', '').replace('\t', '')
                movies = program.css('tr')
                for movie in movies:
                    movie_title = movie.css('td.name h3 a::text').get()
                    movie_id_csfd = movie.css('td.name h3 a').attrib['href'].split('/')[2]
                    movie_url = 'https://www.csfd.cz' + movie.css('td.name h3 a').attrib['href']
                    dab_tit = movie.css('td.td-title span::text').get()
                    rating_csfd_color = movie.css('td.name h3 i').attrib['class'].split(' ')[-1]
                    time_starts = []
                    times = movie.css('td.td-time')
                    for time in times:
                        time_starts.append(time.css('::text').get().replace('\n', '').replace('\t', ''))
                    item = CSFDProgramItem()
                    item['cinema_name'] = cinema_name
                    item['cinema_city'] = cinema_city
                    item['cinema_fullname'] = cinema_fullname
                    item['cinema_tel'] = cinema_tel
                    item['cinema_address'] = cinema_address
                    item['movie_id_csfd'] = movie_id_csfd
                    item['cinema_url'] = cinema_url
                    item['date'] = date
                    item['movie_title'] = movie_title
                    item['movie_url'] = movie_url
                    item['dab_tit'] = dab_tit
                    item['rating_csfd_color'] = rating_csfd_color
                    item['time_starts'] = time_starts
                    yield item