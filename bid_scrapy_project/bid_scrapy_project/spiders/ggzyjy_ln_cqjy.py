#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/5 10:30
@Author : xushaowei
@File : ggzyjy_ln_cqjy.py
@Desc :
@Software:PyCharm
"""
import json
import time

import pandas as pd
import requests
import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class GgzyjyNmgSpider(scrapy.Spider):
    name = "ggzyjy_liaoning_cqjy"
    website_name = '辽宁省公共资源交易网'
    website_url = 'http://ggzy.ln.gov.cn'
    type_codes = [{"city": "省本级", "data_code": '149563', "type": '交易公告'},
                {"city": "省本级", "data_code": '157443', "type": '变更公告'},
                {"city": "省本级", "data_code": '149564', "type": '成交公告'},
                {"city": "省本级", "data_code": '157763', "type": '特殊事项公告'},

                {"city": "沈阳市", "data_code": '152829', "type": '交易公告'},
                {"city": "沈阳市", "data_code": '152830', "type": '成交公告'},

                {"city": "大连市", "data_code": '157799', "type": '交易公告'},
                {"city": "大连市", "data_code": '152854', "type": '成交公告'},

                {"city": "鞍山市", "data_code": '152876', "type": '交易公告'},
                {"city": "鞍山市", "data_code": '152877', "type": '成交公告'},

                {"city": "本溪市", "data_code": '152922', "type": '交易公告'},
                {"city": "本溪市", "data_code": '152923', "type": '成交公告'},

                {"city": "丹东市", "data_code": '152945', "type": '交易公告'},
                {"city": "丹东市", "data_code": '152946', "type": '成交公告'},

                {"city": "锦州市", "data_code": '152968', "type": '交易公告'},
                {"city": "锦州市", "data_code": '152969', "type": '成交公告'},

                {"city": "营口市", "data_code": '152991', "type": '交易公告'},
                {"city": "营口市", "data_code": '152992', "type": '成交公告'},

                {"city": "阜新市", "data_code": '153014', "type": '交易公告'},
                {"city": "阜新市", "data_code": '153015', "type": '成交公告'},

                {"city": "辽阳市", "data_code": '153037', "type": '交易公告'},
                {"city": "辽阳市", "data_code": '153038', "type": '成交公告'},

                {"city": "铁岭市", "data_code": '153060', "type": '交易公告'},
                {"city": "铁岭市", "data_code": '153061', "type": '成交公告'},

                {"city": "朝阳市", "data_code": '153083', "type": '交易公告'},
                {"city": "朝阳市", "data_code": '153084', "type": '成交公告'},

                {"city": "盘锦市", "data_code": '153106', "type": '交易公告'},
                {"city": "盘锦市", "data_code": '153107', "type": '成交公告'},
             ]
    def start_requests(self):
        for page in range(1, 4):
            for type_code in self.type_codes:
                city = type_code.get('city')
                data_code = type_code.get('data_code')
                type = type_code.get('type')
                item = {"two_title": type, "city": city}
                timestamp = int(time.time() * 1000)
                url = f'http://218.60.147.210/was5/web/search?page={page}&perpage=20&docchannel={data_code}&channelid=211892&_={timestamp}'
                yield scrapy.Request(url=url, callback=self.parse_list_page, meta=item, dont_filter=True)

    def parse_list_page(self, response):
        data_json =json.loads(response.text.split('null(')[1].rsplit(")", 1)[0])
        datas = data_json.get('datas')
        if len(datas) > 0:
            for data in datas:
                docpuburl = data.get('DOCPUBURL')
                title = data.get('DOCTITLE')
                time = data.get('DOCRELTIME')
                item = {"url": docpuburl, "two_title": response.meta['two_title'], "city": response.meta['city'], "title": title, "time": time}
                yield scrapy.Request(docpuburl, callback=self.parse_ztb_detail, meta=item)
        else:
            pass
    def parse_ztb_detail(self, response):
        detail_htlm = response.xpath("//div[@class='zf_mainconlist1']").get()
        detail_text = ' '.join(response.xpath('//div[@class="zf_mainconlist1"]//text()').extract()).strip()
        bid_public_time = response.meta['time']
        po_public_time = self.normalize_datetime(bid_public_time)
        contentUrl = response.meta['url']
        bid_id = get_md5(contentUrl)
        item = BidScrapyProjectItem()
        item['bid_id'] = bid_id
        item['bid_url'] = contentUrl
        item['bid_province'] = '辽宁省'
        item['bid_city'] = response.meta['city']
        item['bid_category'] = '产权交易'
        item['bid_info_type'] = response.meta['two_title']
        item['bid_name'] = response.meta['title']
        item['bid_public_time'] = po_public_time
        item['bid_html_con'] = detail_htlm
        item['bid_content'] = detail_text
        item['website_name'] = self.website_name
        item['website_url'] =self.website_url
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