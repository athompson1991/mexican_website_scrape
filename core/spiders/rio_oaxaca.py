from core.spiders.core_spiders import ListingsSpider, ArticleSpider


class RioOaxacaListingsSpider(ListingsSpider):
    name = "rio_oaxaca_listings"
    url_stem = "https://www.rioaxaca.com"


    def __init__(self):
        super().__init__()
        self.create_urls(self.url_gen, self.sections, list(self.page_range))

    def url_gen(self, section, page):
        return self.url_stem + "/category/" + section + "/page/" + str(page)

    def parse(self, response):
        pass

class RioOaxacaArticleSpider(ArticleSpider):

    def parse(self, response):
        pass
