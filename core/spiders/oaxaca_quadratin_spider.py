import bs4
import scrapy
import datetime
import locale
import hashlib

from core import pipelines
from core.spiders.core_spiders import ListingsSpider, ArticleSpider
from core.utils import get_urls, url_hash


class OaxacaQuadratinListingsSpider(ListingsSpider):

    n = 100
    name = 'oaxaca_quadratin_listings'
    url_stem = 'https://oaxaca.quadratin.com.mx/'

    def __init__(self):
        super().__init__()
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        self.sections = [
            'principal',
            'ciudad',
            'regiones',
            'comunicados',
            'politicas',
            'gobierno',
            'justicia',
            'opinion',
            'cultura',
            'deportes',
            'Estados',
            'entretenimiento',
            'versiones-estenograficas',
        ]
        self.pages = [i for i in range(1, self.n)]
        self.urls = []
        for page in self.pages:
            for section in self.sections:
                new_url = self.url_stem + section + '/page/' + str(page) + '/'
                self.urls.append(new_url)

    def parse(self, response):

        soup = bs4.BeautifulSoup(response.text)
        out = {
            "scraped_from": response.url,
            "section": response.url.split("/")[3]
        }
        divs = soup.find_all("div", {"class": "col-lg-6"})
        for div in divs:
            box_container = div.find_all("div", {"class": "box-container"})[0]
            box1 = box_container.find_all("div", {"class": "box1"})[0]
            box2 = box_container.find_all("div", {"class": "box2"})[0]
            url = box2.find("a", href=True).get("href")
            url_hash = hashlib.sha224(url.encode("utf-8")).hexdigest()
            out["url"] = url
            out["url_hash"] = url_hash
            out["headline"] = box1.find("h4").text
            timestamp = box1.find("div", {"class": "date-hour"}).text
            timestamp = timestamp.replace("\n", "").strip()
            d = datetime.datetime.strptime(timestamp, "%H:%M %d %b %Y")
            out["publish_date"] = d.strftime("%Y-%m-%d")
            out["publish_time"] = d.strftime("%H:%M")
            yield out


class OaxacaQuadratinArticleSpider(ArticleSpider):

    name = 'oaxaca_quadratin_articles'

    def parse(self, response):
        soup, out = super(OaxacaQuadratinArticleSpider, self).parse(response)
        article = soup.find("div", {"class": "post-content"})
        info = soup.find("div", {"class": "single-post-info"})
        paragraphs = [p.text for p in article.find_all("p")]
        out["paragraphs"] = paragraphs
        out["url"] = response.url
        out["url_hash"] = url_hash(response.url)
        out["headline"] = info.find("h1").text.replace("\n", "").strip()
        yield out
