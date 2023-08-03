#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/6/21 10:59
@Author : xushaowei
@File : ggzyjy_zj.py
@Desc : 浙江省公共资源交易服务平台
@Software:PyCharm
"""
import json
import time

# import pandas as pd
import scrapy

from bid_scrapy_project.common.common import get_md5, gettime_day
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

from bid_scrapy_project.common.common import format_time


class GgzyjyNmgSpider(scrapy.Spider):
    name = "ggzyjy_zj"
    start_urls = "http://zjpubservice.zjzwfw.gov.cn/jyxxgk/list.html"
    website_name = '浙江省公共资源交易服务平台'
    website_url = 'http://zjpubservice.zjzwfw.gov.cn'
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list_page,
            dont_filter=True
        )

    def parse_list_page(self, response):
        panel_list = response.xpath('//ul[@id="jyly"]/li')
        gcxmdiv_item = response.xpath('//div[@id="gcxmdiv"]/li')    # 工程建设
        zfcgdiv_item = response.xpath('//div[@id="zfcgdiv"]/li')    # 政府采购
        tdkcdiv_item = response.xpath('//div[@id="tdkcdiv"]/li')    # 土地矿产
        cqjydiv_item = response.xpath('//div[@id="cqjydiv"]/li')    # 国有产权
        lqdiv_item = response.xpath('//div[@id="lqdiv"]/li')  # 林权交易
        ynqdiv_item = response.xpath('//div[@id="ynqdiv"]/li')  # 用能权
        pwqdiv_item = response.xpath('//div[@id="pwqdiv"]/li')  # 排污权
        qtjydiv_item = response.xpath('//div[@id="qtjydiv"]/li')  # 其他交易
        # zfbzdiv_item = response.xpath('//div[@id="zfbzdiv"]/li')  # 住房保障
        # kyqdiv_item = response.xpath('//div[@id="kyqdiv"]/li')    # 矿业权
        title = []
        for gcxmdiv in gcxmdiv_item:
            two_title = gcxmdiv.xpath('./a/text()').get()
            catenum = gcxmdiv.xpath('./a/@catenum').get()
            one_title = panel_list[0].xpath('./a/text()').get()
            value = panel_list[0].xpath('./a/@value').get()
            title_dict = {"one_title": one_title, "value": value, "two_title": two_title, "catenum": catenum}
            title.append(title_dict)
        for zfcgdiv in zfcgdiv_item:
            two_title = zfcgdiv.xpath('./a/text()').get()
            catenum = zfcgdiv.xpath('./a/@catenum').get()
            one_title = panel_list[1].xpath('./a/text()').get()
            value = panel_list[1].xpath('./a/@value').get()
            title_dict = {"one_title": one_title, "value": value, "two_title": two_title, "catenum": catenum}
            title.append(title_dict)
        for tdkcdiv in tdkcdiv_item:
            two_title = tdkcdiv.xpath('./a/text()').get()
            catenum = tdkcdiv.xpath('./a/@catenum').get()
            one_title = panel_list[2].xpath('./a/text()').get()
            value = panel_list[2].xpath('./a/@value').get()
            title_dict = {"one_title": one_title, "value": value, "two_title": two_title, "catenum": catenum}
            title.append(title_dict)
        for cqjydiv in cqjydiv_item:
            two_title = cqjydiv.xpath('./a/text()').get()
            catenum = cqjydiv.xpath('./a/@catenum').get()
            one_title = panel_list[3].xpath('./a/text()').get()
            value = panel_list[3].xpath('./a/@value').get()
            title_dict = {"one_title": one_title, "value": value, "two_title": two_title, "catenum": catenum}
            title.append(title_dict)
        for lqdiv in lqdiv_item:
            two_title = lqdiv.xpath('./a/text()').get()
            catenum = lqdiv.xpath('./a/@catenum').get()
            one_title = panel_list[4].xpath('./a/text()').get()
            value = panel_list[4].xpath('./a/@value').get()
            title_dict = {"one_title": one_title, "value": value, "two_title": two_title, "catenum": catenum}
            title.append(title_dict)
        for ynqdiv in ynqdiv_item:
            two_title = ynqdiv.xpath('./a/text()').get()
            catenum = ynqdiv.xpath('./a/@catenum').get()
            one_title = panel_list[5].xpath('./a/text()').get()
            value = panel_list[5].xpath('./a/@value').get()
            title_dict = {"one_title": one_title, "value": value, "two_title": two_title, "catenum": catenum}
            title.append(title_dict)
        for pwqdiv in pwqdiv_item:
            two_title = pwqdiv.xpath('./a/text()').get()
            catenum = pwqdiv.xpath('./a/@catenum').get()
            one_title = panel_list[6].xpath('./a/text()').get()
            value = panel_list[6].xpath('./a/@value').get()
            title_dict = {"one_title": one_title, "value": value, "two_title": two_title, "catenum": catenum}
            title.append(title_dict)
        for qtjydiv in qtjydiv_item:
            two_title = qtjydiv.xpath('./a/text()').get()
            catenum = qtjydiv.xpath('./a/@catenum').get()
            one_title = panel_list[7].xpath('./a/text()').get()
            value = panel_list[7].xpath('./a/@value').get()
            title_dict = {"one_title": one_title, "value": value, "two_title": two_title, "catenum": catenum}
            title.append(title_dict)

        for nav_link in title:
            one_title = nav_link.get('one_title')
            two_title = nav_link.get('two_title')
            catenum = nav_link.get('catenum')
            value = nav_link.get('value')
            date_time = gettime_day(days=7)
            end_of_day = str(date_time[0])
            start_of_day = str(date_time[1])
            for page_i in range(0, 4):
                url = 'http://zjpubservice.zjzwfw.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData'
                meta = {"one_title": one_title, "two_title": two_title, "url": url, "catenum": catenum}
                if '002002' == value:
                    for page in range(0, 48, 12):
                        payload = json.dumps({
                            "token": "",
                            "pn": 0,
                            "rn": 12,
                            "sdt": "",
                            "edt": "",
                            "wd": "",
                            "inc_wd": "",
                            "exc_wd": "",
                            "fields": "title",
                            "cnum": "001",
                            "sort": "{\"webdate\":\"0\"}",
                            "ssort": "title",
                            "cl": 200,
                            "terminal": "",
                            "condition": [
                                {
                                    "fieldName": "categorynum",
                                    "isLike": True,
                                    "likeType": 2,
                                    "equal": catenum
                                },
                                {
                                    "fieldName": "infoc",
                                    "isLike": True,
                                    "likeType": 2,
                                    "equal": "33"
                                }
                            ],
                            "time": [
                                {
                                    "fieldName": "webdate",
                                    "startTime": start_of_day,
                                    "endTime": end_of_day
                                }
                            ],
                            "highlights": "",
                            "statistics": None,
                            "unionCondition": None,
                            "accuracy": "",
                            "noParticiple": "0",
                            "searchRange": None,
                            "isBusiness": "1"
                        })
                        yield scrapy.Request(url, method="POST", body=payload, callback=self.parse_zfcg_list, dont_filter=True, meta=meta)
                else:
                    for page in range(1, 4):
                        payload = json.dumps({
                            "token": "",
                            "pn": 0,
                            "rn": 12,
                            "sdt": "",
                            "edt": "",
                            "wd": "",
                            "inc_wd": "",
                            "exc_wd": "",
                            "fields": "title",
                            "cnum": "001",
                            "sort": "{\"webdate\":\"0\"}",
                            "ssort": "title",
                            "cl": 200,
                            "terminal": "",
                            "condition": [
                                {
                                    "fieldName": "categorynum",
                                    "isLike": True,
                                    "likeType": 2,
                                    "equal": catenum
                                },
                                {
                                    "fieldName": "infoc",
                                    "isLike": True,
                                    "likeType": 2,
                                    "equal": "33"
                                }
                            ],
                            "time": [
                                {
                                    "fieldName": "webdate",
                                    "startTime": start_of_day,
                                    "endTime": end_of_day
                                }
                            ],
                            "highlights": "",
                            "statistics": None,
                            "unionCondition": None,
                            "accuracy": "",
                            "noParticiple": "0",
                            "searchRange": None,
                            "isBusiness": "1"
                        })
                        yield scrapy.Request(url, method="POST", body=payload, callback=self.parse_ztb_list, dont_filter=True, meta=meta)

    def parse_ztb_list(self, response):
        json_data = response.json()
        records = json_data.get('result').get('records')
        for item in records:
            titlenew = item['titlenew']
            infod = item['infod']
            webdate = item['webdate']
            linkurl = item['linkurl']
            url = self.website_url + linkurl
            meta = {"one_title": response.meta['one_title'], "two_title": response.meta['two_title'], "url": response.meta['url'], "catenum": response.meta['catenum'],
                    "titlenew": titlenew, "infod": infod, "webdate": webdate, "linkurl": url}
            yield scrapy.Request(url, callback=self.parse_ztb_detail, meta=meta)


    def parse_zfcg_list(self, response):
        json_data = response.json()
        records = json_data.get('result').get('records')
        for item in records:
            titlenew = item['titlenew']
            infod = item['infod']
            webdate = item['webdate']
            linkurl = item['linkurl']
            url = self.website_url + linkurl
            meta = {"one_title": response.meta['one_title'], "two_title": response.meta['two_title'],
                    "url": response.meta['url'], "catenum": response.meta['catenum'],
                    "titlenew": titlenew, "infod": infod, "webdate": webdate, "linkurl": url}
            yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta)

    def parse_ztb_detail(self, response):
        detail_htlm = response.xpath('//div[@class="ewb-page-main ewb-h543"]').get()
        detail_text = ' '.join(response.xpath('//div[@class="ewb-page-main ewb-h543"]//text()').extract()).strip()
        public_time = response.meta['webdate']
        bid_public_time = format_time(public_time)
        contentUrl = response.meta['linkurl']
        bid_id = get_md5(contentUrl)
        item = BidScrapyProjectItem()
        item['bid_id'] = bid_id
        item['bid_url'] = contentUrl
        item['bid_province'] = '浙江省'
        item['bid_category'] = response.meta['one_title']
        item['bid_info_type'] = response.meta['two_title']
        item['bid_name'] = response.meta['titlenew']
        item['bid_public_time'] = bid_public_time
        item['bid_html_con'] = detail_htlm
        item['bid_content'] = detail_text
        item['website_name'] = self.website_name
        item['website_url'] =self.website_url
        item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        yield item
    def parse_zfcg_detail(self, response):
        detail_htlm = response.xpath('//div[@class="ewb-page-main ewb-h543"]').get()
        detail_text = ' '.join(response.xpath('//div[@class="ewb-page-main ewb-h543"]//text()').extract()).strip()
        public_time = response.meta['webdate']
        po_public_time = format_time(public_time)
        contentUrl = response.meta['linkurl']
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item['po_id'] = po_id
        item['bid_url'] = contentUrl
        item['po_province'] = '浙江省'
        item['po_category'] = response.meta['one_title']
        item['po_info_type'] = response.meta['two_title']
        item['po_public_time'] = po_public_time
        item['bo_name'] = response.meta['titlenew']
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