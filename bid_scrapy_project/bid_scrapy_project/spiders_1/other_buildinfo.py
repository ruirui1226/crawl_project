#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/20 13:39
@Author : xushaowei
@File : other_buildinfo.py
@Desc :
@Software:PyCharm
"""
import logging
import time

# import pandas as pd
import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

from bid_scrapy_project.common.common import format_time


class GgzyjyNmgSpider(scrapy.Spider):
    name = "other_buildinfo"
    start_urls = [{"url": "http://www.buildinfo.com.cn/zb.do?method=list", "type": "招标公示"}, {"url": "http://www.buildinfo.com.cn/stock.do?method=list", "type": "采购公示"}]
    website_name = '广东建设工程信息网'
    website_url = 'http://www.buildinfo.com.cn'
    def start_requests(self):
        for st_url in self.start_urls:
            url = st_url.get('url')
            url_ty = st_url.get('type')
            if '招标公示' in url_ty:
                for page in range(1, 3):
                    data = f'typeName=&info_type=3&zb_type=&stype=&keyword=&kw=&sarea=&page={page}&pageText=1'
                    headers = {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Host": "www.buildinfo.com.cn"
                    }
                    item = {"bid_category": url_ty}
                    yield scrapy.Request(url=url, body=data, method='POST', callback=self.parse_zb_list, meta=item,
                                         headers=headers, dont_filter=True)
            else:
                for page in range(1, 3):
                    data = f'skind=3&stock_type=&keyword=&kw=&sarea=&page={page}&pageText=1'
                    headers = {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Host": "www.buildinfo.com.cn"
                    }
                    item = {"bid_category": url_ty}
                    yield scrapy.Request(url=url, body=data, method='POST', callback=self.parse_cg_list, meta=item,
                                         headers=headers, dont_filter=True)

    def parse_zb_list(self, response):
        lists_url = response.xpath('//td[@class="box_5"]//tr')
        for list_url in lists_url:
            try:
                detail_urls = list_url.xpath('.//a/@href').get()
                detail_title = list_url.xpath('.//a/@title').get()
                time = list_url.xpath('.//td[last()]/text()').get()
                type = list_url.xpath('.//td[last()-1]/text()').get()
                city = list_url.xpath('.//td[last()-2]/text()').get()
                meta = {"list_url": self.website_url + detail_urls, "bid_category": response.meta['bid_category'], "title": detail_title.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').replace(' ', ''), "time": time, "bid_info_type": type, "city": city}
                yield scrapy.Request(url=self.website_url + detail_urls, callback=self.parse_ztb_detail, meta=meta)
            except Exception as e:
                logging.debug(e)

    def parse_cg_list(self, response):
        lists_url = response.xpath('//td[@class="box_5"]//tr')
        for list_url in lists_url:
            try:
                detail_urls = list_url.xpath('.//a/@href').get()
                detail_title = list_url.xpath('.//a/font/text()').get()
                time = list_url.xpath('.//td[last()]/text()').get()
                type = list_url.xpath('.//td[last()-1]/text()').get()
                city = list_url.xpath('.//td[last()-2]/text()').get()
                meta = {"list_url": self.website_url + detail_urls, "bid_category": response.meta['bid_category'],
                        "title": detail_title.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').replace(' ', ''), "time": time, "bid_info_type": type, "city": city}
                yield scrapy.Request(url=self.website_url + detail_urls, callback=self.parse_cg_detail, meta=meta)
            except Exception as e:
                logging.debug(e)


    def parse_ztb_detail(self, response):
        detail_htmls = response.xpath('//td[@class="box_5"]').getall()
        html = detail_htmls[0] + detail_htmls[1]
        province = response.xpath('//td[@class="box_5"]//tr')[3].xpath('.//td[2]/text()').get()
        detail_text = ' '.join(response.xpath('//td[@class="box_5"]//text()').extract()).strip()
        bid_public_time1 = response.meta['time']
        bid_public_time = format_time(bid_public_time1)
        contentUrl = response.meta['list_url']
        bid_id = get_md5(contentUrl)
        item = BidScrapyProjectItem()
        item['bid_id'] = bid_id
        item['bid_url'] = contentUrl
        item['bid_province'] = province
        item['bid_city'] = response.meta['city']
        item['bid_city'] = item['bid_city'].replace('[','').replace('[',']')
        # item['bid_category'] = response.meta['bid_category']
        item['bid_info_type'] = response.meta['bid_category']
        item['bid_name'] = response.meta['title']
        item['bid_public_time'] = bid_public_time
        item['bid_html_con'] = html
        item['bid_content'] = detail_text
        item['website_name'] = self.website_name
        item['website_url'] =self.website_url
        item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        yield item

    def parse_cg_detail(self, response):
        detail_htmls = response.xpath('//td[@class="box_5"]').getall()
        html = detail_htmls[0] + detail_htmls[1]
        province = response.xpath('//td[@class="box_5"]//tr')[3].xpath('.//td[2]/text()').get()
        detail_text = ' '.join(response.xpath('//td[@class="box_5"]//text()').extract()).strip()
        bid_public_time1 = response.meta['time']
        po_public_time = format_time(bid_public_time1)
        contentUrl = response.meta['list_url']
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item['po_id'] = po_id
        item['bid_url'] = contentUrl
        item['po_province'] = province
        item['po_city'] = response.meta['city']
        item['po_city'] = item['po_city'].replace('[','').replace('[',']')
        # item['po_category'] = response.meta['bid_category']
        item['po_info_type'] = response.meta['bid_category']
        item['po_public_time'] = po_public_time
        item['bo_name'] = response.meta['title']
        item['po_html_con'] = html
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