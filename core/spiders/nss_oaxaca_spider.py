import hashlib

import bs4

from core.spiders.core_spiders import ListingsSpider
from core.utils import url_hash


class NssOaxacaListingsSpider(ListingsSpider):
    n = 100
    page_range = range(1, n)
    name = "nss_oaxaca_listings"
    url_stem = "https://www.nssoaxaca.com/"
    sections = [
        "estado",
        "municipios",
        "ciudad",
        "politica",
        "deportes",
        "turismo",
        "justicia",
        "nacional",
        "policiaca",
        "culturas",
        "sociales",
        "educacion",
        "economia",
        "ciencia-y-tecnologia",
        "entretenimiento",
        "salud",
        "them",
        "mundo"
    ]

    def __init__(self):
        super().__init__()
        self.create_urls(self.url_gen, self.sections, list(self.page_range))

    def url_gen(self, section, page):
        return self.url_stem + "/category/" + section + "/page/" + str(page)

    def parse(self, response):
        soup, out = super(NssOaxacaListingsSpider, self).parse(response)
        posts = soup.find_all("div", {"class": "infinite-post"})
        out["section"] = response.url.split("/")[4]
        for post in posts:
            out["url"] = post.find("a").get("href")
            out["publish_date"] = "-".join(out["url"].split("/")[3:6])
            out["url_hash"] = url_hash(out["url"])
            out["headline"] = post.find("h2").text
            yield out