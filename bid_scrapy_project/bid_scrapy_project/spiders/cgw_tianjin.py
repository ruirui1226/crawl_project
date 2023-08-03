#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/7/6 9:23
@Author : xushaowei
@File : cgw_tianjin.py
@Desc :
@Software:PyCharm
"""
import time

# import pandas as pd
import requests
import scrapy
from lxml import etree

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

from bid_scrapy_project.common.common import format_time


class GgzyjyNmgSpider(scrapy.Spider):
    name = "cgw_tianjin"
    start_urls = 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=view&view=Infor&id=1665&ver=2&st=1'
    website_name = '天津政府采购网'
    website_url = 'http://www.ccgp-tianjin.gov.cn'

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list_page,
            dont_filter=True
        )

    def parse_list_page(self, response):
        menu_lefts = response.xpath('//div[@class="menuWrap"]//ul[@style="display:block"]//li')
        # jsessionid = response.headers.getlist('Set-Cookie')[0].decode("utf-8").split(";")[0].split("=")[1]
        # topapp_cookie = response.headers.getlist('Set-Cookie')[1].decode("utf-8").split(";")[0].split("=")[1]
        for menu_left in menu_lefts:
            two_title = menu_left.xpath('./a[@class="twoHead"]/text()').get()
            ids = []
            urls = menu_left.xpath('./div[@class="twoWrap"]//a/@href').getall()
            for url in urls:
                id = url.split('&id=')[-1].split('&ver')[0]
                ids.append(id)
            for page in range(1, 4):
                for i in ids:
                    url = 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do'
                    data = f'method=view&page={page}&id={i}&step=1&view=Infor&ldateQGE=&ldateQLE='
                    headers = {
                            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                            "Host": "www.ccgp-tianjin.gov.cn",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                        }
                    res = requests.get(url=self.start_urls, headers=headers)
                    jsessionid = res.cookies.get('JSESSIONID')
                    topapp_cookie = res.cookies.get('TOPAPP_COOKIE')
                    item = {"two_title": two_title, "JSESSIONID": jsessionid, "TOPAPP_COOKIE": topapp_cookie}
                    headers = {
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Host": "www.ccgp-tianjin.gov.cn",
                        "Proxy-Connection": "keep-alive",
                        "Cookie": f"HttpOnly; HttpOnly; JSESSIONID={jsessionid}; TOPAPP_COOKIE={topapp_cookie}"
                    }
                    time.sleep(3)
                    yield scrapy.Request(url, body=data, method='POST', callback=self.parse_zfcg_list, headers=headers, meta=item, dont_filter=True)

    def parse_zfcg_list(self, response):
        dataLists = response.xpath('//ul[@class="dataList"]//li')
        jsessionid = response.meta['JSESSIONID']
        topapp_cookie = response.meta['TOPAPP_COOKIE']
        if len(dataLists) > 0:
            for dataList in dataLists:
                url_type = dataList.xpath('./a/@href').get()
                title = dataList.xpath('./a/@title').get()
                public_time = dataList.xpath('./span[@class="time"]/text()').get()
                url = self.website_url + url_type
                meta = {"list_url": url, "title": title, "two_title": response.meta['two_title'], "public_time": public_time}
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cache-Control": "max-age=0",
                    "Cookie": f"HttpOnly; JSESSIONID={jsessionid}; TOPAPP_COOKIE={topapp_cookie}; HttpOnly",
                    "Host": "www.ccgp-tianjin.gov.cn",
                    "Proxy-Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                }
                time.sleep(3)
                yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta, headers=headers)
        else:
            pass

    def parse_zfcg_detail(self, response):
        detail_htlm = response.xpath('//div[@id="content"]').get()
        detail_text = ' '.join(response.xpath('//div[@id="content"]//text()').extract()).strip()
        public_time = response.meta['public_time']
        po_public_time = format_time(public_time)
        contentUrl = response.meta['list_url']
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item['po_id'] = po_id
        item['bid_url'] = contentUrl
        item['po_province'] = '天津市'
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
    #
    #     normalized_time_str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    #     return normalized_time_str