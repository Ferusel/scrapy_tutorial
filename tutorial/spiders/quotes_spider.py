import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        self.logger.info("hello this is my first spider")
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'text': quote.xpath('.//span[@class="text"]/text()').get(),
                'author': quote.xpath('.//span[2]/small[@class="author"]/text()').get(),
                'tags': quote.xpath('.//div[@class="tags"]/a/text()').getall(),
            }

            author_url = quote.xpath('.//span[2]/a/@href').get()
            self.logger.info("Grabbing author URL: " + str(author_url))
            yield scrapy.Request(url=response.urljoin(author_url), callback=self.parse_author)

        next_page = response.xpath(
            '//ul[@class="pager"]/li[@class="next"]/a/@href').get()

        if next_page:
            url = response.urljoin(next_page)
            self.logger.info(url)
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_author(self, response):
        yield {
            'author_name': response.xpath('//h3[@class="author-title"]').get(),
            'author_birthday': response.xpath('//span[@class="author-born-date"]').get(),
            'author_bornlocation': response.xpath('//span[@class="author-born-location"]').get(),
            'author_bio': response.xpath('//div[@class="author-description"]').get()
        }
