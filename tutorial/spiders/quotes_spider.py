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
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.add_xpath('quote_content', './/span[@class="text"]/text()')
            loader.add_xpath(
                'tags', './/div[@class="tags"]/a/text()')
            quote_item = loader.load_item()

            author_url = quote.xpath('.//span[2]/a/@href').get()
            self.logger.info("Grabbing author URL: " + str(author_url))
            yield scrapy.Request(url=response.urljoin(author_url), callback=self.parse_author, meta={'quote_item': quote_item})

        next_page = response.xpath(
            '//ul[@class="pager"]/li[@class="next"]/a/@href').get()

        if next_page:
            url = response.urljoin(next_page)
            self.logger.info(url)
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item=quote_item, response=response)
        loader.add_xpath("author_name", '//h3[@class="author-title"]/text()')
        loader.add_xpath("author_birthday",
                         '//span[@class="author-born-date"]/text()')
        loader.add_xpath("author_bornlocation",
                         '//span[@class="author-born-location"]/text()')
        loader.add_xpath(
            "author_bio", '//div[@class="author-description"]/text()')
        yield loader.load_item()
