import json

from scrapy.crawler import CrawlerProcess

from spiders.SmashingArticlesSpider import SmashingArticlesSpider

if __name__ == '__main__':

    process = CrawlerProcess({
        "FEEDS": {
            "smashing_articles.json": {"format": "json"}
        }
    })
    process.crawl(SmashingArticlesSpider)
    process.start()

    print('FINISHED')
    jsonFile = open('smashing_articles.json')
    print(json.load(jsonFile))
