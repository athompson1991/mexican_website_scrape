import bs4
import scrapy
import datetime
import locale
import hashlib

from core import pipelines


def parse_article(response_text):
    soup = bs4.BeautifulSoup(response_text)
    return soup.find_all("div", {"class": "post-content"})


class OaxacaQuadratinSpider(scrapy.Spider):

    n = 100
    pipeline = {pipelines.CSVPipeline}

    name = 'oaxaca_quadratin'
    url_stem = 'https://oaxaca.quadratin.com.mx/'
    colnames = [
        "url",
        "url_hash",
        "scraped_from",
        "section",
        "headline",
        "publish_time",
        "publish_date"
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        self.sections = ['principal', 'ciudad', 'regiones', 'comunicados',
                         'politicas', 'gobierno', 'justicia', 'opinion',
                         'cultura', 'deportes', 'Estados', 'entretenimiento',
                         'versiones-estenograficas', ]
        self.pages = [i for i in range(1, self.n)]
        self.urls = []
        for page in self.pages:
            for section in self.sections:
                new_url = self.url_stem + section + '/page/' + str(page) + '/'
                self.urls.append(new_url)

    def parse(self, response):
        soup = bs4.BeautifulSoup(response.text)
        divs = soup.find_all("div", {"class": "col-lg-6"})
        for div in divs:
            out = {"scraped_from": response.url,
                   "section": response.url.split("/")[3]}
            box_container = div.find_all("div", {"class": "box-container"})[0]
            box1 = box_container.find_all("div", {"class": "box1"})[0]
            box2 = box_container.find_all("div", {"class": "box2"})[0]
            url = box2.find("a", href=True).get("href")
            url_hash = hashlib.sha224(url.encode("utf-8"))
            out["url"] = url
            out["url_hash"] = url_hash
            out["headline"] = box1.find("h4").text
            timestamp = box1.find("div", {"class": "date-hour"}).text
            timestamp = timestamp.replace("\n", "").strip()
            d = datetime.datetime.strptime(timestamp, "%H:%M %d %b %Y")
            out["publish_date"] = d.strftime("%Y-%m-%d")
            out["publish_time"] = d.strftime("%H:%M")
            yield out

    def start_requests(self):
        for url in self.urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)
