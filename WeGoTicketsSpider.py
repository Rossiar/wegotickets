from scrapy import Spider
from scrapy import Request
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


class WeGoTicketsSpider(Spider):
    name = 'wegotickets'
    start_urls = ['http://www.wegottickets.com/searchresults/page/1/all']

    def parse(self, response):
        """Accesses the page at start_urls and parses each event link,
        makes a new request to the event link and uses parse_concert
        to render into JSON.
        """
        for href in response.css('a.event_link::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield Request(full_url, callback=self.parse_concert)

    def parse_concert(self, response):
        """Parses an event page,
        extracting data from the HTML response
        using CSS
        """
        yield {
            'title': response.css('.event-information h1::text').extract()[0],
            'location': response.css('.venue-details h2::text').extract()[0],
            'time': response.css('.venue-details h4::text').extract()[0],
        }


timestamp = '{:%Y%m%dT%H%M%S}'.format(datetime.now())

settings = Settings()
settings.overrides['SPIDER_MODULES'] = 'WeGoTicketsSpider'
settings.overrides['FEED_FORMAT'] = 'json'
settings.overrides['FEED_URI'] = timestamp + 'events.json'

process = CrawlerProcess(settings)
process.crawl(WeGoTicketsSpider)
process.start()