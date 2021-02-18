import json

from scrapy.crawler import CrawlerProcess

from spiders.RemoteJobsSpider import RemoteJobsSpider

if __name__ == '__main__':

    process = CrawlerProcess({
        "FEEDS": {
            "jobs.json": {"format": "json"}
        }
    })
    process.crawl(RemoteJobsSpider)
    process.start()

    print('FINISHED')
    jsonFile = open('jobs.json')
    print(json.load(jsonFile))
