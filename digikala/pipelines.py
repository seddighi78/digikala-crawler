import sqlite3
import json


class SqlitePipeline:

    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        self.create_products_table()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            name=crawler.settings.get('SQLITE_DATABASE_NAME')
        )

    def create_products_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id real primary key,
            title text null,
            category varchar null,
            sizes text null,
            colors text null,
            pure_price real null,
            image_urls text null                   
        )
        """)

    def process_item(self, item, spider):
        self.insert_item(item)

        return item

    def insert_item(self, item):
        self.cursor.execute("""INSERT OR IGNORE INTO products VALUES(?,?,?,?,?,?,?)""", (
            item['id'],
            item['title'],
            item['category'],
            json.dumps(item['sizes']),
            json.dumps(item['colors']),
            item['pure_price'],
            item['image_urls'][0],
        ))
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()
