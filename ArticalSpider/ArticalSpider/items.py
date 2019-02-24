# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.loader import ItemLoader
import scrapy
from w3lib.html import remove_tags

class ArticalspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title_name = scrapy.Field()
    pub_date = scrapy.Field()
    prave_num = scrapy.Field()
    fav_nums = scrapy.Field()
    comment_num = scrapy.Field()
    tags = scrapy.Field()
    from_image_url = scrapy.Field()
    from_image_path = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()

#
# class LagoujobItemLoader(ItemLoader):
#
#     default_output_processor = TakeFirst()

class LagouspiderItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field()
    work_year = scrapy.Field()
    degree_need = scrapy.Field()
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field()
    crawl_time = scrapy.Field()


