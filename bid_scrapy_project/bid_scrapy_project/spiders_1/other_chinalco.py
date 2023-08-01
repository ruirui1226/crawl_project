#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/18 14:22
@Author : xushaowei
@File : other_chinalco.py
@Desc :
@Software:PyCharm
"""
import time

import pandas as pd
import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class GgzyjyNmgSpider(scrapy.Spider):
    name = "other_chinalco"
    website_name = '中国铝业公司电子采购交易系统'
    website_url = 'http://e-al.chinalco.com.cn'
    urls_data = [{"url": "http://sus.chalco.com.cn:8080/irj/servlet/prt/portal/prtroot/com.sap.portal.pagebuilder.IviewModeProxy?iview_id=pcd%3Aportal_content%2Fcom.chalco.Chalco%2Fcom.chalco.folder_view%2Fcom.chalco.fld_batch1%2Ftest.test%2Fnm_role.nm_role%2Fnm_workset.nm_workset%2Fgsjzhaobiao&iview_mode=default&NavigationTarget=navurl://3366d9825f90d803ac8189d3e9c046f7&typee=A&statue=B"},
                {"url": "http://sus.chalco.com.cn:8080/irj/servlet/prt/portal/prtroot/com.sap.portal.pagebuilder.IviewModeProxy?iview_id=pcd%3Aportal_content%2Fcom.chalco.Chalco%2Fcom.chalco.folder_view%2Fcom.chalco.fld_batch1%2Ftest.test%2Fnm_role.nm_role%2Fnm_workset.nm_workset%2Fgsjzhaobiao&iview_mode=default&NavigationTarget=navurl://3366d9825f90d803ac8189d3e9c046f7&typee=B&statue=B"},
                {"url": "http://sus.chalco.com.cn:8080/irj/servlet/prt/portal/prtroot/com.sap.portal.pagebuilder.IviewModeProxy?iview_id=pcd%3Aportal_content%2Fcom.chalco.Chalco%2Fcom.chalco.folder_view%2Fcom.chalco.fld_batch1%2Ftest.test%2Fnm_role.nm_role%2Fnm_workset.nm_workset%2Fgsjzhaobiao&iview_mode=default&NavigationTarget=navurl://3366d9825f90d803ac8189d3e9c046f7&typee=C&statue=B"}]
    def start_requests(self):
        for url_data in self.urls_data:
            url_type = url_data.get('url')
            for page in range(1, 3):
                data = f'&title=&basedate=&enddate=&showItemNumber=20&pageNumber={page}'
                url = url_type + data
                yield scrapy.Request(url=url, callback=self.parse_list_page, dont_filter=True)

    def parse_list_page(self, response):
        lists = response.xpath('//tbody')[3].xpath('.//tr')
        for list in lists:
            detali_url = list.xpath('.//a/@href').get()
            detali_title = list.xpath('.//a/text()').get()
            LeftTime = list.xpath('.//td[last()]/text()').get()
            item = {"list_url": detali_url, "title": detali_title.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').replace(' ', ''), "time": LeftTime}
            yield scrapy.Request(detali_url, callback=self.parse_ztb_detail, meta=item)


    def parse_ztb_detail(self, response):
        detail_htlm = response.xpath('//table')[1].get()
        detail_text = ' '.join(response.xpath('//table[2]//text()').extract()).strip()
        bid_public_time1 = response.meta['time']
        po_public_time = self.normalize_datetime(bid_public_time1)
        contentUrl = response.meta['list_url']
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item['po_id'] = po_id
        # item['bid_url'] = contentUrl
        item['po_category'] = '招标公告'
        item['po_public_time'] = po_public_time
        item['bo_name'] = '招标'
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