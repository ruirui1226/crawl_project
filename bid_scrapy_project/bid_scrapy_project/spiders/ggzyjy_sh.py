#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/6/25 13:53
@Author : xushaowei
@File : ggzyjy_sh.py
@Desc :
@Software:PyCharm
"""
import logging
import re
import time

import pandas as pd
import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class GgzyjyNmgSpider(scrapy.Spider):
    name = "ggzyjy_sh"
    start_urls = "https://www.shggzy.com/jyxxgc"
    website_name = '上海市公共资源交易中心'
    website_url = 'https://www.shggzy.com'
    custom_settings = {
        "REDIRECT_ENABLED": False,
        # "DUPEFILTER_CLASS": 'scrapy.dupefilters.BaseDupeFilter'
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list_page,
            dont_filter=True
        )

    def parse_list_page(self, response):
        panel_list = response.xpath('//ul[@class="content_ul-left"]//li')
        for panel in panel_list:
            one_title = panel.xpath("./span/text()").get()
            nav_links = panel.xpath("./@onclick").get()
            url_min = re.findall("location.href='(.*?)'", nav_links)[0]
            url = self.website_url + url_min
            meta = {"one_title": one_title, "url": url}
            yield scrapy.FormRequest(url, callback=self.parse_list_paging, meta=meta, dont_filter=True)

    def parse_list_paging(self, response):
        panel_list = response.xpath('//ul[@data-in="channelId"]//li')
        cExt = re.findall(""".*var cExt = '(.*?)';.*""", response.text)[0]
        for panel in panel_list:
            if '全部' == panel.xpath('./text()').get():
                pass
            elif 'jyxxzc' in response.url or 'jyxxyp' in response.url or 'jyxxwzcg' in response.url:
                two_title = panel.xpath("./text()").get()
                data_val = panel.xpath("./@data-val").get()
                timestamp = int(time.time())
                for page in range(1, 4):
                    url = f'https://www.shggzy.com/search/queryContents_{page}.jhtml?title=&channelId={data_val}&origin=&inDates=4000&ext=&timeBegin=&timeEnd=&ext1=&ext2=&cExt={cExt}'
                    meta = {"one_title": response.meta['one_title'], "url": response.meta['url'],
                            "two_title": two_title, "cExt": cExt}
                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                        'Connection': 'keep-alive',
                        'Host': 'www.shggzy.com',
                        'Cookie': f"_site_id_cookie=1; JIDENTITY=b337f298-8231-49f5-bcce-89c7bfa225f6; Hm_lvt_ddd51655888df4f02c24c55810416e80={timestamp}; Hm_lpvt_ddd51655888df4f02c24c55810416e80={timestamp}",
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-User': '?1',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }
                    yield scrapy.Request(url, callback=self.parse_zfcg_list, headers=headers, meta=meta, dont_filter=True)
            else:
                two_title = panel.xpath("./text()").get()
                data_val = panel.xpath("./@data-val").get()
                for page in range(1, 4):
                    url = f'https://www.shggzy.com/search/queryContents_{page}.jhtml?title=&channelId={data_val}&origin=&inDates=4000&ext=&timeBegin=&timeEnd=&ext1=&ext2=&cExt={cExt}'
                    meta = {"one_title": response.meta['one_title'], "url_list": url, "two_title": two_title, "cExt": cExt}
                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                        'Connection': 'keep-alive',
                        'Host': 'www.shggzy.com',
                        'Cookie': "_site_id_cookie=1; JIDENTITY=b337f298-8231-49f5-bcce-89c7bfa225f6;",
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-User': '?1',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }
                    yield scrapy.Request(url, callback=self.parse_ztb_list, headers=headers, meta=meta, dont_filter=True)


    def parse_ztb_list(self, response):
        try:
            list_urls = response.xpath('//div[@id="allList"]//ul//li')
            cExt = re.findall(""".*var cExt = '(.*?)';.*""", response.text)[0]
            for list_url in list_urls:
                detail_urls = list_url.xpath('./@onclick').get()
                detail_url = re.findall("open\('(.*?)\?cExt", detail_urls)[0]
                detail_title = list_url.xpath('./span[@class="cs-span2"]/text()').get()
                detail_date = list_url.xpath('./span[last()]/text()').get()
                title = detail_title.replace(' ', '').replace('\r\n', '').replace('\t', '')
                one_title = response.meta["one_title"]
                two_title = response.meta["two_title"]
                url = self.website_url + detail_url + '?cExt=' + cExt + '&isIndex='
                meta = {"list_url": url, "title": title, "detail_date": detail_date,
                        "one_title": one_title, "two_title": two_title}
                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Host': 'www.shggzy.com',
                    'Cookie': "_site_id_cookie=1; JIDENTITY=b337f298-8231-49f5-bcce-89c7bfa225f6;",
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                }
                yield scrapy.Request(url, callback=self.parse_ztb_detail, meta=meta, headers=headers)
        except Exception as e:
            logging.error(e)

    def parse_zfcg_list(self, response):
        try:
            list_urls = response.xpath('//div[@id="allList"]//ul//li')
            cExt = re.findall(""".*var cExt = '(.*?)';.*""", response.text)[0]
            for list_url in list_urls:
                detail_urls = list_url.xpath('./@onclick').get()
                detail_url = re.findall("open\('(.*?)\?cExt", detail_urls)[0]
                detail_title = list_url.xpath('./span[@class="cs-span2"]/text()').get()
                detail_date = list_url.xpath('./span[last()]/text()').get()
                title = detail_title.replace(' ', '').replace('\r\n', '').replace('\t', '')
                one_title = response.meta["one_title"]
                two_title = response.meta["two_title"]
                url = self.website_url + detail_url + '?cExt=' + cExt + '&isIndex='
                meta = {"list_url": url, "title": title, "detail_date": detail_date,
                        "one_title": one_title, "two_title": two_title}
                timestamp = int(time.time())
                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Host': 'www.shggzy.com',
                    'Cookie': f"_site_id_cookie=1; JIDENTITY=b337f298-8231-49f5-bcce-89c7bfa225f6; Hm_lvt_ddd51655888df4f02c24c55810416e80={timestamp}; Hm_lpvt_ddd51655888df4f02c24c55810416e80={timestamp}",
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                }
                yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta, headers=headers)
        except Exception as e:
            logging.error(e)

    def parse_ztb_detail(self, response):
        detail_htlm = response.xpath('//div[@class="content"]').get()
        detail_text = ' '.join(response.xpath('//div[@class="content"]//text()').extract()).strip()
        public_time = response.meta['detail_date']
        bid_public_time = self.normalize_datetime(public_time)
        contentUrl = response.meta['list_url']
        bid_id = get_md5(contentUrl)
        item = BidScrapyProjectItem()
        item['bid_id'] = bid_id
        item['bid_url'] = contentUrl
        item['bid_province'] = '上海市'
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
        public_time = response.meta['detail_date']
        po_public_time = self.normalize_datetime(public_time)
        contentUrl = response.meta['list_url']
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item['po_id'] = po_id
        item['bid_url'] = contentUrl
        item['po_province'] = '上海市'
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
