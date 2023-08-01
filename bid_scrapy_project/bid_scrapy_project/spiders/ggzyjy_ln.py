#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/4 10:34
@Author : xushaowei
@File : ggzyjy_ln.py
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
    name = "ggzyjy_liaoning"
    website_name = '辽宁省公共资源交易网'
    website_url = 'http://ggzy.ln.gov.cn'
    type_codes = [{"city": "省本级", "data_code": '149559', "type": '招标公告'},
                {"city": "省本级", "data_code": '154004', "type": '资格预审'},
                {"city": "省本级", "data_code": '149560', "type": '变更公告'},
                {"city": "省本级", "data_code": '149561', "type": '中标候选人公示'},
                {"city": "省本级", "data_codee": '149562', "type": '中标结果公告'},
                {"city": "省本级", "data_code": '153299', "type": '特殊事项公告'},
                {"city": "沈阳市", "data_code": '162316', "type": '招标计划'},
                {"city": "沈阳市", "data_code": '152821', "type": '招标公告'},
                {"city": "沈阳市", "data_code": '152823', "type": '中标候选人公示'},
                {"city": "沈阳市", "data_code": '152824', "type": '中标结果公告'},
                {"city": "大连市", "data_code": '152845', "type": '招标公告'},
                {"city": "大连市", "data_code": '152846', "type": '变更公告'},
                {"city": "大连市", "data_code": '152847', "type": '中标候选人公示'},
                {"city": "大连市", "data_code": '152848', "type": '中标结果公告'},
                {"city": "大连市", "data_code": '158875', "type": '竣工销号公示'},
                {"city": "鞍山市", "data_code": '152868', "type": '招标公告'},
                {"city": "鞍山市", "data_code": '152870', "type": '中标候选人公示'},
                {"city": "鞍山市", "data_code": '152871', "type": '中标结果公告'},
                {"city": "抚顺市", "data_code": '152891', "type": '招标公告'},
                {"city": "抚顺市", "data_code": '152892', "type": '变更公告'},
                {"city": "抚顺市", "data_code": '152893', "type": '中标候选人公示'},
                {"city": "抚顺市", "data_code": '152894', "type": '中标结果公告'},
                {"city": "本溪市", "data_code": '152914', "type": '招标公告'},
                {"city": "本溪市", "data_code": '152916', "type": '中标候选人公示'},
                {"city": "本溪市", "data_code": '152917', "type": '中标结果公告'},
                {"city": "丹东市", "data_code": '152937', "type": '招标公告'},
                {"city": "丹东市", "data_code": '152938', "type": '变更公告'},
                {"city": "丹东市", "data_code": '152939', "type": '中标候选人公示'},
                {"city": "丹东市", "data_code": '152940', "type": '中标结果公告'},
                {"city": "锦州市", "data_code": '162314', "type": '招标计划'},
                {"city": "锦州市", "data_code": '152960', "type": '招标公告'},
                {"city": "锦州市", "data_code": '152961', "type": '变更公告'},
                {"city": "锦州市", "data_code": '152962', "type": '中标候选人公示'},
                {"city": "锦州市", "data_code": '152963', "type": '中标结果公告'},
                {"city": "锦州市", "data_code": '162315', "type": '废标公示'},
                {"city": "营口市", "data_code": '152983', "type": '招标公告'},
                {"city": "营口市", "data_code": '152984', "type": '变更公告'},
                {"city": "营口市", "data_code": '152985', "type": '中标候选人公示'},
                {"city": "营口市", "data_code": '152986', "type": '中标结果公告'},
                {"city": "阜新市", "data_code": '153006', "type": '招标公告'},
                {"city": "阜新市", "data_code": '153008', "type": '中标候选人公示'},
                {"city": "阜新市", "data_code": '153009', "type": '中标结果公告'},
                {"city": "辽阳市", "data_code": '153029', "type": '招标公告'},
                {"city": "辽阳市", "data_code": '153030', "type": '变更公告'},
                {"city": "辽阳市", "data_code": '153031', "type": '中标候选人公示'},
                {"city": "辽阳市", "data_code": '153032', "type": '中标结果公告'},
                {"city": "铁岭市", "data_code": '153052', "type": '招标公告'},
                {"city": "铁岭市", "data_code": '153054', "type": '中标候选人公示'},
                {"city": "铁岭市", "data_code": '153055', "type": '中标结果公告'},
                {"city": "朝阳市", "data_code": '153075', "type": '招标公告'},
                {"city": "朝阳市", "data_code": '153077', "type": '中标候选人公示'},
                {"city": "朝阳市", "data_code": '153078', "type": '中标结果公告'},
                {"city": "朝阳市", "data_code": '162273', "type": '澄清/特殊事项'},
                {"city": "盘锦市", "data_code": '153098', "type": '招标公告'},
                {"city": "盘锦市", "data_code": '153100', "type": '中标候选人公示'},
                {"city": "盘锦市", "data_code": '153101', "type": '中标结果公告'},
                {"city": "葫芦岛市", "data_code": '153121', "type": '招标公告'},
                {"city": "葫芦岛市", "data_code": '153122', "type": '变更公告'},
                {"city": "葫芦岛市", "data_code": '153123', "type": '中标候选人公示'},
                {"city": "葫芦岛市", "data_code": '153124', "type": '中标结果公告'},
                {"city": "沈抚示范区", "data_code": '158856', "type": '招标公告'},
                {"city": "沈抚示范区", "data_code": '158858', "type": '中标候选人公示'},
                {"city": "沈抚示范区", "data_code": '158859', "type": '中标结果公告'},
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
            for data in data_json.get('datas'):
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
        item['bid_category'] = '工程建设'
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