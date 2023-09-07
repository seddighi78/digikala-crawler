# digikala-crawler
Scrapy crawler for digikala products information

## Installation
First of all, we need to install the requirements with this command:

### Intsll `virtualenv`:
```bash
pip3 install virtualenv
```

### Activate the new virtual environment:
```bash
virtualenv venv
source venv/bin/activate
```

### Install requirements inside that;
```bash
pip install -r requirements.txt
```

## Run the Flask application:
```bash
flask run
```
now application can be accessible from http://127.0.0.1:5000

## Run the crawler
there is a crawler named `products_spider.py` which crawls the products based on the `category`. to run this crawler run these commands in the activated virtual environment:
```bash
cd scrapy
scrapy crawl products
```