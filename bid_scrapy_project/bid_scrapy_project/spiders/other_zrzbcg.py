#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/14 15:06
@Author : xushaowei
@File : other_zrzbcg.py
@Desc :
@Software:PyCharm
"""
import json
import logging
import re
import time

import pandas as pd
import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class GgzyjyNmgSpider(scrapy.Spider):
    name = "other_zrzbcg"
    start_urls = "https://zrzbcg.chinagasholdings.com/gg/cgggList"
    website_name = '中国燃气'
    website_url = 'https://zrzbcg.chinagasholdings.com'
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list_type,
            dont_filter=True
        )

    def parse_list_type(self, response):
        types_url = response.xpath('//ul[@class="cgxm"]//a/@href').getall()
        two_titles = response.xpath('//ul[@class="cgxm"]//a/text()').getall()
        for type_url, two_title in zip(types_url, two_titles):
            item = {"two_title": two_title}
            for page in range(1, 3):
                data = f'currentPage={page}&ggName='
                headers = {
                    "Host": "zrzbcg.chinagasholdings.com",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
                url = self.website_url + type_url
                yield scrapy.Request(url=url, body=data, method='POST', callback=self.parse_ztb_list, meta=item, headers=headers, dont_filter=True)

    def parse_ztb_list(self, response):
        detail_lists = response.xpath('//tbody//a')
        if len(detail_lists) > 0:
            num = len(response.xpath('//tbody//tr')[0].xpath('./td'))
            detail_times = response.xpath(f'//td[position()=((position() mod {num})=0)]//text()').getall()
            for detail_list, detail_time in zip(detail_lists, detail_times):
                detail_url = detail_list.xpath('./@href').get()
                detail_title = detail_list.xpath('./@title').get()
                time = detail_time.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
                guid = detail_url.split('guid=')[-1].split('&')[0]
                item = {"list_url": self.website_url + detail_url, "title": detail_title, "time": time,
                        "two_title": response.meta['two_title'], "guid": guid}
                url = self.website_url + detail_url
                yield scrapy.Request(url=url, callback=self.parse_get_detail_url, meta=item, dont_filter=True)

    def parse_get_detail_url(self, response):
        url = response.xpath('//iframe/@src').get()
        yield scrapy.Request(url=url, callback=self.parse_get_detail_json, meta=response.meta, dont_filter=True)

    def parse_get_detail_json(self, response):
        res_text = response.text
        url_typw = re.findall("url:'(.*?)'\+guid,", res_text)[0]
        url = self.website_url + url_typw + response.meta['guid']
        yield scrapy.Request(url=url, callback=self.parse_ztb_detail, meta=response.meta)
    def parse_ztb_detail(self, response):
        try:
            data_json = response.json()
            l = GetJsonTextSpider()
            l.print_keyvalue_all(data_json)
            text_string = l.json_text_list
            json_text = " ".join(text_string)
            detail_htlm = json.dumps(data_json, ensure_ascii=False)
            bid_public_time1 = response.meta['time']
            bid_public_time = self.normalize_datetime(bid_public_time1)
            contentUrl = response.meta['list_url']
            bid_id = get_md5(contentUrl)
            item = GovernmentProcurementItem()
            item['po_id'] = bid_id
            item['bid_url'] = contentUrl
            item['po_category'] = '采购公告'
            item['po_public_time'] = bid_public_time
            item['bo_name'] = response.meta['title']
            item['po_json_data'] = detail_htlm
            item['po_content'] = json_text
            item['website_name'] = self.website_name
            item['website_url'] = self.website_url
            item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            yield item
        except Exception as e:
            logging.debug(e)

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


class GetJsonTextSpider():
    def __init__(self):
        self.json_text_list = []

    def print_keyvalue_all(self, input_json):
        if isinstance(input_json, dict):
            for key in input_json.keys():
                key_value = input_json.get(key)
                if isinstance(key_value, dict):
                    self.print_keyvalue_all(key_value)
                elif isinstance(key_value, list):
                    for json_array in key_value:
                        self.print_keyvalue_all(json_array)
                else:
                    if key_value is None:
                        key_value = ''
                        self.json_text_list.append(str(key_value))
                    else:
                        self.json_text_list.append(str(key_value))
        elif isinstance(input_json, list):
            for input_json_array in input_json:
                self.print_keyvalue_all(input_json_array)