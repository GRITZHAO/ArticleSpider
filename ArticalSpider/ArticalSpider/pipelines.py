# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
from ArticalSpider.settings import MYSQL_HOST,MYSQL_DBNAME,MYSQL_USER,MYSQL_PASSWORD
import codecs
import json
import pymysql
import pymongo

class ArticalspiderPipeline(object):
    def process_item(self, item, spider):
        return item

# 保存图片地址


class ArticalImagePipline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
        item['from_image_path'] = image_file_path
        return item

# 自定义json文件导出


class JsonWithEncodingPipeline(object):
    def __init__(self):
        # 打开文件
        self.file = codecs.open('artical.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 转化成字符串
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_close(self,spider):
        self.file.close()

# 调用scrapy提供的json—exporter导出文件


class JsonExproterPipleline(object):
    def __init__(self):
        self.file = open('articleexporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# 同步
class MYsqlpipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='702115', db='article', charset='utf8')
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        self.cursor.executemany("insert into articlespider(title,create_date)values(%s %s)",[item['title_name'], item['pub_date']])
        # self.cursor.execute(insert_sql, (item["title_name"], item["url"], item["pub_date"], item["fav_nums"]))
        self.conn.commit()


# 异步
class MysqlTwistedpipline(object):

    @classmethod
    def from_settings(cls, settings):
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        passwd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DBNAME']


# import pymongo
# 保存在数据库中
class MongolagouPipeline(object):

    collection_name = 'lagou_job'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
