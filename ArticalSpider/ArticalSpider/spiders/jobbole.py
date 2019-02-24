# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticalSpider.items import ArticalspiderItem
from ArticalSpider.utils.comment import get_md5
from scrapy.loader import ItemLoader
# from ArticalSpider.settings import user_agent_list

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        # 解析文章中的url
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        # 获取图片和文章url
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first()
            post_url = post_node.css("::attr(href)").extract_first()
            yield Request(url=parse.urljoin(response.url, post_url), meta={"from_image_url": image_url}, callback=self.parse_detail)

        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        article_item = ArticalspiderItem()
        from_image_url = response.meta.get("from_image_url", '')
        title_name = response.css(".entry-header h1::text").extract()[0]
        pub_date = response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip().replace(" ·","")
        prave_num = response.css(".post-adds h10::text").extract()[0]
        match_re1 = re.match(r".*?(\d+).*", prave_num)
        if match_re1:
            prave_num = match_re1.group(1)
        else:
            prave_num = 0
        fav_nums = response.css("span.btn-bluet-bigger::text").extract()[0]
        match_re1 = re.match(r".*?(\d+).*", fav_nums)
        if match_re1:
            fav_nums = match_re1.group(1)
        else:
            fav_nums = 0
        comment_num = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re2 = re.match(r".*?(\d+).*", comment_num)
        if match_re2:
            comment_num = match_re2.group(1)
        else:
            comment_num = 0

        tags = response.css("p.entry-meta-hide-on-mobile a::text").extract()[0]
        # 以数组的形式
        article_item["from_image_url"] = [from_image_url]
        article_item['title_name'] = title_name
        article_item["pub_date"] = pub_date
        article_item["fav_nums"] = fav_nums
        article_item["comment_num"] = comment_num
        article_item["tags"] = tags
        article_item["prave_num"] = prave_num
        article_item["url"] = response.url
        article_item['url_object_id'] = get_md5(response.url)

        # 通过item——loader加载item
        #item_load = ItemLoader(item=ArticalspiderItem(), response=response)

        yield article_item
