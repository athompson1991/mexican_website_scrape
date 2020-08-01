from core.spiders.core_spiders import ListingsSpider, ArticleSpider


class OaxacaUniversalListingsSpider(ListingsSpider):
    name = "oaxaca_universal_listings"
    url_stem = "https://oaxaca.eluniversal.com.mx/"

    def __init__(self):
        super(OaxacaUniversalListingsSpider, self).__init__()
        self.create_urls(self.url_gen, self.sections, self.page_range)

    def url_gen(self, section, page):
        return self.url_stem + "secciones/" + section + "?page=" + str(page)

    def parse(self, response):
        soup, out = super(OaxacaUniversalListingsSpider, self).parse(response)
        out["section"] = response.url.split("/")[-1].split("?")[0]
        main = soup.find("div", {"class": "grid-15"})
        views = main.find_all("div", {"class": "views-row"})
        for view in views:
            out["url"] = self.url_stem + view.find("a").get("href")
            div = view.find("div", {"class": "views-field-title"})
            out["headline"] = div.text.strip()
            div = view.find("div", {"class": "views-field-created"})
            out["publish_date"] = div.text.strip()
            out["url_hash"] = self.url_hash(out["url"])
            yield out


class OaxacaUniversalArticleSpider(ArticleSpider):
    name = "oaxaca_universal_articles"

    def parse(self, response):
        soup, out = super().parse(response)
        apertura = soup.find("div", id="apertura")
        out["headline"] = apertura.find("h1").text
        paragraphs = apertura.find_all("p")
        paragraphs = [p.text for p in paragraphs]
        out["paragraphs"] = paragraphs
        yield out
