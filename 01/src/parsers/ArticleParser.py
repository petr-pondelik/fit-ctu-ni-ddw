from typing import List
from scrapy import Selector

from entities.Article import Article


class ArticleParser:

    @staticmethod
    def parse(articleSrc: Selector) -> Article:
        print('ArticleParser')

        title: str = articleSrc.css('h1.article-header--title::text').extract_first()
        print(title)

        author: str = articleSrc.css('.bio-image-image::attr(alt)').extract_first()
        print(author)

        published: str = articleSrc.css('.article-header--date::attr(datetime)').extract_first()
        print(published)

        length: str = articleSrc.css('.meta-box--published::text').extract_first()
        print(length)

        tags: List[str] = articleSrc.css('li.meta-box--tags a::text').extract()
        print(tags)

        summary: str = articleSrc.css('.article__summary::text').extract_first()
        print(summary)

        # content: List[str] = articleSrc.css('#article__content > div > p::text').extract
        # print(content)

        return Article(title, author, published, length, tags, summary)
