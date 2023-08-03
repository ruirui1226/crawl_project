#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/4 17:14
@Author : xushaowei
@File : ggzyjy_ln_cg.py
@Desc :
@Software:PyCharm
"""
import json
import time

# import pandas as pd
import requests
import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

from bid_scrapy_project.common.common import format_time


class GgzyjyNmgSpider(scrapy.Spider):
    name = "ggzyjy_liaoning_caigou"
    website_name = '辽宁省公共资源交易网'
    website_url = 'http://ggzy.ln.gov.cn'
    type_codes = [{"city": "省本级", "data_code": '149565', "type": '采购公告'},
                {"city": "省本级", "data_code": '153368', "type": '更正公告'},
                {"city": "省本级", "data_code": '149567', "type": '结果公告'},

                {"city": "沈阳市", "data_code": '152832', "type": '采购公告'},
                {"city": "沈阳市", "data_code": '152834', "type": '结果公告'},

                {"city": "大连市", "data_code": '152856', "type": '采购公告'},
                {"city": "大连市", "data_code": '152857', "type": '更正公告'},
                {"city": "大连市", "data_code": '152858', "type": '结果公告'},
                {"city": "大连市", "data_code": '162276', "type": '采购文件公示'},
                {"city": "大连市", "data_code": '162277', "type": '采购合同公示'},
                {"city": "大连市", "data_code": '162275', "type": '单一来源'},

                {"city": "鞍山市", "data_code": '152879', "type": '采购公告'},
                {"city": "鞍山市", "data_code": '152881', "type": '结果公告'},
                {"city": "鞍山市", "data_code": '162297', "type": '合同管理'},

                {"city": "本溪市", "data_code": '152925', "type": '采购公告'},
                {"city": "本溪市", "data_code": '152926', "type": '更正公告'},
                {"city": "本溪市", "data_code": '152927', "type": '结果公告'},

                {"city": "丹东市", "data_code": '152948', "type": '采购公告'},
                {"city": "丹东市", "data_code": '152949', "type": '更正公告'},
                {"city": "丹东市", "data_code": '152950', "type": '结果公告'},

                {"city": "锦州市", "data_code": '152971', "type": '采购公告'},
                {"city": "锦州市", "data_code": '152972', "type": '更正公告'},
                {"city": "锦州市", "data_code": '152973', "type": '结果公告'},

                {"city": "营口市", "data_code": '152994', "type": '采购公告'},
                {"city": "营口市", "data_code": '152995', "type": '更正公告'},
                {"city": "营口市", "data_code": '152996', "type": '结果公告'},

                {"city": "阜新市", "data_code": '153017', "type": '采购公告'},
                {"city": "阜新市", "data_code": '153018', "type": '更正公告'},
                {"city": "阜新市", "data_code": '153019', "type": '结果公告'},

                {"city": "辽阳市", "data_code": '153040', "type": '采购公告'},
                {"city": "辽阳市", "data_code": '153041', "type": '更正公告'},
                {"city": "辽阳市", "data_code": '153042', "type": '结果公告'},

                {"city": "铁岭市", "data_code": '153063', "type": '采购公告'},
                {"city": "铁岭市", "data_code": '153065', "type": '结果公告'},

                {"city": "朝阳市", "data_code": '153086', "type": '采购公告'},
                {"city": "朝阳市", "data_code": '153087', "type": '更正公告'},
                {"city": "朝阳市", "data_code": '153088', "type": '结果公告'},
                {"city": "朝阳市", "data_code": '162274', "type": '履约信息'},

                {"city": "盘锦市", "data_code": '153109', "type": '采购公告'},
                {"city": "盘锦市", "data_code": '153111', "type": '结果公告'},

                {"city": "葫芦岛市", "data_code": '153132', "type": '采购公告'},
                {"city": "葫芦岛市", "data_code": '153133', "type": '更正公告'},
                {"city": "葫芦岛市", "data_code": '153134', "type": '结果公告'},
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
        po_public_time = format_time(bid_public_time)
        contentUrl = response.meta['url']
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item['po_id'] = po_id
        item['bid_url'] = contentUrl
        item['po_province'] = '辽宁省'
        item['po_city'] = response.meta['city']
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
    #     normalized_time_str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    #     return normalized_time_str