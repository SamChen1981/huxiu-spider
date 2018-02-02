#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc :
"""
from coolscrapy.items import HuxiuItem  # 导入自定义的Item类
import scrapy
import json

class HuxiuSpider(scrapy.Spider):
    # Spider名称，必须是唯一的
    name = "huxiu"
    allowed_domains = ["huxiu.com"]

    # 初始化下载链接URL
    start_urls = [
        "http://www.huxiu.com/index.php"
    ]

    # 用来解析下载后的Response对象，该对象也是这个方法的唯一参数。
    # 它负责解析返回页面数据并提取出相应的Item（返回Item对象），还有其他合法的链接URL（返回Request对象）
    def parse(self, response):
        for sel in response.xpath('//div[@class="mod-info-flow"]/div/div[@class="mob-ctt"]'):
            item = HuxiuItem()
            item['title'] = sel.xpath('h2/a/text()')[0].extract()
            item['link'] = sel.xpath('h2/a/@href')[0].extract()
            url = response.urljoin(item['link'])
            item['desc'] = sel.xpath('div[@class="mob-sub"]/text()')[0].extract()
            # print(item['title'],item['link'],item['desc'])
            yield scrapy.Request(url, callback=self.parse_article) #注册一个回调函数来解析新闻详情

    def parse_article(self, response):
        detail = response.xpath('//div[@class="article-wrap"]')

        item = HuxiuItem()
        item['title'] = detail.xpath('h1/text()')[0].extract().strip()
        item['link'] = response.url.strip()
        item['author'] = detail.xpath(
            'div[@class="article-author"]/span[@class="author-name"]/a/text()')[0].extract().strip()
        item['published'] = detail.xpath(
            'div[@class="article-author"]/div[@class="column-link-box"]/span/text()')[0].extract().strip()
        yield item