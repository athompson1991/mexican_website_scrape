import hashlib
import locale

import bs4
import scrapy

from core import pipelines
from core.sections import listings_sections
from core.utils import get_urls, url_hash, camel_case_split


class PrimarySpider(scrapy.Spider):

    def __init__(self):
        super().__init__()
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        self.urls = []
        self.class_name = type(self).__name__
        print("Created spider: " + self.class_name)

    def url_hash(self, url):
        hasher = hashlib.sha3_224(url.encode("utf-8"))
        return hasher.hexdigest()[:15]

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) '
                                 'Gecko/20100101 Firefox/48.0'}
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)




class ListingsSpider(PrimarySpider):
    n = 100
    page_range = list(range(1, n))

    pipeline = {pipelines.CSVPipeline}
    colnames = [
        "url",
        "url_hash",
        "site",
        "scraped_from",
        "section",
        "headline",
        "publish_time",
        "publish_date"
    ]

    def __init__(self):
        super(ListingsSpider, self).__init__()
        self.sections = listings_sections[self.name[:-9]]

    def create_urls(self, func, sections, pages):
        self.urls = []
        for section in sections:
            for page in pages:
                new_url = func(section, page)
                self.urls.append(new_url)

    def parse(self, response):
        soup = bs4.BeautifulSoup(response.text)
        out = {
            "scraped_from": response.url,
            "site": self.name[:-9],
            "publish_time": None,
            "publish_date": None
        }
        return soup, out


class ArticleSpider(PrimarySpider):

    pipeline = {pipelines.ArticlePipeline}
    colnames = None

    def __init__(self):
        super().__init__()
        self.assign_urls()

    def assign_urls(self):
        file = "listings_tables/" + self.name[:-9] + ".csv"
        self.urls = list(get_urls(file))[1:]

    def parse(self, response):
        out = {
            "url": response.url,
            "url_hash": None,
            "headline": None,
            "paragraphs": None,
            "author": None
        }
        out["url_hash"] = url_hash(out["url"])
        soup = bs4.BeautifulSoup(response.text)
        return soup, out
