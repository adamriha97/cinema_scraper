import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class AeroProgramSpiderSpider(scrapy.Spider):
    name = 'aero_program_spider'
    #allowed_domains = ['www.kinoaero.cz']
    #start_urls = ['http://www.kinoaero.cz/']

    custom_settings = {
        'FEEDS': {'aero_program_data.json': {'format': 'json', 'overwrite': True}},
        'FEED_EXPORT_ENCODING': 'utf-8'
        }

    def start_requests(self):
        url = 'https://www.kinoaero.cz/?sort=sort-by-data&cinema=1%2C2%2C3%2C7&hall=1%2C2%2C3' # https://www.kinoaero.cz/?cinema=2%2C3%2C7&sort=sort-by-data&hall=1%2C2%2C3
        #return super().start_requests()
        #yield scrapy.Request(url, meta={'playwright': True})
        yield SeleniumRequest(
            url=url, 
            callback=self.parse, 
            #script="""
            #    document.querySelector('.form-check-input').click();
            #    document.querySelector('.navigation__hamburger').click();
            #    """, #()setTimeout(document.querySelector('.form-check-input').click(), 5);
            wait_time=15,
            wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'program')) # EC.text_to_be_present_in_element((By.CLASS_NAME, "program__place"), "Aero")
        )

    def parse(self, response):
        for program in response.css('div.program'):
            yield {
                'day': program.css('span.desktop::text').get()
            }
