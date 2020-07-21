from core.spiders.core_spiders import ListingsSpider, ArticleSpider
from core.utils import url_hash


class NssOaxacaListingsSpider(ListingsSpider):
    name = "nss_oaxaca_listings"
    url_stem = "https://www.nssoaxaca.com/"

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
            out["url_hash"] = url_hash(out["url"])
            out["publish_date"] = "-".join(out["url"].split("/")[3:6])
            out["headline"] = post.find("h2").text
            yield out


class NssOaxacaArticleSpider(ArticleSpider):
    name = "nss_oaxaca_articles"

    def parse(self, response):
        soup, out = super().parse(response)
        article = soup.find("article")
        post_content = article.find("div", {"class": "post-content"})
        paragraphs = post_content.find_all("p")
        paragraphs = [p.text for p in paragraphs if p.text != '']
        out["headline"] = article.find("h1").text
        out["paragraphs"] = paragraphs
        yield out
