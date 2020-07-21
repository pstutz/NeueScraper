# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NeuescraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Kanton = scrapy.Field()
    Num = scrapy.Field()
    Kammer = scrapy.Field()
    EDatum = scrapy.Field()
    PDatum = scrapy.Field()
    Titel = scrapy.Field()
    Leitsatz = scrapy.Field()
    Rechtsgebiet = scrapy.Field()
    DocID = scrapy.Field()
    PDFUrl = scrapy.Field()
    HTMLUrl = scrapy.Field()
    PDFFile = scrapy.Field()
    HTML = scrapy.Field()
    Raw = scrapy.Field()

    # pass
    
