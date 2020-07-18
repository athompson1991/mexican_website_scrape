import datetime
import hashlib

import bs4

from core.spiders.core_spiders import ListingsSpider
from core.utils import url_hash


class InformadorListingsSpider(ListingsSpider):
    n = 100
    page_range = list(range(1, n))
    name = "informador_listings"
    url_stem = "https://www.informador.mx"
    sections = [
        "jalisco",
        "mexico",
        "internacional",
        "deportes",
        "entretenimiento",
        "economia",
        "tecnologia",
        "ideas",
        "cultura"
    ]

    def __init__(self):
        super().__init__()
        self.create_urls(self.url_gen, self.sections, list(self.page_range))

    def url_gen(self, section, page):
        xref = "/ajax/get_section_news.html?"
        size = "size=100"
        query = "page=" + str(page) + "&" + size + "&section=" + section
        return self.url_stem + xref + query

    def parse(self, response):
        soup, out = super(InformadorListingsSpider, self).parse(response)
        out["section"] = response.url.split("=")[-1]
        articles = soup.find_all("article")
        for article in articles:
            out["url"] = article.find("a").get("href")
            out["url"] = self.url_stem + out["url"]
            out["headline"] = article.find("a").get("title")
            dt_str = article.find("time").get("datetime")
            dt = datetime.datetime.strptime(dt_str, "%Y-%d-%mT%H:%M")
            out["publish_date"] = dt.strftime("%Y-%m-%d")
            out["publish_time"] = dt.strftime("%H:%M")
            out["url_hash"] = url_hash(out["url"])
            yield out