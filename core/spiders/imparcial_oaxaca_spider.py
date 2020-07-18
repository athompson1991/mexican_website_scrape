import hashlib
import locale

import bs4
import scrapy

from core.spiders.core_spiders import ListingsSpider
from core.utils import get_urls, url_hash


class ImparcialOaxacaListingsSpider(ListingsSpider):
    n = 100

    name = "imparcial_oaxaca_listings"
    url_stem = "https://imparcialoaxaca.mx/"
    sections = [
        'nacional',
        'internacional',
        'ecologia',
        'economia',
        'salud',
        'viral',
        'arte-y-cultura',
        'en-escena'
        'tecnologia',
        'ciencia',
        'policiaca',
        'super-deportivo',
        'especiales',
        'oaxaca',
        'caniada',
        'costa',
        'cuenca',
        'istmo',
        'mixteca',
        'sierra-norte',
        'sierra-sur',
        'valles-centrales'
    ]

    def __init__(self):
        super().__init__()
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        self.create_urls(self.url_gen, self.sections, list(range(1, self.n)))

    def url_gen(self, section, page):
        return self.url_stem + section + "/page/" + str(page) + "/"

    def parse_mason_jar(self, post, out):
        post_title = post.find("div", {"class": "post-title"})
        link = post_title.find("a")
        out["url"] = link.get("href")
        out["headline"] = link.text
        out["url_hash"] = url_hash(out["url"])
        return out

    def parse(self, response):
        soup, out = super(ImparcialOaxacaListingsSpider, self).parse(response)
        section = response.url.split("/")[3]
        out["section"] = section
        masonry_box = soup.find("div", {"class": "masonry-box"})
        article_box = soup.find("div", {"class": "article-box"})
        if masonry_box is not None:
            news_posts = masonry_box.find_all("div", {"class": "news-post"})
            for post in news_posts:
                out = self.parse_mason_jar(post, out)
                yield out
        elif article_box is not None:
            news_posts = article_box.find_all("div", {"class": "news-post"})
            for post in news_posts:
                link = post.find("div", {"class": "post-content"}).find("a")
                out["url"] = link.get("href")
                out["headline"] = link.text
                out["url_hash"] = url_hash(out["url"])
                yield out


class ImparcialOaxacaArticleSpider(scrapy.Spider):
    name = 'imparcial_oaxaca_articles'
    colnames = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        self.urls = list(get_urls("hard_keyed_listing_io.csv"))[1:]
        print("CREATED URLS: " + self.urls[0])

    def parse(self, response):
        out = {}
        soup = bs4.BeautifulSoup(response.text)
        content = soup.find(id="content")
        paragraphs = content.find_all("p")
        paragraphs = [p.text for p in paragraphs]
        out["paragraphs"] = paragraphs
        out["url"] = response.url
        hash = hashlib.sha224(response.url.encode("utf-8")).hexdigest()
        out["url_hash"] = hash
        yield out

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)
