import scrapy
import re
from unidecode import unidecode
from digikala.items import DigikalaProduct


class ApparelSpider(scrapy.Spider):
    name = "apparel"
    base_url: str = "https://www.digikala.com"
    page: int = 1
    all_pages: int = 1

    def start_requests(self):
        yield scrapy.Request(url=self.generate_page_url(), callback=self.parse)

    def parse(self, response, **kwargs):
        self.parse_all_pages_count(response)
        yield from self.parse_products_list(response)

    def parse_products_list(self, response):
        self.page += 1

        for product in response.css('ul.c-listing__items > li'):
            url = product.css('a.js-product-url::attr(href)').extract_first(),
            if url is not None:
                url = self.base_url + url[0]
                yield scrapy.Request(url, callback=self.parse_product)

        if self.page <= self.all_pages:
            yield from self.request_next_page()

    def parse_all_pages_count(self, response):
        total = response.css('a.c-pager__next::attr(data-page)').extract_first(),
        if total is not None:
            self.all_pages = int(total[0])
        else:
            self.all_pages = 1

    def request_next_page(self):
        yield scrapy.Request(url=self.generate_page_url(), callback=self.parse_products_list)

    def parse_product(self, response):
        product = DigikalaProduct()
        product['id'] = (re.search(self.id_pattern(), response.url)).group(2)
        product['title'] = response.css('h1.c-product__title::text').get().strip()
        product['category'] = response.css('div.c-product__nav-container nav.js-breadcrumb a span::text')[-1].get()
        product['colors'] = response.css('li.c-circle-variant__item span.c-tooltip--short::text').getall()
        product['sizes'] = [self.persian_to_english_number(size.strip()) for size in response.css('select.c-product__size-dropdown option::text').getall()]
        product['pure_price'] = self.persian_to_english_number(response.css('div.c-product__seller-price-pure::text').get().strip())
        product['image_urls'] = [response.css('img.js-gallery-img::attr(data-src)').get()]

        yield product

    def id_pattern(self):
        return '(.*)dkp-(.*)/(.*)'

    def persian_to_english_number(self, text):
        return unidecode(text)

    def generate_page_url(self):
        return self.base_url + '/search/apparel/?pageno=' + str(self.page)
