import scrapy


class DigikalaProduct(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    sizes = scrapy.Field()
    colors = scrapy.Field()
    pure_price = scrapy.Field()
    image_urls = scrapy.Field()
