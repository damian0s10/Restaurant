import copy
import logging
from typing import List, Dict

from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from requests_html import HTMLSession

from api.serializers import CategorySerializer


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

    def prepare_to_save(self, data):
        results = []

        for item in data:
            category = item.get('category')
            products = item.get('products')

            if category == 'Pizza':
                tmp = []
                for product in products:
                    product_big_size = copy.deepcopy(product)
                    product_big_size.update({
                        "name": f"{product_big_size.get('name')} (42 cm)"
                    })

                    product_small_size = copy.deepcopy(product)
                    product_small_size.update({
                        "name": f"{product_small_size.get('name')} (32 cm)",
                        "price": float(product_small_size.get('price')) - 10.50
                    })

                    tmp.append(product_big_size)
                    tmp.append(product_small_size)
                products = tmp
            results.append({
                "name": category,
                "products": products
            })

        return results

    def handle(self, *args, **options):
        sections = self.get_sections_list()
        results = self.parse_sections(sections)
        data = self.prepare_to_save(results)
        serializer = CategorySerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.logger.debug("Products imported")
