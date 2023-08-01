#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/12 17:28
@Author : xushaowei
@File : other_chinagoldgroup.py
@Desc :
@Software:PyCharm
"""
import logging
import time

import pandas as pd
import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class GgzyjyNmgSpider(scrapy.Spider):
    name = "other_chinagoldgroup"
    start_urls = "https://zjjs.chinagoldgroup.com/2110.html"
    website_name = '中国黄金集团建设有限公司'
    website_url = 'https://zjjs.chinagoldgroup.com'
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list_page,
            dont_filter=True
        )

    def parse_list_page(self, response):
        nav_link = response.xpath('//ul[@class="accordion-3"]//li/a/@href').getall()[-2:]
        for url_min in nav_link:
            if '2431' in url_min:
                yield scrapy.Request(url_min, callback=self.parse_zfcg_list, dont_filter=True)
            else:
                yield scrapy.Request(url_min, callback=self.parse_ztb_list, dont_filter=True)

    def parse_ztb_list(self, response):
        lists_url = response.xpath('//div[@class="list"]//div[@class="second-item"]')
        for list_url in lists_url:
            try:
                detail_urls = list_url.xpath('.//a/@href').get()
                detail_title = list_url.xpath('.//a/text()').get()
                time = list_url.xpath('./div[@class="second-item-date"]/text()').get()
                if '\r\n' in time:
                    time = time.replace(' ', '').replace('\r\n', '').replace('\t', '')
                meta = {"list_url": detail_urls, "title": detail_title.replace(' ', '').replace('\r', '').replace('\t', '').replace('\n', ''), "time": time}
                yield scrapy.Request(detail_urls, callback=self.parse_ztb_detail, meta=meta)
            except Exception as e:
                logging.debug(e)

    def parse_zfcg_list(self, response):
        lists_url = response.xpath('//div[@class="list"]//div[@class="second-item"]')
        for list_url in lists_url:
            try:
                detail_urls = list_url.xpath('.//a/@href').get()
                detail_title = list_url.xpath('.//a/text()').get()
                time = list_url.xpath('./div[@class="second-item-date"]/text()').get()
                if '\r\n' in time:
                    time = time.replace(' ', '').replace('\r\n', '').replace('\t', '')
                meta = {"list_url": detail_urls, "title": detail_title.replace(' ', '').replace('\r\n', '').replace('\t', ''), "time": time}
                yield scrapy.Request(detail_urls, callback=self.parse_zfcg_detail, meta=meta)
            except Exception as e:
                logging.debug(e)


    def parse_ztb_detail(self, response):
        detail_htlm = response.xpath('//div[@class="Gnews-detail"]').get()
        detail_text = ' '.join(response.xpath('//div[@class="Gnews-detail"]//text()').extract()).strip()
        bid_public_time1 = response.meta['time']
        bid_public_time = self.normalize_datetime(bid_public_time1)
        contentUrl = response.meta['list_url']
        bid_id = get_md5(contentUrl)
        item = BidScrapyProjectItem()
        item['bid_id'] = bid_id
        item['bid_url'] = contentUrl
        item['bid_category'] = '招标公告'
        item['bid_name'] = response.meta['title']
        item['bid_public_time'] = bid_public_time
        item['bid_html_con'] = detail_htlm
        item['bid_content'] = detail_text
        item['website_name'] = self.website_name
        item['website_url'] =self.website_url
        item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        yield item
    def parse_zfcg_detail(self, response):
        detail_htlm = response.xpath('//div[@class="Gnews-detail"]').get()
        detail_text = ' '.join(response.xpath('//div[@class="Gnews-detail"]//text()').extract()).strip()
        bid_public_time1 = response.meta['time']
        po_public_time = self.normalize_datetime(bid_public_time1)
        contentUrl = response.meta['list_url']
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item['po_id'] = po_id
        item['bid_url'] = contentUrl
        item['po_category'] = '采购公告'
        item['po_public_time'] = po_public_time
        item['bo_name'] = response.meta['title']
        item['po_html_con'] = detail_htlm
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