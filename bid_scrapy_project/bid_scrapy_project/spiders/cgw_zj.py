#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/6/27 10:39
@Author : xushaowei
@File : cgw_zj.py
@Desc :
@Software:PyCharm
"""
import datetime
import time

# import pandas as pd
import scrapy
from lxml import etree

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

from bid_scrapy_project.common.common import format_time


class GgzyjyNmgSpider(scrapy.Spider):
    name = "cgw_zj"
    start_urls = 'http://www.ccgp-zhejiang.gov.cn/admin/category/home/categoryTreeFind?parentId=600007&siteId=110&timestamp=1687833978'
    website_name = '浙江政府采购网'
    website_url = 'http://www.ccgp-zhejiang.gov.cn'
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list_page,
            dont_filter=True
        )

    def parse_list_page(self, response):
        result_json = response.json()
        result_data = result_json.get('result').get('data')[0].get('children')[0].get('children')
        for panel in result_data:
            childrens = panel.get('children')
            one_name = panel.get('name')
            one_code = panel.get('code')
            for children_data in childrens:
                code = children_data.get('code')
                name = children_data.get('name')
                dict_data = {"one_name": one_name, "one_code": one_code, "code": code, "name": name}
                url = 'http://www.ccgp-zhejiang.gov.cn/portal/category'
                timestamp = int(time.time())
                for page in range(1, 4):
                    data = '{"pageNo":"%s","pageSize":"15","categoryCode":"%s","isGov":true,"excludeDistrictPrefix":"90","_t":"%s000"}' % (page, code, timestamp)
                    headers = {
                        "Content-Type": "application/json;charset=UTF-8",
                        "Host": "www.ccgp-zhejiang.gov.cn",
                        "Proxy-Connection": "keep-alive",
                    }
                    yield scrapy.Request(url, body=data, method='POST', callback=self.parse_zfcg_list, headers=headers, meta=dict_data, dont_filter=True)

    def parse_zfcg_list(self, response):
        detail_list_data = response.json().get('result').get('data').get('data')
        for list_data in detail_list_data:
            articleId = list_data.get('articleId')
            title = list_data.get('title')
            districtName = list_data.get('districtName')
            publishDate = list_data.get('publishDate')
            url = 'http://www.ccgp-zhejiang.gov.cn/portal/detail?articleId=' + articleId
            list_url = 'http://www.ccgp-zhejiang.gov.cn/luban/detail?parentId=600007&articleId=' + articleId
            meta = {"list_url": list_url, "title": title, "one_title": response.meta['one_name'], "two_title": response.meta['name'], "city":districtName, "public_time": publishDate}
            yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta)

    def parse_zfcg_detail(self, response):
        detail_json = response.json()
        success = detail_json.get('success')
        if False is success:
            return False
        detail_data = detail_json.get('result').get('data')
        title = detail_data.get('title')
        detail_htlm = detail_data.get('content')
        parser = etree.HTMLParser()
        tree = etree.fromstring(detail_htlm, parser)
        detail_text = ' '.join(tree.xpath('//text()')).strip().replace(' ', '')
        public_time_unix_ms = response.meta['public_time']
        normal_time = datetime.datetime.fromtimestamp(public_time_unix_ms / 1000.0)
        po_public_time = format_time(normal_time)
        contentUrl = response.meta['list_url']
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item['po_id'] = po_id
        item['bid_url'] = contentUrl
        item['po_province'] = '浙江省'
        item['po_category'] = response.meta['one_title']
        item['po_info_type'] = response.meta['two_title']
        item['po_public_time'] = po_public_time
        item['bo_name'] = title
        item['po_html_con'] = detail_htlm
        item['po_content'] = detail_text
        item['website_name'] = self.website_name
        item['website_url'] = self.website_url
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