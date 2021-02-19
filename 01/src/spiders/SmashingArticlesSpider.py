import scrapy

from entities.Article import Article
from parsers.ArticleParser import ArticleParser


class SmashingArticlesSpider(scrapy.Spider):

    name = 'SmashingArticlesSpider'
    start_urls = ['https://www.smashingmagazine.com/articles/']
    allowed_domains = ['smashingmagazine.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': False,
        'CLOSESPIDER_PAGECOUNT': 10,
        'LOG_ENABLED': False
    }

    def parse(self, response):
        for articleSrc in response.css('article.article'):
            article: Article = ArticleParser.parse(articleSrc)
            yield article.serialize()

        for nextPage in response.css('h1.article--post__title > a ::attr(href), li.pagination__next > a ::attr(href)'):
            yield scrapy.Request(response.urljoin(nextPage.extract()), callback=self.parse)
