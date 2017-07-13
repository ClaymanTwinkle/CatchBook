#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib

import scrapy
from scrapy import Request
from scrapy.selector import HtmlXPathSelector


# scrapy crawl quanben.co --nolog
class QuanbenSpider(scrapy.spiders.Spider):
    name = "quanben.co"
    allowed_domains = ["www.quanben.co"]
    start_urls = [
        "http://www.quanben.co/top/allvisit_1.html",
    ]

    url_set = set()

    def parse(self, response):
        # print(response, type(response))
        # from scrapy.http.response.html import HtmlResponse
        # print(response.body_as_unicode())
        md5_obj = hashlib.md5()
        md5_obj.update(response.url)
        md5_url = md5_obj.hexdigest()
        if md5_url in self.url_set:
            pass
        else:
            # print response.url

            self.url_set.add(md5_url)
            hxs = HtmlXPathSelector(response)

            if response.url.startswith('http://www.quanben.co/info/'):
                book_name = hxs.select('//div[@id="content"]/h1/text()')[0].extract()
                book_pic = hxs.select('//div[@class="novel_img"]/img/@src')[0].extract()
                book_author = hxs.select('//ul[@class="novel_msg"]/li[1]/a/text()')[0].extract()
                book_create_time = hxs.select('//ul[@class="novel_msg"]/li[2]/text()')[0].extract().replace(u"驻站时间：",
                                                                                                            u"")
                book_status = hxs.select('//ul[@class="novel_msg"]/li[3]/em/text()')[0].extract()
                book_type = hxs.select('//ul[@class="novel_msg"]/li[4]/text()')[0].extract().replace(u'类型：', u"")
                book_words_count = hxs.select('//ul[@class="novel_msg"]/li[5]/text()')[0].extract().replace(u'总字数：',u"")
                book_description = "\n".join(hxs.select('//li[@id="description1"]/text()').extract())

                print book_name
                print book_pic
                print book_author
                print book_create_time
                print book_status
                print book_type
                print book_words_count
                print book_description

            current_page_urls = hxs.select('//a/@href').extract()
            for url in current_page_urls:
                if url.startswith('http://www.quanben.co'):
                    url_ab = url
                    yield Request(url_ab, callback=self.parse)
                    # current_url = response.url  # 爬取时请求的url
                    # body = response.body  # 返回的html
                    # unicode_body = response.body_as_unicode()  # 返回的html unicode编码
                    # print body
