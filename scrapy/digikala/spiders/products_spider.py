import scrapy
import re
import json
from unidecode import unidecode
from digikala.items import DigikalaProduct


class ProductsSpider(scrapy.Spider):
    name = "products"
    category = 'mobile-accessories'
    base_url: str = "https://api.digikala.com/v1"
    page: int = 1
    all_pages: int = 1
    max_page: int = 20

    def start_requests(self):
        yield scrapy.Request(url=self.generate_page_url(), callback=self.parse)

    def parse(self, response, **kwargs):
        self.parse_all_pages_count(response)

        yield from self.parse_products_list(response)

    def parse_products_list(self, response):
        self.page += 1

        for product in json.loads(response.body)['data']['products']:
            url = self.generate_product_url(product['id'])

            if url is not None:
                yield scrapy.Request(url, callback=self.parse_product)

        if self.page <= self.all_pages and self.page <= self.max_page:
            yield from self.request_next_page()

    def parse_all_pages_count(self, response):
        total = decoded = json.loads(response.body)['data']['pager']['total_pages']
        
        if total is not None :
            self.all_pages = int(total)
        else:
            self.all_pages = 1

    def request_next_page(self):
        yield scrapy.Request(url=self.generate_page_url(), callback=self.parse_products_list)

    def parse_product(self, response):
        decoded = json.loads(response.body)['data']['product']
        
        product = DigikalaProduct()
        product['id'] = decoded['id']
        product['title'] = decoded['title_fa']
        product['category'] = decoded['category']['title_fa']
        product['image_urls'] = [decoded['images']['main']['url'][0]]
        product['sizes'] = self.extract_sizes_from_product(decoded)
        product['colors'] = self.extract_colors_from_product(decoded)
        product['pure_price'] = product['pure_price'] = decoded['default_variant']['price']['selling_price']
        
        yield product

    def extract_sizes_from_product(self, response):
        if 'varians' not in response:
            return []

        sizes = []
        for size in response['variants']:
            sizes.append(size['title'])

        return sizes
    
    def extract_colors_from_product(self, response):
        if 'colors' not in response:
            return []

        colors = []
        for color in response['colors']:
            colors.append(color['title'])

        return colors

    def id_pattern(self):
        return '(.*)dkp-(.*)/(.*)'

    def persian_to_english_number(self, text):
        return unidecode(text)

    def generate_page_url(self):
        return self.base_url + '/categories/' + self.category + '/search/?page=' + str(self.page)
    
    def generate_product_url(self, id):
        return self.base_url + '/product/' + str(id) + '/'
