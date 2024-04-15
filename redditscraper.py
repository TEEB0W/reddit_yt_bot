import scrapy
from config import SUBREDDIT_PAGE_URL
from config import MEDIA_URLS_PATH
from config import API_KEY
from scrapy.crawler import CrawlerProcess
#TO DO: change xpath; works only sometimes
#TO DO: scrape photos; easy low priorty
class RedditspiderSpider(scrapy.Spider):
    name = "redditspider"
    allowed_domains = ["old.reddit.com"]
    start_urls = [SUBREDDIT_PAGE_URL]

    def parse(self, response):
        media_links = response.xpath("//a[@data-event-action='thumbnail']/@href")

        for link in media_links:
            # count += 1
            yield {
                'url': link.get()
            }
            # if count == 4:
            #     break

def main():
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                MEDIA_URLS_PATH : {'format': 'csv', 'overwrite' : True},
            },
            "SCRAPEOPS_API_KEY" : API_KEY, # signup at https://scrapeops.io
            "SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT" : 'https://headers.scrapeops.io/v1/user-agents',
            "SCRAPEOPS_FAKE_USER_AGENT_ENABLED" : True,
            "SCRAPEOPS_NUM_RESULTS" : 5,
            "ROBOTSTXT_OBEY" : False,
            "COOKIES_ENABLED" : False,
            'DOWNLOADER_MIDDLEWARES' : {
                'middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 400,
                },
        }
    )

    process.crawl(RedditspiderSpider)
    process.start()

if __name__ == "__main__":
    main()