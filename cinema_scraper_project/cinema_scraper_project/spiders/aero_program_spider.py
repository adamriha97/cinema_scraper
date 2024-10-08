import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
import time
from selenium.webdriver.chrome.options import Options
from cinema_scraper_project.items import AeroProgramItem, AeroProgramItemSimple

from shutil import which

#from scrapy_playwright.page import PageMethod


class AeroProgramSpiderSpider(scrapy.Spider):
    name = 'aero_program_spider'
    allowed_domains = ['www.kinoaero.cz']
    #start_urls = ['http://www.kinoaero.cz/']

    custom_settings = {
        'FEEDS': {'aero_program_data.json': {'format': 'json', 'overwrite': True}},
        'FEED_EXPORT_ENCODING': 'utf-8',
        'MONGODB_COLLECTION': 'aero_program',
        'ITEM_PIPELINES': {
            "cinema_scraper_project.pipelines.MongoDBPipeline": 720
        },
        'SELENIUM_DRIVER_NAME': 'chrome',
        #'SELENIUM_DRIVER_EXECUTABLE_PATH': which('.\cinema_scraper_project\chromedriver'),
        'SELENIUM_DRIVER_ARGUMENTS': ['--headless'],
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_selenium.SeleniumMiddleware': 800
        }
        }

    def start_requests(self):
        url = 'https://www.kinoaero.cz/?sort=sort-by-data&cinema=1%2C2%2C3%2C7&hall=10%2C23%2C1%2C2%2C3'
        yield SeleniumRequest(
            url=url, 
            callback=self.parse_notall, 
            wait_time=15,
            wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'program')) # modal-dialog modal-body__right modal-body__projection-time EC.element_to_be_clickable((By.CLASS_NAME, 'modal-body__projection-time')) EC.text_to_be_present_in_element((By.CLASS_NAME, "modal-body__projection-time"), ":")
        )

    def start_requests_all(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("window-size=1920,1080")
        #options.headless = True
        driver = Chrome(options=options)
        driver.get('https://www.kinoaero.cz/?sort=sort-by-data&cinema=2%2C3%2C7&hall=10%2C23%2C1%2C2%2C3') # https://www.kinoaero.cz/?sort=sort-by-data
        #driver.maximize_window()
        #driver.set_window_size(1920, 1080)
        time.sleep(5)
        driver.find_element(By.CLASS_NAME, 'custom-select__input-chevron').click()
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, 'form-check-input').click()
        driver.find_element(By.CLASS_NAME, 'custom-select__input-chevron-active').click()
        time.sleep(5)
        projections = driver.find_element(By.ID, 'projections-ids').get_attribute('data-projections').split(',')
        for projection in projections[:-1]:
            url = f'https://www.kinoaero.cz/?sort=sort-by-data&cinema=1%2C2%2C3%2C7&hall=10%2C23%2C1%2C2%2C3&projection={projection}'
            yield SeleniumRequest(
                url=url, 
                callback=self.parse, 
                wait_time=15,
                wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'modal-dialog')) # modal-dialog modal-body__right modal-body__projection-time EC.element_to_be_clickable((By.CLASS_NAME, 'modal-body__projection-time')) EC.text_to_be_present_in_element((By.CLASS_NAME, "modal-body__projection-time"), ":")
            )
        #    yield scrapy.Request(url, meta=dict(
        #        playwright = True,
        #        playwright_include_page = True, 
        #        playwright_page_methods =[PageMethod('wait_for_selector', 'div.modal-dialog')],
        #    errback=self.errback,
        #    ))
        driver.quit()

        ###url = 'https://www.kinoaero.cz/?sort=sort-by-data&cinema=1%2C2%2C3%2C7&hall=1%2C2%2C3' # https://www.kinoaero.cz/?cinema=2%2C3%2C7&sort=sort-by-data&hall=1%2C2%2C3
        #return super().start_requests()
        #yield scrapy.Request(url, meta={'playwright': True})
        ###yield SeleniumRequest(
        ###    url=url, 
        ###    callback=self.parse, 
            #script="""
            #    document.querySelector('.form-check-input').click();
            #    document.querySelector('.navigation__hamburger').click();
            #    """, #()setTimeout(document.querySelector('.form-check-input').click(), 5);
        ###    wait_time=15,
        ###    wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'program')) # EC.text_to_be_present_in_element((By.CLASS_NAME, "program__place"), "Aero")
        ###)

    def parse(self, response):
    #async def parse(self, response):
    #    page = response.meta["playwright_page"]
    #    await page.close()

        dialog = response.css('div.modal-dialog')
        item = AeroProgramItem()
        movie_info = str(dialog.css('div.modal-body__right h6').get()).split('\n')[1].strip()
        item['event_id'] = response.url.split('&projection=')[1]
        item['event_url'] = response.url
        item['cinema_name3'] = dialog.css('div.modal-body__projection-cinema span::text').get()
        item['date_orig'] = dialog.css('div.modal-body__projection-day ::text').get().replace('\n', '').strip()
        item['movie_title'] = dialog.css('div.modal-body__right h3::text').get()
        item['movie_img'] = 'http://www.kinoaero.cz' + dialog.css('div.slick-track img').attrib['src']
        item['movie_imgs'] = []
        for img in dialog.css('div.slick-track img'):
            item['movie_imgs'].append('http://www.kinoaero.cz' + img.css('img').attrib['src'])
        item['movie_vid'] = 'N/A'
        if dialog.css('button#trailer-button') is not None:
            item['movie_vid'] = 'https://www.youtube.com/watch?v=' + dialog.css('button#trailer-button').attrib['data-youtube-id']
        item['dab_tit'] = 'N/A'
        if 'znění: ' in movie_info:
            if 'čeština' in movie_info.split('nění: ')[1].split('/')[0]:
                item['dab_tit'] = 'Dabing'
            elif 'titulky: ' in movie_info:
                if 'čeština' in movie_info.split('itulky: ')[1].split('/')[0]:
                    item['dab_tit'] = 'Titulky'
        elif 'titulky: ' in movie_info:
            if 'čeština' in movie_info.split('itulky: ')[1].split('/')[0]:
                item['dab_tit'] = 'Titulky'
        item['cinema_hall'] = str(dialog.css('div.modal-body__projection-cinema').get()).split('\n')[-2].strip()
        item['time_start'] = dialog.css('div.modal-body__projection-time ::text').get().replace('\n', '').strip()
        item['length'] = 'N/A'
        if ' min.' in movie_info:
            item['length'] = movie_info.split(' min.')[0].split()[-1]
        #* zde u price je pravdepodobne problem, neni asi vzdy button
        item['price'] = dialog.css('button.modal-body__projection-price span::text').get()
        item['calendar_url'] = 'http://www.kinoaero.cz' + dialog.css('a.modal-body__projection-calendar').attrib['href']
        item['movie_attrs'] = []
        if dialog.css('div.modal-body__right span.modal-body__tag') is not None:
            for tag in dialog.css('div.modal-body__right span.modal-body__tag'):
                item['movie_attrs'].append(tag.css('span.modal-body__tag ::text').get())
        item['movie_info'] = movie_info
        item['movie_score_urls'] = []
        if dialog.css('div.modal-body__right a.btn-outline-secondary') is not None:
            for score in dialog.css('div.modal-body__right a.btn-outline-secondary'):
                item['movie_score_urls'].append(score.css('a.btn-outline-secondary').attrib['href'])
        yield item

    #async def errback(self, failure):
    #    page = failure.request.meta["playwright_page"]
    #    await page.close()

    def parse_notall(self, response):
        for day in response.css('div.program'):
            date = day.css('div.program__day span::text').get()
            for film in day.css('div.program__info-row'):
                event_id = film.css('div.program__movie-name').attrib['data-projection']
                movie_attrs = []
                if film.css('div.program__tags span.program__tag') is not None:
                    for tag in film.css('div.program__tags span.program__tag'):
                        movie_attrs.append(tag.css('span.program__tag ::text').get().replace('\n', '').strip())
                item = AeroProgramItemSimple()
                item['event_id'] = event_id
                item['event_url'] = f'https://www.kinoaero.cz/?sort=sort-by-data&cinema=1%2C2%2C3%2C7&hall=10%2C23%2C1%2C2%2C3&projection={event_id}'
                item['cinema_name3'] = film.css('div.program__place span::text').get()
                item['date_orig'] = date
                item['movie_title'] = film.css('div.program__movie-name ::text').get()
                item['dab_tit'] = 'N/A'
                if 'dabing' in movie_attrs or 'Dabing' in movie_attrs:
                    item['dab_tit'] = 'Dabing'
                item['cinema_hall'] = str(film.css('div.program__place').get()).split('\n')[-1].replace('</div>', '').strip()
                item['time_start'] = film.css('div.program__hour ::text').get()
                item['price'] = film.css('div.program__price span::text').get().replace('\n', '').strip()
                item['movie_attrs'] = movie_attrs
                yield item
