#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/19 15:32
@Author : xushaowei
@File : other_cdcin.py
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
    name = "other_cdcin"
    start_urls = "http://www.cdcin.com/two/gsgg.do?flmbh=169&flmmc=LcTnJMx4M5ArSBMjIPpFtA&lmbh=150&lmmc=sCo7ALcTHXsExegaUEhkivuimTpzfOxP&curPage=-1"
    website_name = '成都建信'
    website_url = 'http://www.cdcin.com/'
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list_page,
            dont_filter=True
        )
    def parse_list_page(self, response):
        nav_link = response.xpath('//td[@class="navbar-bg"]//li')
        for url_min in nav_link:
            url_type = url_min.xpath('.//a/@href').get()
            text_type = url_min.xpath('.//a/text()').get()
            for page in range(1, 3):
                if '1' in str(page):
                    url = self.website_url + url_type
                else:
                    url = self.website_url + url_type.replace('&curPage=-1', f'&rowCount=1&pageCount=10&curPage={str(page)}')
                item = {"bid_category": text_type}
                yield scrapy.Request(url, callback=self.parse_list, meta=item)

    def parse_list(self, response):
        lists_url = response.xpath('//table[@class="table-style1"]//tr')
        for list_url in lists_url:
            try:
                if '评标结果公示' in response.meta['bid_category']:
                    if list_url.xpath('.//td').get() is not None:
                        detail_urls = list_url.xpath('.//a/@href').get()
                        detail_title = list_url.xpath('.//a/text()').get()
                        time = list_url.xpath('.//td[last()]/text()').get()
                        type = list_url.xpath('.//td[last()-3]/text()').get()
                        meta = {"list_url": self.website_url + detail_urls, "bid_category": response.meta['bid_category'], "title": detail_title.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').replace(' ', ''), "time": time, "bid_info_type": type}
                        yield scrapy.Request(url=self.website_url + detail_urls, callback=self.parse_ztb_detail, meta=meta)
            except Exception as e:
                logging.debug(e)


    def parse_ztb_detail(self, response):
        detail_htlm = response.xpath('//div[@class="container"]').getall()[3]
        detail_text = ' '.join(response.xpath('//div[@class="container"]')[3].xpath('.//text()').getall()).strip()
        bid_public_time1 = response.meta['time']
        bid_public_time = format_time(bid_public_time1)
        contentUrl = response.meta['list_url']
        bid_id = get_md5(contentUrl)
        item = BidScrapyProjectItem()
        item['bid_id'] = bid_id
        item['bid_url'] = contentUrl
        item['bid_province'] = '成都市'
        item['bid_city'] = '成都市'
        item['bid_category'] = response.meta['bid_category']
        item['bid_info_type'] = response.meta['bid_info_type']
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