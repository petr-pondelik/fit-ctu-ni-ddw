import scrapy
from typing import List

from scrapy import Selector


class Article:

    title: str
    tags: List[str]
    content: str

    def __init__(self, title: str, tags: List[str]):
        self.title = title
        self.tags = tags
        self.content = ''

    def serialize(self):
        return {
            'title': self.title,
            'tags': self.tags,
            'content': self.content
        }


class ArticleParser:

    @staticmethod
    def parse(articleSrc: Selector) -> Article:
        print('ArticleParser')
        title: str = articleSrc.css('h1.article-header--title::text').extract_first()
        print(title)
        tags: List = articleSrc.css('li.meta-box--tags a::text').extract()
        print(tags)
        return Article(title, tags)


class RemoteJobsSpider(scrapy.Spider):

    name = 'RemoteJobsSpider'
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

