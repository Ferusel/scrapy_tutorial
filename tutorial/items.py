# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class QuoteItem(scrapy.Item):
    quote_content = Field()
    tags = Field()
    author_name = Field()
    author_birthday = Field()
    author_bornlocation = Field()
    author_bio = Field()
