# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 列表数据字段
class ColumnItem(scrapy.Item):
    topic = scrapy.Field()
    id = scrapy.Field()
    img_url = scrapy.Field()
    detail_url = scrapy.Field()

    title = scrapy.Field()
    abstract = scrapy.Field()
    author = scrapy.Field()
    author_icon = scrapy.Field()
    comments = scrapy.Field()
    likes = scrapy.Field()

    pass


# 文章数据字段
class ArticleItem(scrapy.Item):
    id = scrapy.Field()
    topic = scrapy.Field()
    title = scrapy.Field()

    abstract = scrapy.Field()

    pass
