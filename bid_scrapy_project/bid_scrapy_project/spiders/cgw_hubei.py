#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 3/7/2023 下午1:36
@Author : xushaowei
@File : cgw_hubei.py
@Desc :
@Software:PyCharm
"""
import datetime
import re
import time

import pandas as pd
import scrapy
from lxml import etree

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class GgzyjyNmgSpider(scrapy.Spider):
    name = "cgw_hubei"
    start_urls = 'http://www.ccgp-hubei.gov.cn/sub/left_memu.jsp?act=01'
    website_name = '湖北采购网'
    website_url = 'http://www.ccgp-hubei.gov.cn'
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list_page,
            dont_filter=True
        )

    def parse_list_page(self, response):
        result_urls = response.xpath('//div[@class="nav-list"]//li/a/@href').getall()
        result_texts = response.xpath('//div[@class="nav-list"]//li/a/text()').getall()
        for url, text in zip(result_urls, result_texts):
            dict_data = {"one_title": '采购公告', "two_title": text, "url": url}
            url = self.website_url + url
            yield scrapy.Request(url, callback=self.parse_zfcg_list, meta=dict_data, dont_filter=True)

    def parse_zfcg_list(self, response):
        details = response.xpath('//ul[@class="news-list-content list-unstyled margin-top-20"]//li')
        page_li = response.xpath('//ul[@class="pagination"]//li')[-1].get()
        page_max = re.findall('/(\d+)页', page_li)[0]
        if len(details) > 0:
            for list_data in details:
                url_type = list_data.xpath('./a/@href').get()
                title = list_data.xpath('./a/text()').getall()[1]
                time = list_data.xpath('./span/text()').get()
                url = self.website_url + url_type
                meta = {"list_url": url, "title": title, "one_title": response.meta['one_title'], "two_title": response.meta['two_title'], "public_time": time}
                if int(page_max) > 1:
                    for page in range(1, int(page_max) + 1):
                        url_list = response.url
                        url_list_page = url_list.split('_1.html')[0]
                        url_page = url_list_page + f'_{page}.html'
                        yield scrapy.Request(url_page, callback=self.parse_zfcg_page, meta=meta, dont_filter=True)
                else:
                    yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta)
        else:
            pass

    def parse_zfcg_page(self, response):
        details = response.xpath('//ul[@class="news-list-content list-unstyled margin-top-20"]//li')
        if len(details) > 0:
            for list_data in details:
                url_type = list_data.xpath('./a/@href').get()
                title = list_data.xpath('./a/text()').getall()[1]
                time = list_data.xpath('./span/text()').get()
                url = self.website_url + url_type
                meta = {"list_url": url, "title": title, "one_title": response.meta['one_title'], "two_title": response.meta['two_title'], "public_time": time}
                yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta)
        else:
            pass

    def parse_zfcg_detail(self, response):
        detail_html = response.xpath('//div[@class="art_con"]').get()
        detail_text = ' '.join(response.xpath('//div[@class="art_con"]//text()').extract()).strip().replace(' ', '')
        public_time = response.meta['public_time']
        po_public_time = self.normalize_datetime(public_time)
        contentUrl = response.meta['list_url']
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item['po_id'] = po_id
        item['bid_url'] = contentUrl
        item['po_province'] = '湖北省'
        item['po_category'] = response.meta['one_title']
        item['po_info_type'] = response.meta['two_title']
        item['po_public_time'] = po_public_time
        item['bo_name'] = response.meta['title']
        item['po_html_con'] = detail_html
        item['po_content'] = detail_text
        item['website_name'] = self.website_name
        item['website_url'] = self.website_url
        item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        yield item

    def normalize_datetime(self, time_str):
        try:
            datetime_obj = pd.to_datetime(time_str, format="%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                datetime_obj = pd.to_datetime(time_str, format="%Y-%m-%d")
            except ValueError:
                try:
                    datetime_obj = pd.to_datetime(time_str, format="%m/%d/%Y %I:%M %p")
                except ValueError:
                    return None

        normalized_time_str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        return normalized_time_str