# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticalSpider.items import LagouspiderItem
from ArticalSpider.utils.comment import get_md5
from datetime import datetime


class LaogouSpider(CrawlSpider):
    name = 'laogou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    rules = (
         # Rule(LinkExtractor(allow=r'gongsi/\d+.html'), callback='parse_item', follow=True),

        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item_load = LagouspiderItem()
        item_load['title'] = response.xpath("//div[@class='job-name']/span/text()").get()
        item_load['url'] = response.url
        item_load['url_object_id'] = get_md5(response.url)
        item_load['salary'] = response.xpath("//dd/p/span[1]/text()").get()
        item_load['job_city'] = response.xpath('//dd/p/span[2]/text()').get().replace("/", '')
        item_load['work_year'] = response.xpath('//dd/p/span[3]/text()').get().replace("/", '')
        item_load['degree_need'] = response.xpath('//dd/p/span[4]/text()').get().replace("/", '')
        item_load['job_type'] = response.xpath('//dd/p/span[5]/text()').get()
        item_load['publish_time'] = response.xpath('//dd/p[2]/text()').get().split()[0]
        item_load['job_advantage'] = response.xpath("//dd[@class='job-advantage']/p/text()").get()
        item_load['job_desc'] = response.xpath("//div[@class='job-detail']/p//text()").getall()
        item_load['job_addr'] = response.xpath("//div[@class='work_addr']/a/text()").getall()[:-1]
        item_load['company_name'] = response.xpath("//em[@class='fl-cn']/text()").get().split()[0]
        item_load['company_url'] = response.xpath("//ul[@class='c_feature']/li[4]/a/@href").get()
        item_load['tags'] = response.xpath("//dd[@class='job_request']//li/text()").get()
        item_load['crawl_time'] = datetime.now()
        yield item_load
