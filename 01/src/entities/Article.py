from typing import List


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
        return {
            'title': self.title,
            'author': self.author,
            'published': self.published,
            'length': self.length,
            'tags': self.tags,
            'summary': self.summary
        }
