#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/5 13:37
@Author : xushaowei
@File : cgw_ln.py
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
    name = "cgw_ln"
    start_urls = 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=goPubInfoList'
    website_name = '辽宁政府采购网'
    website_url = 'http://www.ccgp-liaoning.gov.cn'
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list_page,
            dont_filter=True
        )

    def parse_list_page(self, response):
        menu_lefts = response.xpath('//ul[@class="menu_left"]//li')
        for menu_left in menu_lefts:
            for page in range(1, 4):
                id = menu_left.xpath('./a/@id').get()
                url = 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoList&t_k=null'
                data = f'current={page}&rowCount=20&searchPhrase=&infoTypeCode={id}&privateOrCity=1'
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Host": "www.ccgp-liaoning.gov.cn",
                    "Proxy-Connection": "keep-alive"
                }
                yield scrapy.Request(url, body=data, method='POST', callback=self.parse_zfcg_list, headers=headers, dont_filter=True)

    def parse_zfcg_list(self, response):
        list_datas = response.json().get('rows')
        if len(list_datas) > 0:
            for list_data in list_datas:
                articleId = list_data.get('id')
                districtName = list_data.get('districtName')
                title = list_data.get('title')
                releaseDate = list_data.get('releaseDate')
                infoTypeName = list_data.get('infoTypeName')
                url = 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoViewOpenNew&infoId=' + articleId
                meta = {"list_url": url, "title": title, "two_title": infoTypeName, "city": districtName, "public_time": releaseDate}
                yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta)
        else:
            pass

    def parse_zfcg_detail(self, response):
        detail_htlm = response.xpath('//div[@id="template"]').get().replace('&lt;', '<').replace('&#034;', '').replace('&gt;', '>')
        parser = etree.HTMLParser()
        tree = etree.fromstring(detail_htlm, parser)
        detail_text = ' '.join(tree.xpath('//text()')).strip().replace(' ', '')
        public_time = response.meta['public_time']
        po_public_time = format_time(public_time)
        contentUrl = response.meta['list_url']
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item['po_id'] = po_id
        item['bid_url'] = contentUrl
        item['po_province'] = '辽宁省'
        item['po_category'] = '政府采购'
        item['po_info_type'] = response.meta['two_title']
        item['po_public_time'] = po_public_time
        item['bo_name'] = response.meta['title']
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