#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/7 15:11
@Author : xushaowei
@File : cgw_zcyun.py
@Desc :
@Software:PyCharm
"""
import datetime
import time
from io import StringIO

import pandas as pd
import scrapy
from lxml import etree

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class GgzyjyNmgSpider(scrapy.Spider):
    name = "cgw_zcyun"
    start_urls = 'http://www.zcbidding.com/portal/jyxx?type=zbgg&flag=jyxx'
    website_name = '采招云电子招投标交易平台'
    website_url = 'http://www.zcbidding.com'
    type_codes = [{"data-val": 'zbgg', "type": '招标公告'},
                {"data-val": 'bggg', "type": '变更公告'},
                {"data-val": 'zbgs', "type": '中标公示'},
                {"data-val": 'zbggs', "type": '中标公告'},
                {"data-val": 'dycq', "type": '答疑澄清'},
                {"data-val": 'lbgg', "type": '流标公告'},
             ]
    def start_requests(self):
        for page in range(1, 4):
            for type_code in self.type_codes:
                data_val = type_code.get('data-val')
                type = type_code.get('type')
                item = {"two_title": type}
                url = 'http://www.zcbidding.com/web/Dealxx/jxmessage'
                data = f'type={data_val}&startTime=&endTime=&title=&page={page}'
                headers = {
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Host": "www.zcbidding.com",
                    "Origin": "http://www.zcbidding.com",
                    "Proxy-Connection": "keep-alive",
                    "Referer": "http://www.zcbidding.com/portal/jyxx?type=zbgg&flag=jyxx",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    "X-Requested-With": "XMLHttpRequest"
                }
                yield scrapy.Request(url, callback=self.parse_list_page, body=data, method='POST', meta=item, dont_filter=True, headers=headers)

    def parse_list_page(self, response):
        result_json = response.json()
        result_data = result_json.get('data')
        if len(result_data) > 0:
            for list_item in result_data:
                detail_htlm = list_item.get('descr')
                title = list_item.get('title')
                po_info_type = list_item.get('type')
                po_city = list_item.get('regionCodeName')
                tree = etree.parse(StringIO(detail_htlm), etree.HTMLParser())
                detail_text = ' '.join(tree.xpath('//text()')).strip()
                bid_public_time = list_item.get('noticeSendTime')
                po_public_time = self.normalize_datetime(bid_public_time)
                url = 'http://www.zcbidding.com/portal/ggXq?id=' + str(list_item.get('id'))
                po_id = get_md5(url)
                item = GovernmentProcurementItem()
                item['po_id'] = po_id
                item['bid_url'] = url
                item['po_province'] = '河北省'
                item['po_category'] = '政府采购'
                item['po_city'] = po_city
                item['po_info_type'] = po_info_type
                item['po_public_time'] = po_public_time
                item['bo_name'] = title
                item['po_html_con'] = detail_htlm
                item['po_content'] = detail_text
                item['website_name'] = self.website_name
                item['website_url'] = self.website_url
                item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                item['list_parse'] = url
                yield item
        else:
            pass
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