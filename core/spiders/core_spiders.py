import locale

import scrapy

from core import pipelines


class ListingsSpider(scrapy.Spider):

    pipeline = {pipelines.CSVPipeline}
    colnames = [
        "url",
        "url_hash",
        "scraped_from",
        "section",
        "headline",
        "publish_time",
        "publish_date"
    ]

    def __init__(self):
        super().__init__()
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        self.urls = []

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def create_urls(self, func, sections, pages):
        self.urls = []
        for section in sections:
            for page in pages:
                new_url = func(section, page)
                self.urls.append(new_url)


