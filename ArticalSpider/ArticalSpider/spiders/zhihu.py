# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time
from scrapy.selector import Selector
from scrapy.http import HtmlResponse


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
         print(response)
    # def start_requests(self):
    #     # return [scrapy.Request("https://www.zhihu.com/signup", callback=self.parse)]
    #     driver = webdriver.Firefox()
    #     driver.get('https://www.zhihu.com/signup')
    #     time.sleep(5)
    #     driver.find_element_by_css_selector("div.SignContainer-switch > span").click()
    #     driver.find_element_by_css_selector("input[name='username']").send_keys('17839902249')
    #     time.sleep(3)
    #     driver.find_element_by_css_selector("input[name='password']").send_keys('huanying123321')
    #     time.sleep(5)
    #     driver.find_element_by_css_selector("div.Login-content > form > button").click()
    #     time.sleep(15)
    #     driver.get_cookies()
    #     driver.get('https://www.zhihu.com/')
    #     recmons = driver.find_elements_by_css_selector(".Topstory-recommend > div")
    #
    #     for reco in recmons:
    #
    #         print(reco)
    #         time.sleep(3)
