#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/17 16:50
@Author : xushaowei
@File : other_jiugangbid.py
@Desc :
@Software:PyCharm
"""
import logging
import time

import pandas as pd
import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class GgzyjyNmgSpider(scrapy.Spider):
    name = "other_chinagoldgroup"
    start_urls = "http://eps.jiugangbid.com:8000/f/tenderannquainqueryanns/tenderannquainqueryanns/findAnnoInfoList?inward=&selectedProjectType=1&projectName=&dataType=0"
    website_name = '酒钢公共交易平台'
    website_url = 'http://eps.jiugangbid.com'
    urls_data = [{"url": "http://eps.jiugangbid.com:8000/f/newservertrade/purchasingforecast?inside=", "val": "1", "type": "采购预告"},
                {"url": "http://eps.jiugangbid.com:8000/f/tenderannquainqueryanns/tenderannquainqueryanns/NewannquainList?tenderMode=2&projectName=&displaytype=secondLevel", "val": "2", "type": "公开招标"},
                {"url": "http://eps.jiugangbid.com:8000/f/tenderannquainqueryanns/tenderannquainqueryanns/NewannquainList?tenderMode=3&projectName=&displaytype=secondLevel", "val": "3", "type": "竞争性谈判"},
                {"url": "http://eps.jiugangbid.com:8000/f/tenderannquainqueryanns/tenderannquainqueryanns/NewannquainList?tenderMode=4&projectName=&displaytype=secondLevel", "val": "4", "type": "竞争性磋商"},
                {"url": "http://eps.jiugangbid.com:8000/f/enquiry", "val": "5", "type": "询价"},
                {"url": "http://eps.jiugangbid.com:8000/f/sunAll", "val": "6", "type": "竞价"},
                {"url": "http://eps.jiugangbid.com:8000/f/auction", "val": "7", "type": "竞卖"}]
    def start_requests(self):
        for url_data in self.urls_data:
            url = url_data.get('url')
            val = url_data.get('val')
            type = url_data.get('type')
            item = {"type": type}
            for page in range(1, 3):
                data = f'pageNo={page}&pageSize=20&listType={val}&dataType=0&pageType=item&codeProjectName=&projectName='
                headers = {
                    "Host": "eps.jiugangbid.com:8000",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                }
                yield scrapy.Request(url=url, body=data, method='POST', callback=self.parse_list_page, meta=item,
                                     headers=headers, dont_filter=True)

    def parse_list_page(self, response):
        lists = response.xpath('//dl')
        for list in lists:
            detali_url = list.xpath('.//a/@href').get()
            detali_title = list.xpath('.//a/text()').get()
            LeftTime = list.xpath('.//span[@class="gsPropertyLeftTime"]/text()').get()
            url = 'http://eps.jiugangbid.com:8000' + detali_url
            item = {"list_url": url, "tow_title": response.meta['type'], "title": detali_title.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').replace(' ', ''), "time": LeftTime}
            yield scrapy.Request(url, callback=self.parse_ztb_detail, meta=item)


    def parse_ztb_detail(self, response):
        detail_htlm = response.xpath('//div[@class="jxTradingMainLayer clear"]').get()
        detail_text = ' '.join(response.xpath('//div[@class="jxTradingMainLayer clear"]//text()').extract()).strip()
        bid_public_time1 = response.meta['time']
        po_public_time = self.normalize_datetime(bid_public_time1)
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