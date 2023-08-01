#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/6/27 17:00
@Author : xushaowei
@File : ggzyjy_jining.py
@Desc :
@Software:PyCharm
"""
import time

import pandas as pd
import requests
import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class GgzyjyNmgSpider(scrapy.Spider):
    name = "ggzyjy_jining"
    start_urls = "https://jnggzy.jnzbtb.cn:4430/JiNing/Bulletins?CategoryCode=536"
    website_name = '济宁公共资源交易网'
    website_url = 'https://jnggzy.jnzbtb.cn'
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list_page,
            dont_filter=True
        )

    def parse_list_page(self, response):
        panel_list = response.xpath('//div[@id="myAccordion"]//div[@class="panel"]')
        for panel in panel_list:
            one_title = panel.xpath('./div[@class="column-header"]/a[@data-toggle="collapse"]/text()').extract_first()
            nav_links = panel.xpath('.//a[@class="nav-link"]')
            if '政府采购' in one_title:
                for nav_link in nav_links:
                    for page_i in range(0, 60, 20):
                        two_title = nav_link.xpath(".//span[@class='title']/text()").extract_first().replace(' ', '').replace('\r\n', '')
                        post_url = 'https://jnggzy.jnzbtb.cn:4430/api/services/app/stPrtBulletin/GetBulletinList'
                        data_id = nav_link.xpath("./@data-id").extract_first()
                        cookies = response.headers.getlist('Set-Cookie')
                        r_token = cookies[4].decode().split('__RequestVerificationToken=')[1].split('; path=/; HttpOnly')[0]
                        Token = cookies[5].decode().split('XSRF-TOKEN=')[1].split('; path=/')[0]
                        data = '{"skipCount":%s,"maxResultCount":20,"categoryCode":"%s","includeAllSite":false,"FilterText":"","tenantId":"3"}' % (
                        page_i, data_id)
                        meta = {"one_title": one_title, "two_title": two_title}
                        headers = {
                            "Content-Type": "application/json",
                            "Cookie": f"__RequestVerificationToken={r_token}; XSRF-TOKEN={Token}",
                            "Host": "jnggzy.jnzbtb.cn:4430",
                            "Referer": f"https://jnggzy.jnzbtb.cn:4430/JiNing/Bulletins?CategoryCode={data_id}",
                            "X-Xsrf-Token": Token
                        }
                        yield scrapy.Request(post_url, method='POST', body=data, headers=headers, callback=self.parse_zfcg_list, meta=meta, dont_filter=True)
            else:
                for nav_link in nav_links:
                    for page_i in range(0, 60, 20):
                        two_title = nav_link.xpath(".//span[@class='title']/text()").extract_first().replace(' ', '').replace('\r\n', '')
                        post_url = 'https://jnggzy.jnzbtb.cn:4430/api/services/app/stPrtBulletin/GetBulletinList'
                        data_id = nav_link.xpath("./@data-id").extract_first()
                        cookies = response.headers.getlist('Set-Cookie')
                        r_token = cookies[4].decode().split('__RequestVerificationToken=')[1].split('; path=/; HttpOnly')[0]
                        Token = cookies[5].decode().split('XSRF-TOKEN=')[1].split('; path=/')[0]
                        if '建设工程' in one_title:
                            data = '{"skipCount":%s,"maxResultCount":20,"categoryCode":"%s","includeAllSite":false,"FilterText":"","tenantId":"3","regionId":"0","tenderProjectType":""}' % (
                        page_i, data_id)
                        else:
                            data = '{"skipCount":%s,"maxResultCount":20,"categoryCode":"%s","includeAllSite":false,"FilterText":"","tenantId":"3"}' % (
                                page_i, data_id)
                        meta = {"one_title": one_title, "two_title": two_title}
                        headers = {
                                    "Content-Type": "application/json",
                                    "Cookie": f"__RequestVerificationToken={r_token}; XSRF-TOKEN={Token}",
                                    "Host": "jnggzy.jnzbtb.cn:4430",
                                    "Referer": f"https://jnggzy.jnzbtb.cn:4430/JiNing/Bulletins?CategoryCode={data_id}",
                                    "X-Xsrf-Token": Token
                                }
                        yield scrapy.Request(post_url, method='POST', body=data, headers=headers, callback=self.parse_ztb_list, meta=meta, dont_filter=True)


    def parse_ztb_list(self, response):
        list_json_data = response.json()
        list_items = list_json_data.get('result').get('items')
        for list_item in list_items:
            categoryCode = list_item.get('categoryCode')
            releaseDate = list_item.get('releaseDate')
            title = list_item.get('title')
            list_id = list_item.get('id')
            url = f'https://jnggzy.jnzbtb.cn:4430/JiNing/Bulletins/Detail/{list_id}/?CategoryCode={categoryCode}'
            meta = {"url": url, "title": title, "releaseDate": releaseDate, "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
            yield scrapy.Request(url, callback=self.parse_ztb_detail, meta=meta)

    def parse_zfcg_list(self, response):
        list_json_data = response.json()
        list_items = list_json_data.get('result').get('items')
        for list_item in list_items:
            categoryCode = list_item.get('categoryCode')
            releaseDate = list_item.get('releaseDate')
            title = list_item.get('title')
            list_id = list_item.get('id')
            url = f'https://jnggzy.jnzbtb.cn:4430/JiNing/Bulletins/Detail/{list_id}/?CategoryCode={categoryCode}'
            meta = {"url": url, "title": title, "releaseDate": releaseDate, "one_title": response.meta['one_title'],
                    "two_title": response.meta['two_title']}
            yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta)

    def parse_ztb_detail(self, response):
        detail_htlm = response.xpath("//div[@class='ctn-detail']").get()
        detail_text = ' '.join(response.xpath('//div[@class="ctn-detail"]//text()').extract()).strip()
        bid_public_time = response.meta['releaseDate']
        po_public_time = self.normalize_datetime(bid_public_time)
        contentUrl = response.meta['url']
        bid_id = get_md5(contentUrl)
        item = BidScrapyProjectItem()
        item['bid_id'] = bid_id
        item['bid_url'] = contentUrl
        item['bid_province'] = '山东省'
        item['bid_city'] = '济宁市'
        item['bid_category'] = response.meta['one_title']
        item['bid_info_type'] = response.meta['two_title']
        item['bid_name'] = response.meta['title']
        item['bid_public_time'] = po_public_time
        item['bid_html_con'] = detail_htlm
        item['bid_content'] = detail_text
        item['website_name'] = self.website_name
        item['website_url'] =self.website_url
        item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        yield item
    def parse_zfcg_detail(self, response):
        detail_htlm = response.xpath("//div[@class='ctn-detail']").get()
        detail_text = ' '.join(response.xpath('//div[@class="ctn-detail"]//text()').extract()).strip()
        bid_public_time = response.meta['releaseDate']
        po_public_time = self.normalize_datetime(bid_public_time)
        contentUrl = response.meta['url']
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item['po_id'] = po_id
        item['bid_url'] = contentUrl
        item['po_province'] = '山东省'
        item['po_city'] = '济宁市'
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