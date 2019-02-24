import requests
from scrapy.selector import Selector
import MySQLdb
import time
conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='702115', db='article', charset='utf8',)
course = conn.cursor()


def crawl_ips():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    # 代理服务器
    proxyHost = "http-cla.abuyun.com"
    proxyPort = "9030"

    # 代理隧道验证信息
    proxyUser = "H4C123792U8LI85C"
    proxyPass = "C1BEE9D4DB823359"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }

    for i in range(1):
        result = requests.get('https://www.xicidaili.com/nn/'.format(i), headers=headers,proxies=proxies)
        print(result.status_code)
        print(result.text)
        secetor = Selector(text=result.text)
        ip_infos = secetor.xpath("//table[@id='ip_list']//tr[@class='odd']")
        ip_list = []
        for ip_info in ip_infos:
            seconds = float(ip_info.xpath("./td/div/@title").get().split("秒")[0])
            print(seconds)
            ip_detial = ip_info.xpath(".//td/text()").getall()
            print(ip_detial)
            ip = ip_detial[0]
            port = ip_detial[1]
            type = ip_detial[5]
            ip_list.append((ip, port, type, seconds))
        print(ip_list)
        for ip_lt in ip_list:
            course.execute("insert ip_proxy(ip,port,speed,proxy_type) VALUES ('{0}','{1}',{2},'{3}')".format(ip_lt[0], ip_lt[1],ip_lt[3],ip_lt[2]))
            conn.commit()
        time.sleep(5)

# 从数据库在取ip


class GetIp(object):
    def get_random_ip(self):
        random_sql = """
        SELECT ip,port FROM `ip_proxy`
        ORDER BY RAND()
        LIMIT 1
        """
        resu = course.execute(random_sql)
        for ip_info in course.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            judge_result = self.judge_ip(ip, port)
            if judge_result:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()

    def delete_ip(self, ip):
        # 从数据库中删除无效的ip
        delete_sql = """
        delete from ip_proxy where ip='{0}'
        """.format(ip)
        course.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        http_url = 'http://www.baidu.com'
        # 构建ip并且验证
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict ={
                'http': proxy_url
            }
            requests.get(http_url,proxies=proxy_dict)
            return True
        except Exception as e:
            print(e)
            self.delete_ip(ip)
            return False
        else:
            code = respon.status_code
            if code >= 200 and code <300:
                print('valuable ip')
                return True
            else:
                print('invalueable ip')
                self.delete_ip(ip)
                return False


if __name__ == '__main__':

    get_ip = GetIp()
    print(get_ip.get_random_ip())










