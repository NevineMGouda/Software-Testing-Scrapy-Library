# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/lat  est/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    year = scrapy.Field()
    price = scrapy.Field()

class StudentItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()