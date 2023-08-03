#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/19 9:56
@Author : xushaowei
@File : other_jlsjsxxw.py
@Desc :
@Software:PyCharm
"""
import logging
import time

# import pandas as pd
import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

from bid_scrapy_project.common.common import format_time


class GgzyjyNmgSpider(scrapy.Spider):
    name = "other_jlsjsxxw"
    start_urls = "http://www.jlsjsxxw.com/gcxx/004001/moreinfojyxx.html"
    website_name = '吉林省建设信息网'
    website_url = 'http://www.jlsjsxxw.com'
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list_page,
            dont_filter=True
        )

    def parse_list_page(self, response):
        nav_link = response.xpath('//ul[@class="wb-tree sidebar_nav"]//li')
        for url_min in nav_link:
            url_type = url_min.xpath('.//a/@href').get()
            text_type = url_min.xpath('.//a/text()').get()
            for page in range(1, 3):
                if '1' in str(page):
                    url = self.website_url + url_type
                else:
                    url = self.website_url + url_type.replace('moreinfojyxx', str(page))
                item = {"two_title": text_type}
                yield scrapy.Request(url, callback=self.parse_list, meta=item)

    def parse_list(self, response):
        lists_url = response.xpath('//tbody[@id="list"]//tr')
        for list_url in lists_url:
            try:
                detail_urls = list_url.xpath('.//a/@href').get()
                detail_title = list_url.xpath('.//a/text()').get()
                time = list_url.xpath('.//td[last()]/span/text()').get()
                city = list_url.xpath('.//td[last()-1]/span/text()').get()
                meta = {"list_url": self.website_url + detail_urls, "two_title": response.meta['two_title'] , "title": detail_title, "time": time, "city": city}
                yield scrapy.Request(url=self.website_url + detail_urls, callback=self.parse_ztb_detail, meta=meta)
            except Exception as e:
                logging.debug(e)


    def parse_ztb_detail(self, response):
        detail_htlm = response.xpath('//div[@class="w1200"]').get()
        detail_text = ' '.join(response.xpath('//div[@class="w1200"]//text()').extract()).strip()
        bid_public_time1 = response.meta['time']
        bid_public_time = format_time(bid_public_time1)
        contentUrl = response.meta['list_url']
        bid_id = get_md5(contentUrl)
        item = BidScrapyProjectItem()
        item['bid_id'] = bid_id
        item['bid_url'] = contentUrl
        item['bid_province'] = '吉林省'
        item['bid_city'] = response.meta['city']
        item['bid_category'] = '工程信息'
        item['bid_info_type'] = response.meta['two_title']
        item['bid_name'] = response.meta['title']
        item['bid_public_time'] = bid_public_time
        item['bid_html_con'] = detail_htlm
        item['bid_content'] = detail_text
        item['website_name'] = self.website_name
        item['website_url'] =self.website_url
        item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        yield item

    # def normalize_datetime(self, time_str):
    #     try:
    #         datetime_obj = pd.to_datetime(time_str, format="%Y-%m-%d %H:%M:%S")
    #     except ValueError:
    #         try:
    #             datetime_obj = pd.to_datetime(time_str, format="%Y-%m-%d")
    #         except ValueError:
    #             try:
    #                 datetime_obj = pd.to_datetime(time_str, format="%m/%d/%Y %I:%M %p")
    #             except ValueError:
    #                 return None
    #
    #     normalized_time_str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    #     return normalized_time_str