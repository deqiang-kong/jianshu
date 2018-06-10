# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time
import random
from selenium import webdriver
from scrapy.http.response.html import HtmlResponse

from jianshu.spiders.jianshu import topics


class UserAgentDownloadMiddleware(object):
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
        "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
        "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
        "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
        "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
        "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
        "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3",
    ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = user_agent


# Selenium 动态网页爬去中间件
class SeleniumDownloadMiddleware(object):
    def __init__(self):
        # chromedriver文件路径
        driver_path = r"/Users/kaipai/Desktop/Tools/chromedriver"
        self.driver = webdriver.Chrome(executable_path=driver_path)

    # 判断请求列表数据
    def isTopic(self, url):
        topic = False
        for key in topics:
            if url.find(key) > 0:
                return True
        return topic

    def process_request(self, request, spider):
        self.driver.get(request.url)
        index = 0
        # 加载页数，便于测试，不加载太多页
        count = 2
        flag = self.isTopic(str(request.url))
        try:
            # 请求列表数据时，加载指定页数
            while flag:
                # 执行js滑动到屏幕底部
                self.driver.execute_script("""   
                           (function () {   
                               var y = document.body.scrollHeight;   
                               window.scroll(0, y);   
                           })();   
                           """)

                if index > count:
                    break
                index = index + 1
                time.sleep(3)
        except:
            pass

        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=source, request=request, encoding='utf-8')
        return response

    # def scroll(driver):
    #     driver.execute_script("""
    #         (function () {
    #             var y = document.body.scrollTop;
    #             var step = 100;
    #             window.scroll(0, y);
    #
    #             function f() {
    #                 if (y < document.body.scrollHeight) {
    #                     y += step;
    #                     window.scroll(0, y);
    #                     setTimeout(f, 50);
    #                 }
    #                 else {
    #                     window.scroll(0, y);
    #                     document.title += "scroll-done";
    #                 }
    #             }
    #
    #             setTimeout(f, 1000);
    #         })();
    #         """)
