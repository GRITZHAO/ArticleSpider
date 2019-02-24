# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from tools.crawl_xici_ip import GetIp
from scrapy import signals
from fake_useragent import UserAgent
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class ArticalspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ArticalspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddlware(object):
    #随机更换ua
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent(verify_ssl=False)
        # 设置ua类型如ua.ie,ua.msie,等
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            # 一下表达式等同于self.ua.self.ua_type获取属性
            # self.ua.random或self.ua.ie
            return getattr(self.ua, self.ua_type)
        # 等同于key(User-Agent):values(get_ua())
        # print(get_ua())
        request.headers.setdefault("User-Agent", get_ua())
        # 配置文件在downloadmiddleware
        # 设置代理IP
        # request.meta["proxy"] = "http://113.122.169.23:9999"

# 设置动态随机ip


class RandomProxymiddleware(object):
    def process_request(self, request, spider):
        get_ip = GetIp()
        request.meta["proxy"] = get_ip.get_random_ip()


class SeleniumMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 5)

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        self.driver.get('https://www.zhihu.com/signup')
        try:
            input_tag = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.SignContainer-switch > span')))
            input_tag.click()
            input_num = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
            input_num.send_keys('17839902249')
            input_passwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
            input_passwd.send_keys('huanying123321')
            login_in = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.Login-content > form > button")))
            login_in.click()
            return HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8')

        except Exception as e:
            print(e)



