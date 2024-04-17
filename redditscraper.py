import scrapy
from config import SUBREDDIT_PAGE_URL
from config import MEDIA_URLS_PATH
from config import API_KEY
from config import page_limit
from scrapy.crawler import CrawlerProcess
#TO DO: change xpath; bugs out sometimes
#TO DO: scrape photos; easy low priorty
class RedditspiderSpider(scrapy.Spider):
    name = "redditspider"
    allowed_domains = ["old.reddit.com"]
    start_urls = [SUBREDDIT_PAGE_URL]
    

    def parse(self, response):   
        global page_limit   #used to count number of recursions
        media_links = response.xpath("//a[@data-event-action='thumbnail']/@href") #get all the links(from the thumbnails)
        
        for link in media_links:
            yield {
                'url': link.get() #get them one by one
            }

        page_limit -= 1
        next_page = response.xpath("//span[@class='next-button'][1]/a[1]/@href").get()  #get next page link
        if not page_limit == 0:     
            yield response.follow(next_page, callback= self.parse)  #recurse and for next page
        

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