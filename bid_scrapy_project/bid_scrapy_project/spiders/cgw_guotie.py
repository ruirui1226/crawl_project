#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/12 9:59
@Author : xushaowei
@File : cgw_guotie.py
@Desc : 国铁 如果获取数据较少，属正常，该网址获取的接口时而能拿到时而拿不到
@Software:PyCharm
"""
import time

import pandas as pd
import scrapy
from lxml import etree

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class GgzyjyNmgSpider(scrapy.Spider):
    name = "cgw_guotie"
    bidTypes = tinydict = [{'type':'招标', 'num': '01'}, {'type':'非招标', 'num': '000'}]
    website_name = '国铁采购平台'
    website_url = 'https://cg.95306.cn'
    def start_requests(self):
        for bidType in self.bidTypes:
            for page in range(1, 4):
                type = bidType.get('type')
                num = bidType.get('num')
                item = {"type": type}
                url = f'https://cg.95306.cn/proxy/portal/elasticSearch/queryDataToEs?projBidType=01&disposalMethod=&bidType={num}&noticeType=&title=&inforCode=&startDate=&endDate=&pageNum={page}&projType=&professionalCode=&createPeopUnit='
                headers = {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Connection": "keep-alive",
                        "Cookie": "AlteonPcgmh=0a03b7f5e5d9dcfd1f41",
                        "Host": "cg.95306.cn",
                        "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                        "Sec-Ch-Ua-Mobile": "?0",
                        "Sec-Ch-Ua-Platform": "\"Windows\"",
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-User": "?1",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                    }
                yield scrapy.Request(url, callback=self.parse_list_page, meta=item, headers=headers,
                                     dont_filter=True)

    def parse_list_page(self, response):
        json_data = response.json()
        if json_data.get('success'):
            menu_lefts = json_data.get('data').get('resultData').get('result')
            for menu_left in menu_lefts:
                title = menu_left.get('notTitle')
                two_title = menu_left.get('noticeTypeName')
                public_time = menu_left.get('checkTime')
                key = menu_left.get('id')
                url = 'https://cg.95306.cn/proxy/portal/elasticSearch/indexView?noticeId=' + key
                item = {"url": url, "title": title, "two_title": two_title, "public_time": public_time}
                headers = {
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Connection": "keep-alive",
                    "Cookie": "AlteonPcgmh=0a03b7f7669c7a9d1f41",
                    "Host": "cg.95306.cn",
                    "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": "\"Windows\"",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    "X-Requested-With": "XMLHttpRequest"
                }
                yield scrapy.Request(url, callback=self.parse_zfcg_detail, headers=headers, meta=item)

    def parse_zfcg_detail(self, response):
        json_data = response.json()
        if json_data.get('success'):
            noticeContent = json_data.get('data').get('noticeContent')
            detail_htlm = noticeContent.get('notCont')
            parser = etree.HTMLParser()
            tree = etree.fromstring(detail_htlm, parser)
            detail_text = ' '.join(tree.xpath('//text()')).strip().replace(' ', '')
            public_time = noticeContent.get('checkTime')
            po_public_time = self.normalize_datetime(public_time)
            contentUrl = 'https://cg.95306.cn/baseinfor/notice/informationShow?id=' + noticeContent.get('id')
            po_id = get_md5(contentUrl)
            item = GovernmentProcurementItem()
            item['po_id'] = po_id
            item['bid_url'] = contentUrl
            item['po_province'] = '国铁'
            item['po_category'] = '国铁采购'
            item['po_info_type'] = response.meta['two_title']
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