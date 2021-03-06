import datetime

from core.spiders.core_spiders import ListingsSpider, ArticleSpider


class RioOaxacaListingsSpider(ListingsSpider):
    name = "rio_oaxaca_listings"
    url_stem = "https://www.rioaxaca.com"

    def __init__(self):
        super().__init__()
        self.create_urls(self.url_gen, self.sections, list(self.page_range))

    def url_gen(self, section, page):
        main = self.url_stem + "/category/"
        if section.split("-")[1] == "general":
            return main + "regiones/" + section + "/page/" + str(page) + "/"
        else:
            return main + section + "/page/" + str(page) + "/"

    def parse(self, response):
        soup, out = super().parse(response)
        out["section"] = response.url.split("/")[-4]
        main_content = soup.find("div", {"class": "td-ss-main-content"})
        item_details = main_content.find_all("div", {"class": "item-details"})
        for item in item_details:
            out["headline"] = item.find("h3").text
            out["url"] = item.find("a").get("href")
            out["url_hash"] = self.url_hash(out["url"])
            dt_str = item.find("time").get("datetime")
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S+00:00")
            out["publish_date"] = dt.strftime("%Y-%m-%d")
            out["publish_time"] = dt.strftime("%H:%M")
            yield out


class RioOaxacaArticleSpider(ArticleSpider):
    name = "rio_oaxaca_articles"

    def parse(self, response):
        soup, out = super(RioOaxacaArticleSpider, self).parse(response)
        post_content = soup.find("div", {"class": "td-post-content"})
        paragraphs = post_content.find_all("p")
        paragraphs = [p.text for p in paragraphs]
        out["paragraphs"] = paragraphs
        header = soup.find("header", {"class": "td-post-title"})
        out["headline"] = header.find("h1").text
        yield out
