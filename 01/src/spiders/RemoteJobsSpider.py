import scrapy
from typing import List

from scrapy import Selector


class Job:

    title: str
    tags: List[str]
    content: str

    def __init__(self, title: str):
        self.title = title
        self.tags = []
        self.content = ''

    def serialize(self):
        return {
            'title': self.title,
            'tags': self.tags,
            'content': self.content
        }


class JobParser:

    @staticmethod
    def parse(jobPost: Selector) -> Job:
        print(input)
        print('JobParser')
        title: str = jobPost.css('h1::text').extract_first()
        return Job(title)


class RemoteJobsSpider(scrapy.Spider):

    name = 'RemoteJobsSpider'
    start_urls = ['https://www.sitepoint.com/jobs/']
    allowed_domains = ['sitepoint.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': False,
        # 'DEPTH_LIMIT': 5,
        # 'CLOSESPIDER_PAGECOUNT': 2
    }

    def parse(self, response):
        for jobPost in response.css('#jobPost-module--post_container--2T7O3'):
            job: Job = JobParser.parse(jobPost)
            yield job.serialize()
            # yield {
            #     'title': jobPost.css('h1::text').extract_first()
            # }

        for nextPage in response.css('.JobListStyles-sc-1bgcgnh-0 a ::attr(href), #jobPost-module--post_container--2T7O3 a ::attr(href)'):
            yield scrapy.Request(response.urljoin(nextPage.extract()), callback=self.parse)

    def test(self):
        print('TEST')
