from core.spiders.core_spiders import ListingsSpider, ArticleSpider
from core.utils import url_hash


class ImparcialOaxacaListingsSpider(ListingsSpider):
    name = "imparcial_oaxaca_listings"
    url_stem = "https://imparcialoaxaca.mx/"

    def __init__(self):
        super().__init__()
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


class ImparcialOaxacaArticleSpider(ArticleSpider):
    name = 'imparcial_oaxaca_articles'

    def parse(self, response):
        soup, out = super().parse(response)
        content = soup.find(id="content")
        paragraphs = content.find_all("p")
        paragraphs = [p.text for p in paragraphs]
        out["paragraphs"] = paragraphs
        out["url"] = response.url
        out["url_hash"] = url_hash(out["url"])
        yield out
