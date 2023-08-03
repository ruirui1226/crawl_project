#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/13 11:28
@Author : xushaowei
@File : other_wuliangye.py
@Desc :
@Software:PyCharm
"""
import json
import logging
import time

# import pandas as pd
import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

from bid_scrapy_project.common.common import format_time


class GgzyjyNmgSpider(scrapy.Spider):
    name = "other_wuliangye"
    start_urls = "https://wuliangye.dacaigou.com/api/saas-portal/noauth/trans/trade/getNoticeTypeConfigList"
    website_name = '五粮液电子招投标平台'
    website_url = 'https://wuliangye.dacaigou.com/'
    type = [{"type": "工程", "tradePattern": "1078329489478815744"}, {"type": "采购", "tradePattern": "1083410751742709761"}]
    def start_requests(self):
        headers = {
            "Host": "wuliangye.dacaigou.com",
            "Content-Type": "application/json"
        }
        data = '{}'
        yield scrapy.Request(
            body=data,
            method='POST',
            headers=headers,
            url=self.start_urls,
            callback=self.parse_list_type,
            dont_filter=True
        )

    def parse_list_type(self, response):
        nav_link = response.json()
        if nav_link.get('success'):
            type_datas = nav_link.get('data')
            for types in self.type:
                type = types.get('type')
                if '工程' in type:
                    tradePattern = types.get('tradePattern')
                    for type_data in type_datas:
                        aliasName = type_data.get('aliasName')
                        noticeType = type_data.get('noticeType')
                        url = 'https://wuliangye.dacaigou.com/api/saas-portal/noauth/trans/trade/pageEs'
                        for page in range(1, 3):
                            data = '{"pageNum":%s,"pageSize":12,"tradePattern":"%s","noticeType":%s,"businessName":"","releaseEndTime":"","releaseStartTime":"","purchaseProjectType":"","purchaseMode":null,"purchasePatternId":""}' % (page, tradePattern, noticeType)
                            item = {"one_title": type, "two_title": aliasName}
                            headers = {
                                "Host": "wuliangye.dacaigou.com",
                                "Content-Type": "application/json"
                            }
                            yield scrapy.Request(url=url, body=data, method='POST', callback=self.parse_ztb_list, meta=item, headers=headers, dont_filter=True)
                else:
                    tradePattern = types.get('tradePattern')
                    for type_data in type_datas:
                        aliasName = type_data.get('aliasName')
                        noticeType = type_data.get('noticeType')
                        url = 'https://wuliangye.dacaigou.com/api/saas-portal/noauth/trans/trade/pageEs'
                        for page in range(1, 3):
                            data = '{"pageNum":%s,"pageSize":12,"tradePattern":"%s","noticeType":%s,"businessName":"","releaseEndTime":"","releaseStartTime":"","purchaseProjectType":"","purchaseMode":null,"purchasePatternId":""}' % (page, tradePattern, noticeType)
                            item = {"one_title": type, "two_title": aliasName}
                            headers = {
                                "Host": "wuliangye.dacaigou.com",
                                "Content-Type": "application/json"
                            }
                            yield scrapy.Request(url=url, body=data, method='POST', callback=self.parse_zfcg_list, meta=item, headers=headers, dont_filter=True)
    def parse_ztb_list(self, response):
        if response.json().get('success'):
            lists = response.json().get('data').get('list')
            if len(lists) > 0:
                for list in lists:
                    try:
                        businessName = list.get('businessName')
                        id = list.get('id')
                        noticeType = list.get('noticeType')
                        releaseTime = list.get('releaseTime')
                        publishStatus = list.get('publishStatus')
                        timeStamp = float(releaseTime / 1000)
                        timeArray = time.localtime(timeStamp)
                        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        url = f'https://wuliangye.dacaigou.com/api/saas-portal/noauth/trans/trade/getByTradeId?id={id}&noticeType={noticeType}'
                        meta = {"list_url": f'https://wuliangye.dacaigou.com/web-portal/index.html#/trade-info-detail?id={id}&noticeType={noticeType}&publishStatus={publishStatus}&systemStatus', "title": businessName, "time": otherStyleTime, "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
                        yield scrapy.Request(url, callback=self.parse_ztb_getdetailurl, meta=meta)
                    except Exception as e:
                        logging.debug(e)

    def parse_zfcg_list(self, response):
        if response.json().get('success'):
            lists = response.json().get('data').get('list')
            if len(lists) > 0:
                for list in lists:
                    try:
                        businessName = list.get('businessName')
                        id = list.get('id')
                        noticeType = list.get('noticeType')
                        releaseTime = list.get('releaseTime')
                        publishStatus = list.get('publishStatus')
                        timeStamp = float(releaseTime / 1000)
                        timeArray = time.localtime(timeStamp)
                        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        url = f'https://wuliangye.dacaigou.com/api/saas-portal/noauth/trans/trade/getByTradeId?id={id}&noticeType={noticeType}'
                        meta = {"list_url": f'https://wuliangye.dacaigou.com/web-portal/index.html#/trade-info-detail?id={id}&noticeType={noticeType}&publishStatus={publishStatus}&systemStatus', "title": businessName, "time": otherStyleTime,
                                "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
                        yield scrapy.Request(url, callback=self.parse_zfcg_getdetailurl, meta=meta)
                    except Exception as e:
                        logging.debug(e)

    def parse_ztb_getdetailurl(self, response):
        detail_json = response.json()
        if detail_json.get('success'):
            detail_html_url = detail_json.get('data').get('biddingNotice')
            if detail_html_url is None:
                l = GetJsonTextSpider()
                l.print_keyvalue_all(detail_json)
                text_string = l.json_text_list
                json_text = " ".join(text_string)
                detail_htlm = json.dumps(detail_json, ensure_ascii=False)
                bid_public_time1 = response.meta['time']
                bid_public_time = format_time(bid_public_time1)
                contentUrl = response.meta['list_url']
                bid_id = get_md5(contentUrl)
                item = BidScrapyProjectItem()
                item['bid_id'] = bid_id
                item['bid_url'] = contentUrl
                item['bid_category'] = '招标公告'
                item['bid_name'] = response.meta['title']
                item['bid_public_time'] = bid_public_time
                item['bid_json_data'] = detail_htlm
                item['bid_content'] = json_text
                item['website_name'] = self.website_name
                item['website_url'] = self.website_url
                item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                yield item
            else:
                detail_html_url = detail_json.get('data').get('biddingNotice').get('htmlFileUrl')
                meta = {"list_url": response.meta['list_url'], "title": response.meta['title'], "time": response.meta['time'], "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
                yield scrapy.Request(detail_html_url, callback=self.parse_ztb_detail, meta=meta)


    def parse_zfcg_getdetailurl(self, response):
        detail_json = response.json()
        if detail_json.get('success'):
            detail_html_url = detail_json.get('data').get('biddingNotice')
            if detail_html_url is None:
                l = GetJsonTextSpider()
                l.print_keyvalue_all(detail_json)
                text_string = l.json_text_list
                json_text = " ".join(text_string)
                detail_htlm = json.dumps(detail_json, ensure_ascii=False)
                bid_public_time1 = response.meta['time']
                po_public_time = format_time(bid_public_time1)
                contentUrl = response.meta['list_url']
                po_id = get_md5(contentUrl)
                item = GovernmentProcurementItem()
                item['po_id'] = po_id
                item['bid_url'] = contentUrl
                item['po_category'] = '采购公告'
                item['po_public_time'] = po_public_time
                item['bo_name'] = response.meta['title']
                item['po_json_data'] = detail_htlm
                item['po_content'] = json_text
                item['website_name'] = self.website_name
                item['website_url'] = self.website_url
                item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                yield item
            else:
                detail_html_url = detail_json.get('data').get('biddingNotice').get('htmlFileUrl')
                meta = {"list_url": response.meta['list_url'], "title": response.meta['title'], "time": response.meta['time'],
                        "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
                yield scrapy.Request(detail_html_url, callback=self.parse_zfcg_detail, meta=meta)
    def parse_ztb_detail(self, response):
        detail_htlm = response.text
        detail_text = ' '.join(response.xpath('//text()').extract()).strip().replace(' ', '')
        bid_public_time1 = response.meta['time']
        bid_public_time = format_time(bid_public_time1)
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
        detail_htlm = response.text
        detail_text = ' '.join(response.xpath('//text()').extract()).strip().replace(' ', '')
        bid_public_time1 = response.meta['time']
        po_public_time = format_time(bid_public_time1)
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