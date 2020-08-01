import datetime
import hashlib

from core.spiders.core_spiders import ListingsSpider, ArticleSpider


class OaxacaQuadratinListingsSpider(ListingsSpider):
    name = 'oaxaca_quadratin_listings'
    url_stem = 'https://oaxaca.quadratin.com.mx/'

    def __init__(self):
        super().__init__()
        self.create_urls(self.url_gen, self.sections, self.page_range)

    def url_gen(self, section, page):
        return self.url_stem + section + '/page/' + str(page) + '/'

    def parse(self, response):
        soup, out = super(OaxacaQuadratinListingsSpider, self).parse(response)
        out["section"] = response.url.split("/")[3]
        divs = soup.find_all("div", {"class": "col-lg-6"})
        for div in divs:
            box_container = div.find_all("div", {"class": "box-container"})[0]
            box1 = box_container.find_all("div", {"class": "box1"})[0]
            box2 = box_container.find_all("div", {"class": "box2"})[0]
            out["url"] = box2.find("a", href=True).get("href")
            out["url_hash"] = self.url_hash(out["url"])
            out["headline"] = box1.find("h4").text.strip()
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
        out["headline"] = info.find("h1").text.replace("\n", "").strip()
        yield out
