# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SmartdbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    accession_number = scrapy.Field()
    name = scrapy.Field()
    species = scrapy.Field()
    url = scrapy.Field()

    SQ = scrapy.Field()
    NA = scrapy.Field()

