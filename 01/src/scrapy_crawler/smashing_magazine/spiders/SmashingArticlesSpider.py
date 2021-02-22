from typing import List

import scrapy
from scrapy import Selector


# Class representing article
class Article:

    title: str
    author: str
    published: str
    length: str
    tags: List[str]
    summary: str

    def __init__(
            self,
            title: str, author: str, published: str, length: str,
            tags: List[str], summary: str
    ):
        self.title = title
        self.author = author
        self.published = published
        self.length = length
        self.tags = tags
        self.summary = summary

    def serialize(self):
        # Return article for serializing
        return {
            'title': self.title,
            'author': self.author,
            'published': self.published,
            'length': self.length,
            'tags': self.tags,
            'summary': self.summary
        }


class ArticleParser:

    @staticmethod
    def parse(articleSrc: Selector) -> Article:
        # Parse the given element Selector into Article instance
        title: str = articleSrc.css('h1.article-header--title::text').extract_first()
        author: str = articleSrc.css('.bio-image-image::attr(alt)').extract_first()
        published: str = articleSrc.css('.article-header--date::attr(datetime)').extract_first()
        length: str = articleSrc.css('.meta-box--published::text').extract_first()
        tags: List[str] = articleSrc.css('li.meta-box--tags a::text').extract()
        summary: str = articleSrc.css('.article__summary::text').extract_first()
        return Article(title, author, published, length, tags, summary)


class SmashingArticlesSpider(scrapy.Spider):

    # Set spider name and seed URL
    # Limit the crawling to the domain
    name = 'SmashingArticlesSpider'
    start_urls = ['https://www.smashingmagazine.com/articles/']
    allowed_domains = ['smashingmagazine.com']

    # Customer spider settings
    custom_settings = {
        'USER_AGENT': 'DDW',
        # 'CLOSESPIDER_PAGECOUNT': 20,
        'DEPTH_LIMIT': 30,
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': False,
        'LOG_ENABLED': False,
        "FEEDS": {
            "./../../results/smashing_articles.json": {"format": "json"}
        }
    }

    def parse(self, response):
        # Select articles in HTML response
        for articleSrc in response.css('article.article'):
            article: Article = ArticleParser.parse(articleSrc)
            # Get article for serialization
            yield article.serialize()

        # Crawl through the links
        for nextPage in response.css('h1.article--post__title > a ::attr(href), li.pagination__next > a ::attr(href)'):
            yield scrapy.Request(response.urljoin(nextPage.extract()), callback=self.parse)
