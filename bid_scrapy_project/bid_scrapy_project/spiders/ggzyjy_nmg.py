#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/6/19 16:48
@Author : xushaowei
@File : ggzyjy_nmg.py
@Desc : 内蒙古公共资源交易网
@Software: PyCharm
"""
import logging
import time

import pandas as pd
import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class GgzyjyNmgSpider(scrapy.Spider):
    name = "ggzyjy_nmg"
    start_urls = "https://ggzyjy.nmg.gov.cn/jyxx/jsgcZbgg"
    website_name = '内蒙古自治区公共资源交易网'
    website_url = 'https://ggzyjy.nmg.gov.cn/'
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list_page,
            dont_filter=True
        )

    def parse_list_page(self, response):
        panel_list = response.xpath('//ul[@class="lv1-ul"]//li[@class="lv1-li"]')
        for panel in panel_list:
            one_title = panel.xpath('./span/a/text()').get()
            nav_links = panel.xpath('./ul/li')
            for nav_link in nav_links:
                for page_i in range(0, 4):
                    two_title = nav_link.xpath("./a/text()").get()
                    url_min = nav_link.xpath("./a/@href").get()
                    url = 'https://ggzyjy.nmg.gov.cn' + url_min
                    meta = {"one_title": one_title, "two_title": two_title, "url": url}
                    if '/zfcg/' in url_min:
                        for page in range(1, 4):
                            data = {
                                "currentPage": str(page),
                                "industriesTypeCode": '000',
                                "time": '',
                                "scrollValue": '857',
                                "bulletinName": '',
                                "area": '',
                                "startTime": '',
                                "endTime": '',
                            }
                            url_text = 'https://ggzyjy.nmg.gov.cn/jyxx/zfcg/cggg'
                            yield scrapy.FormRequest(url_text, formdata=data, callback=self.parse_zfcg_list, meta=meta, dont_filter=True)
                    else:
                        pass
                        for page in range(1, 4):
                            data = {
                                "currentPage": str(page),
                                "industriesTypeCode": '000',
                                "time": '',
                                "scrollValue": '857',
                                "bulletinName": '',
                                "area": '',
                                "startTime": '',
                                "endTime": '',
                            }
                            url_text = 'https://ggzyjy.nmg.gov.cn/jyxx/zfcg/cggg'
                            yield scrapy.FormRequest(url_text, formdata=data, callback=self.parse_ztb_list, meta=meta, dont_filter=True)

    def parse_ztb_list(self, response):
        datas_tr = response.xpath('//table//tr')
        for data_tr in datas_tr:
            try:
                detail_urls = data_tr.xpath('.//a/@href').get()
                detail_title = data_tr.xpath('.//a/text()').get()
                time = data_tr.xpath('./td/text()').getall()[-1]
                if '\r\n' in time:
                    time = time.replace(' ', '').replace('\r\n', '').replace('\t', '')
                one_title = response.meta["one_title"]
                two_title = response.meta["two_title"]
                url = 'https://ggzyjy.nmg.gov.cn' + detail_urls
                meta = {"list_url": url, "title": detail_title.replace(' ', '').replace('\r\n', '').replace('\t', ''),
                        "one_title": one_title, "two_title": two_title, "time": time}
                yield scrapy.Request(url, callback=self.parse_ztb_detail, meta=meta)
            except Exception as e:
                logging.debug(e)

    def parse_zfcg_list(self, response):
        datas_tr = response.xpath('//table//tr')
        for data_tr in datas_tr:
            try:
                detail_urls = data_tr.xpath('.//a/@href').get()
                detail_title = data_tr.xpath('.//a/text()').get()
                time = data_tr.xpath('./td/text()').getall()[-1]
                if '\r\n' in time:
                    time = time.replace(' ', '').replace('\r\n', '').replace('\t', '')
                one_title = response.meta["one_title"]
                two_title = response.meta["two_title"]
                url = 'https://ggzyjy.nmg.gov.cn' + detail_urls
                meta = {"list_url": url, "title": detail_title.replace(' ', '').replace('\r\n', '').replace('\t', ''),
                        "one_title": one_title, "two_title": two_title, "time": time}
                yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta)
            except Exception as e:
                logging.debug(e)

    def parse_ztb_detail(self, response):
        detail_htlm = response.xpath('//div[@class="content"]').get()
        detail_text = ' '.join(response.xpath('//div[@class="content"]//text()').extract()).strip()
        bid_public_time1 = response.meta['time']
        bid_public_time = self.normalize_datetime(bid_public_time1)
        contentUrl = response.meta['list_url']
        bid_id = get_md5(contentUrl)
        item = BidScrapyProjectItem()
        item['bid_id'] = bid_id
        item['bid_url'] = contentUrl
        item['bid_province'] = '内蒙古自治区'
        item['bid_category'] = response.meta['one_title']
        item['bid_info_type'] = response.meta['two_title']
        item['bid_name'] = response.meta['title']
        item['bid_public_time'] = bid_public_time
        item['bid_html_con'] = detail_htlm
        item['bid_content'] = detail_text
        item['website_name'] = self.website_name
        item['website_url'] =self.website_url
        item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        yield item
    def parse_zfcg_detail(self, response):
        detail_htlm = response.xpath('//div[@class="content"]').get()
        detail_text = ' '.join(response.xpath('//div[@class="content"]//text()').extract()).strip()
        bid_public_time1 = response.meta['time']
        po_public_time = self.normalize_datetime(bid_public_time1)
        contentUrl = response.meta['list_url']
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item['po_id'] = po_id
        item['bid_url'] = contentUrl
        item['po_province'] = '内蒙古自治区'
        item['po_category'] = response.meta['one_title']
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