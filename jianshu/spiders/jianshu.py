# -*- coding: utf-8 -*-
import scrapy

from scrapy_splash import SplashRequest
from ..items import ColumnItem, ArticleItem

base_url = 'https://www.jianshu.com'
# 爬取的专题列表
topics = {'/c/NEt52a': '程序员',
          # '/c/V2CqjW': '@IT·互联网',
          # '/c/e7d2d4045b36': '历史',
          }


# 根据专题生产请求地址列表
def get_urls():
    urls = []
    for key in topics:
        url = base_url + key
        urls.append(url)

    return urls


#
# 简书全网爬取
class jianshuSpider(scrapy.Spider):
    name = 'js'
    allowed_domains = ['jianshu.com']

    start_urls = get_urls()

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 1, 'timeout': 5})
            yield SplashRequest(url, self.parse_detail, args={'wait': 1, 'timeout': 5})

    # 获取专题名称
    def get_topic(self, url):
        topic = ''
        for key in topics:
            if url.find(key) > 0:
                topic = topics[key]
                return topic

        return topic

    # 文章列表
    def parse(self, response):
        print("\n " + " parse---------------start")
        data_list = response.xpath(".//div[@id='list-container']/ul/li")
        # 获取专题
        topic = self.get_topic(str(response.urljoin))

        index = 0
        for bean in data_list:
            id = bean.xpath(".//@data-note-id").get()
            img_url = ''
            try:
                img_url = "https:" + bean.xpath(".//a[@class='wrap-img']/img/@src").get()
            except:
                pass
            detail_url = base_url + bean.xpath(".//a[@class='title']/@href").get()
            title = bean.xpath(".//a[@class='title']/text()").get()
            abstract = bean.xpath(".//p[@class='abstract']/text()").get().strip()

            author = bean.xpath(".//div[@class='meta']/a/text()").get()
            author_icon = base_url + bean.xpath(".//div[@class='meta']/a/@href").get()

            comments = bean.xpath(".//div[@class='meta']/a[2]/text()").getall()[-1:]
            comments = ''.join(comments).strip()
            likes = bean.xpath(".//div[@class='meta']/span/text()").get().strip()

            item = ColumnItem()
            item['topic'] = topic
            item['id'] = id
            item['img_url'] = img_url
            item['detail_url'] = detail_url
            item['title'] = title
            item['abstract'] = abstract
            item['author'] = author
            item['author_icon'] = author_icon
            item['comments'] = comments
            item['likes'] = likes
            index = index + 1
            # print(item)
            print(topic + str(index))
            # 传递给管道
            # yield item
            # 详情数据：追加爬取的RUL,交给调度器
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={"info": (id, topic, title)})

    index_detail = 0

    # 详情
    def parse_detail(self, response):
        id, topic, title = response.meta.get("info")
        print("\n" + str(self.index_detail) + title + " detail---------------start")

        self.index_detail = self.index_detail + 1
        article = response.xpath("//div[@class='article']").getall()
        # print(article)

        item = ArticleItem()
        item['id'] = id
        item['topic'] = topic
        item['title'] = title
        item['article'] = article

        yield item
