import requests
import io

from bs4 import BeautifulSoup
from functools import wraps
from requests.exceptions import HTTPError

from ._food_data_parser import FoodDataParser


FOOD_DATA_URL = 'https://www.ers.usda.gov'
FOOD_DATA_PATH = FOOD_DATA_URL + '/data-products/fruit-and-vegetable-prices.aspx'

class FoodDataScraper:
    def __init__(self):
        self.parser = FoodDataParser()

    def get_raw_html(self):
        request = requests.get(FOOD_DATA_PATH)
        request.raise_for_status()
        return request.text

    def get_html(self):
        raw_html = self.get_raw_html()
        return BeautifulSoup(raw_html, 'html.parser')

    def get_xlsx_urls(self):
        html = self.get_html()
        return (FOOD_DATA_URL + row.a.get('href') for row in html.find_all('td') if 'DataFileItem' in row.get('class'))

    def get_xlsx_data(self, url):
        request = requests.get(url)
        request.raise_for_status()
        parsed_data = self.parser(request.content)

        return parsed_data

    @property
    def urls(self):
        return list(self.get_xlsx_urls())

    @staticmethod
    def for_parsed_files(f):
        @wraps(f)
        def wrapped(self, *args, **kwargs):
            scraper = FoodDataScraper()
            for url in scraper.urls:
                try:
                    print(f'Parsing file {url}...')
                    f(self, scraper.get_xlsx_data(url), *args, **kwargs)
                except BaseException as e:
                    if type(e) == KeyboardInterrupt:
                        quit()
                    print(f'An error occured file parsing file {url}: {e}')


        return wrapped
