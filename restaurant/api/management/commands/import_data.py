import logging
from typing import List, Dict

from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from requests_html import HTMLSession


class Command(BaseCommand):
    help = 'Import data from url'
    logger = logging.getLogger(__name__)

    RESTAURANT_URL = "https://pizzaportal.pl/bialystok/brooklyn-pizza-club-jurowiecka/"

    def parse_product_name(self, product) -> str:
        return product.find('h3', class_='restaurant-menu-product-name').text

    def parse_product_description(self, product) -> str:
        return product.find('p', class_='restaurant-menu-product-description').text

    def parse_product_price(self, product) -> str:
        price = product.find('div', class_='restaurant-menu-product-price').text
        price = price.replace(' zł', '')
        price = price.replace(',', '.')
        return price

    def parse_product(self, product) -> Dict[str, str]:
        return {
            "name": self.parse_product_name(product),
            "description": self.parse_product_description(product),
            "price": self.parse_product_price(product),
        }

    def parse_products(self, products) -> List[Dict]:
        return list(map(self.parse_product, products))

    def parse_section(self, section) -> Dict[str, List[Dict]]:
        category_name = section.find('div', class_='text')
        products_list = section.find_all('li', class_='restaurant-menu-product')
        return {
            "category": category_name.text,
            "products": self.parse_products(products_list)
        }

    def parse_sections(self, sections) -> List:
        return [self.parse_section(section) for section in sections]

    def get_sections_list(self):
        session = HTMLSession()
        resp = session.get(self.RESTAURANT_URL)
        page = resp.html.html
        soup = BeautifulSoup(page, 'html.parser')
        sections_list = soup.find('ul', class_='restaurant-menu-section-list')
        sections = sections_list.find_all('li', class_='restaurant-menu-section')
        return sections

    def handle(self, *args, **options):
        sections = self.get_sections_list()
        result = self.parse_sections(sections)
        print(result)
