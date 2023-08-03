#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 29/6/2023 下午2:50
@Author : xushaowei
@File : ggzyjy_hubei.py
@Desc :
@Software:PyCharm
"""
import re
import time
from datetime import datetime
from io import StringIO

# import pandas as pd
import requests
import scrapy
from lxml import etree

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

from bid_scrapy_project.common.common import format_time


class GgzyjyNmgSpider(scrapy.Spider):
    name = "ggzyjy_hubei"
    start_urls = "https://www.hbggzyfwpt.cn/jyxx/jsgcXmxx?currentArea=&businessTypeValue=0"
    website_name = '公共资源交易平台(湖北省)'
    website_url = 'https://www.hbggzyfwpt.cn'
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list_page,
            dont_filter=True
        )

    def parse_list_page(self, response):
        res_text = response.text
        url_detail_set = set()
        urlset = set()
        urldetail = set()
        urls = re.findall('.*url : "(.*?)",\s*data.*', res_text)
        details = re.findall('.*<a href=\\\\"(.*?=)"+.*', res_text)
        for url_type in urls:
            urlset.add(url_type)
        for detail in details:
            urldetail.add(detail)
        for url in urlset:
            if '/jyxx/qtjy/tdlzjggsNew' in url:
                set_data = {"urls": url, "details": '/jyxx/lqjy/cjgsDetail?guid='}
                url_detail_set.add(tuple(set_data.items()))
            if '/jyxx/zfbz/zfbzListNew' in url:
                set_data = {"urls": url, "details": '/jyxx/lqjy/crggDetail?guid='}
                url_detail_set.add(tuple(set_data.items()))
            if '/jyxx/zfcg/cghtsNew' in url:
                set_data = {"urls": url, "details": '/jyxx/zfcg/cghtDetail?guid='}
                url_detail_set.add(tuple(set_data.items()))
            for detail in urldetail:
                code = detail.split('Detail?')[0].split('/jyxx')[-1]
                if code in url:
                    set_data = {"urls": url, "details": detail}
                    url_detail_set.add(tuple(set_data.items()))
        for panel in url_detail_set:
            result = dict(panel)
            url = result.get('urls')
            if '/zfcg/' in url:
                if 'cggg' in url:
                    meta = {"urls": url, "details": result.get('details'), "one_title": '政府采购', "two_title": '采购公告'}
                if 'gzsxs' in url:
                    meta = {"urls": url, "details": result.get('details'), "one_title": '政府采购', "two_title": '更正事项'}
                if 'zbjggs' in url:
                    meta = {"urls": url, "details": result.get('details'), "one_title": '政府采购', "two_title": '采购结果'}
                if 'cghts' in url:
                    meta = {"urls": url, "details": result.get('details'), "one_title": '政府采购', "two_title": '采购合同'}
                if 'jgcfs' in url:
                    continue
                for page_i in range(1, 4):
                    post_url = self.website_url + url
                    data = f'currentPage={page_i}&pageSize=10&currentArea=001&area=000&publishTimeType=3&publishTimeStart=&publishTimeEnd=&bulletinTitle=&purchaserMode=99&purchaserModeType=0'
                    headers = {
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Host": "www.hbggzyfwpt.cn",
                        "Referer": f"https://www.hbggzyfwpt.cn{url}?currentArea=&businessTypeValue=0",
                    }
                    yield scrapy.Request(post_url, method='POST', body=data, headers=headers, callback=self.parse_zfcg_list, meta=meta, dont_filter=True)
            elif '/jyxxAjax/' in url:
                if 'Xmba' in url:
                    continue
                if 'jsgcXmxx' in url:
                    meta = {"urls": url, "details": result.get('details'), "one_title": '工程建设', "two_title": '项目注册'}
                if 'jsgcZbgg' in url:
                    meta = {"urls": url, "details": result.get('details'), "one_title": '工程建设', "two_title": '招标公告/预审公告'}
                if 'jsgcKbjl' in url:
                    meta = {"urls": url, "details": result.get('details'), "one_title": '工程建设', "two_title": '开标记录'}
                if 'jsgcpbjggs' in url:
                    meta = {"urls": url, "details": result.get('details'), "one_title": '工程建设', "two_title": '中标候选人'}
                if 'jsgcZbjggs' in url:
                    meta = {"urls": url, "details": result.get('details'), "one_title": '工程建设', "two_title": '中标结果'}
                if 'jsgcZtxx' in url:
                    continue
                if 'corpBasicInfo'in url:
                    continue
                for page_i in range(1, 4):
                    post_url = self.website_url + url
                    data = f'currentPage={page_i}&pageSize=10&currentArea=001&area=000&publishTimeType=3&publishTimeStart=&publishTimeEnd=&bulletinTitle=&purchaserMode=99&purchaserModeType=0'
                    headers = {
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Host": "www.hbggzyfwpt.cn",
                        "Referer": f"https://www.hbggzyfwpt.cn{url}?currentArea=&businessTypeValue=0",
                    }
                    yield scrapy.Request(post_url, method='POST', body=data, headers=headers, callback=self.parse_ztb_list, meta=meta, dont_filter=True)
            else:
                pass


    def parse_zfcg_list(self, response):
        list_json_data = response.json()
        if 'cggg' in response.meta['urls']:
            list_items = list_json_data.get('data')
            for list_item in list_items:
                detail_htlm = list_item.get('bulletinContent')
                if '</' not in detail_htlm:
                    title = list_item.get('bulletinTitle')
                    bid_public_time = list_item.get('bulletinStartTime')
                    releaseDate = format_time(bid_public_time)
                    url = 'https://www.hbggzyfwpt.cn/jyxx/zfcg/cgggDetail?guid=' + list_item.get('guid')
                    meta = {"url": url, "title": title, "releaseDate": releaseDate,
                            "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
                    yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta)
                else:
                    title = list_item.get('bulletinTitle')
                    tree = etree.parse(StringIO(detail_htlm), etree.HTMLParser())
                    detail_text = ' '.join(tree.xpath('//text()')).strip()
                    bid_public_time = list_item.get('bulletinStartTime')
                    po_public_time = format_time(bid_public_time)
                    url = response.meta['details']
                    contentUrl = self.website_url + url + list_item.get('guid')
                    po_id = get_md5(contentUrl)
                    item = GovernmentProcurementItem()
                    item['po_id'] = po_id
                    item['bid_url'] = contentUrl
                    item['po_province'] = '湖北省'
                    item['po_category'] = response.meta['one_title']
                    item['po_info_type'] = response.meta['two_title']
                    item['po_public_time'] = po_public_time
                    item['bo_name'] = title
                    item['po_html_con'] = detail_htlm
                    item['po_content'] = detail_text
                    item['website_name'] = self.website_name
                    item['website_url'] = self.website_url
                    item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                    item['list_parse'] = contentUrl
                    yield item
        if 'gzsxs' in response.meta['urls']:
            list_items = list_json_data.get('data')
            for list_item in list_items:
                detail_htlm = list_item.get('terminationBulletinContent')
                if '</' not in detail_htlm:
                    title = list_item.get('terminationBulletinTitle')
                    bid_public_time = list_item.get('modificationStartTime')
                    releaseDate = format_time(bid_public_time)
                    url ='https://www.hbggzyfwpt.cn/jyxx/zfcg/gzsxDetail?guid=' + list_item.get('guid')
                    meta = {"url": url, "title": title, "releaseDate": releaseDate,
                            "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
                    yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta)
                else:
                    title = list_item.get('terminationBulletinTitle')
                    tree = etree.parse(StringIO(detail_htlm), etree.HTMLParser())
                    detail_text = ' '.join(tree.xpath('//text()')).strip()
                    bid_public_time = list_item.get('modificationStartTime')
                    po_public_time = format_time(bid_public_time)
                    url = response.meta['details']
                    contentUrl = self.website_url + url + list_item.get('guid')
                    po_id = get_md5(contentUrl)
                    item = GovernmentProcurementItem()
                    item['po_id'] = po_id
                    item['bid_url'] = contentUrl
                    item['po_province'] = '湖北省'
                    item['po_category'] = response.meta['one_title']
                    item['po_info_type'] = response.meta['two_title']
                    item['po_public_time'] = po_public_time
                    item['bo_name'] = title
                    item['po_html_con'] = detail_htlm
                    item['po_content'] = detail_text
                    item['website_name'] = self.website_name
                    item['website_url'] = self.website_url
                    item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                    item['list_parse'] = contentUrl
                    yield item
        if 'zbjggs' in response.meta['urls']:
            list_items = list_json_data.get('data')
            for list_item in list_items:
                detail_htlm = list_item.get('winBidBulletinContent')
                if '</' not in detail_htlm:
                    title = list_item.get('winBidBulletinTitle')
                    bid_public_time = list_item.get('winBidBulletinStartTime')
                    releaseDate = format_time(bid_public_time)
                    url ='https://www.hbggzyfwpt.cn/jyxx/zfcg/zbjggsDetail?guid=' + list_item.get('guid')
                    meta = {"url": url, "title": title, "releaseDate": releaseDate,
                            "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
                    yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta)
                else:
                    title = list_item.get('winBidBulletinTitle')
                    tree = etree.parse(StringIO(detail_htlm), etree.HTMLParser())
                    detail_text = ' '.join(tree.xpath('//text()')).strip()
                    bid_public_time = list_item.get('winBidBulletinStartTime')
                    po_public_time = format_time(bid_public_time)
                    url = response.meta['details']
                    contentUrl = self.website_url + url + list_item.get('guid')
                    po_id = get_md5(contentUrl)
                    item = GovernmentProcurementItem()
                    item['po_id'] = po_id
                    item['bid_url'] = contentUrl
                    item['po_province'] = '湖北省'
                    item['po_category'] = response.meta['one_title']
                    item['po_info_type'] = response.meta['two_title']
                    item['po_public_time'] = po_public_time
                    item['bo_name'] = title
                    item['po_html_con'] = detail_htlm
                    item['po_content'] = detail_text
                    item['website_name'] = self.website_name
                    item['website_url'] = self.website_url
                    item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                    item['list_parse'] = contentUrl
                    yield item
        if 'cghts' in response.meta['urls']:
            list_items = list_json_data.get('data')
            for list_item in list_items:
                title = list_item.get('contractName')
                bid_public_time = list_item.get('signingTime')
                releaseDate = format_time(bid_public_time)
                url = list_item.get('url')
                meta = {"url": url, "title": title, "releaseDate": releaseDate,
                        "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
                yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta)

    def parse_ztb_list(self, response):
        list_json_data = response.json()
        if 'jsgcZbgg' in response.meta['urls']:
            list_items = list_json_data.get('data')
            for list_item in list_items:
                bulletinContent = list_item.get('bulletinContent')
                if '</' not in bulletinContent:
                    title = list_item.get('bulletinName')
                    bulletinIssueTime = list_item.get('bulletinIssueTime')
                    datetime_obj = datetime.strptime(bulletinIssueTime, "%Y%m%d%H%M%S")
                    formatted_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
                    po_public_time = format_time(formatted_time)
                    url ='https://www.hbggzyfwpt.cn/jyxx/jsgcZbggDetail?guid=' + list_item.get('tenderBulletinGuid')
                    meta = {"url": url, "title": title, "releaseDate": po_public_time,
                            "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
                    yield scrapy.Request(url, callback=self.parse_ztb_detail, meta=meta)
                else:
                    tree = etree.parse(StringIO(bulletinContent), etree.HTMLParser())
                    detail_text = ' '.join(tree.xpath('//text()')).strip()
                    tenderBulletinGuid = list_item.get('tenderBulletinGuid')
                    bulletinIssueTime = list_item.get('bulletinIssueTime')
                    datetime_obj = datetime.strptime(bulletinIssueTime, "%Y%m%d%H%M%S")
                    formatted_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
                    po_public_time = format_time(formatted_time)
                    bulletinName = list_item.get('bulletinName')
                    url = response.meta['details']
                    contentUrl = self.website_url + url + tenderBulletinGuid
                    bid_id = get_md5(contentUrl)
                    item = BidScrapyProjectItem()
                    item['bid_id'] = bid_id
                    item['bid_url'] = contentUrl
                    item['bid_province'] = '湖北省'
                    item['bid_category'] = response.meta['one_title']
                    item['bid_info_type'] = response.meta['two_title']
                    item['bid_name'] = bulletinName
                    item['bid_public_time'] = po_public_time
                    item['bid_html_con'] = bulletinContent
                    item['bid_content'] = detail_text
                    item['website_name'] = self.website_name
                    item['website_url'] = self.website_url
                    item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                    item['list_parse'] = contentUrl
                    yield item
        if 'jsgcZbjggs' in response.meta['urls']:
            list_items = list_json_data.get('data')
            for list_item in list_items:
                bulletinContent = list_item.get('bulletincontent')
                if '</' not in bulletinContent:
                    title = list_item.get('bulletinName')
                    bid_public_time = list_item.get('bulletinIssueTime')
                    releaseDate = format_time(bid_public_time)
                    url ='https://www.hbggzyfwpt.cn/jyxx/jsgcZbjggsDetail?guid=' + list_item.get('winBidBulletinGuid')
                    meta = {"url": url, "title": title, "releaseDate": releaseDate,
                            "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
                    yield scrapy.Request(url, callback=self.parse_ztb_detail, meta=meta)
                else:
                    tree = etree.parse(StringIO(bulletinContent), etree.HTMLParser())
                    detail_text = ' '.join(tree.xpath('//text()')).strip()
                    winBidBulletinGuid = list_item.get('winBidBulletinGuid')
                    bulletinIssueTime = list_item.get('bulletinIssueTime')
                    po_public_time = format_time(bulletinIssueTime)
                    bulletinName = list_item.get('bulletinName')
                    url = response.meta['details']
                    contentUrl = self.website_url + url + winBidBulletinGuid
                    bid_id = get_md5(contentUrl)
                    item = BidScrapyProjectItem()
                    item['bid_id'] = bid_id
                    item['bid_url'] = contentUrl
                    item['bid_province'] = '湖北省'
                    item['bid_category'] = response.meta['one_title']
                    item['bid_info_type'] = response.meta['two_title']
                    item['bid_name'] = bulletinName
                    item['bid_public_time'] = po_public_time
                    item['bid_html_con'] = bulletinContent
                    item['bid_content'] = detail_text
                    item['website_name'] = self.website_name
                    item['website_url'] = self.website_url
                    item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                    item['list_parse'] = contentUrl
                    yield item
        if 'jsgcKbjl' in response.meta['urls']:
            list_items = list_json_data.get('data')
            for list_item in list_items:
                bulletinContent = list_item.get('bidOpeningContent')
                if '</' not in bulletinContent:
                    title = list_item.get('noticeName')
                    bid_public_time = list_item.get('bidOpeningTime')
                    releaseDate = format_time(bid_public_time)
                    url ='https://www.hbggzyfwpt.cn/jyxx/jsgcKbjlDetail?guid=' + list_item.get('guid')
                    meta = {"url": url, "title": title, "releaseDate": releaseDate,
                            "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
                    yield scrapy.Request(url, callback=self.parse_ztb_detail, meta=meta)
                else:
                    tree = etree.parse(StringIO(bulletinContent), etree.HTMLParser())
                    detail_text = ' '.join(tree.xpath('//text()')).strip()
                    winBidBulletinGuid = list_item.get('guid')
                    bulletinIssueTime = list_item.get('bidOpeningTime')
                    po_public_time = format_time(bulletinIssueTime)
                    bulletinName = list_item.get('noticeName')
                    url = response.meta['details']
                    contentUrl = self.website_url + url + winBidBulletinGuid
                    bid_id = get_md5(contentUrl)
                    item = BidScrapyProjectItem()
                    item['bid_id'] = bid_id
                    item['bid_url'] = contentUrl
                    item['bid_province'] = '湖北省'
                    item['bid_category'] = response.meta['one_title']
                    item['bid_info_type'] = response.meta['two_title']
                    item['bid_name'] = bulletinName
                    item['bid_public_time'] = po_public_time
                    item['bid_html_con'] = bulletinContent
                    item['bid_content'] = detail_text
                    item['website_name'] = self.website_name
                    item['website_url'] = self.website_url
                    item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                    item['list_parse'] = contentUrl
                    yield item
        if 'jsgcXmxx' in response.meta['urls']:
            list_items = list_json_data.get('data')
            for list_item in list_items:
                categoryCode = list_item.get('guid')
                detail_url = response.meta['details']
                title = list_item.get('projectName')
                createTime = list_item.get('createTime')
                contentUrl = self.website_url + detail_url + categoryCode
                meta = {"url": contentUrl, "title": title, "releaseDate": createTime, "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
                yield scrapy.Request(contentUrl, callback=self.parse_ztb_detail, meta=meta)
        if 'jsgcpbjggs' in response.meta['urls']:
            list_items = list_json_data.get('data')
            for list_item in list_items:
                bulletinContent = list_item.get('publiCityContent')
                if '</' not in bulletinContent:
                    title = list_item.get('publiCityName')
                    bid_public_time = list_item.get('publiCityReferTime')
                    releaseDate = format_time(bid_public_time)
                    url ='https://www.hbggzyfwpt.cn/jyxx/jsgcpbjggsDetail?guid=' + list_item.get('guid')
                    meta = {"url": url, "title": title, "releaseDate": releaseDate,
                            "one_title": response.meta['one_title'], "two_title": response.meta['two_title']}
                    yield scrapy.Request(url, callback=self.parse_ztb_detail, meta=meta)
                else:
                    tree = etree.parse(StringIO(bulletinContent), etree.HTMLParser())
                    detail_text = ' '.join(tree.xpath('//text()')).strip()
                    winBidBulletinGuid = list_item.get('guid')
                    bulletinIssueTime = list_item.get('publiCityReferTime')
                    po_public_time = format_time(bulletinIssueTime)
                    bulletinName = list_item.get('publiCityName')
                    url = response.meta['details']
                    contentUrl = self.website_url + url + winBidBulletinGuid
                    bid_id = get_md5(contentUrl)
                    item = BidScrapyProjectItem()
                    item['bid_id'] = bid_id
                    item['bid_url'] = contentUrl
                    item['bid_province'] = '湖北省'
                    item['bid_category'] = response.meta['one_title']
                    item['bid_info_type'] = response.meta['two_title']
                    item['bid_name'] = bulletinName
                    item['bid_public_time'] = po_public_time
                    item['bid_html_con'] = bulletinContent
                    item['bid_content'] = detail_text
                    item['website_name'] = self.website_name
                    item['website_url'] = self.website_url
                    item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                    item['list_parse'] = contentUrl
                    yield item


    def parse_ztb_detail(self, response):
        detail_htlm = response.xpath("//div[@class='ctn-detail']").get()
        detail_text = ' '.join(response.xpath('//div[@class="ctn-detail"]//text()').extract()).strip()
        bid_public_time = response.meta['releaseDate']
        po_public_time = format_time(bid_public_time)
        contentUrl = response.meta['url']
        bid_id = get_md5(contentUrl)
        item = BidScrapyProjectItem()
        item['bid_id'] = bid_id
        item['bid_url'] = contentUrl
        item['bid_province'] = '湖北省'
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
        detail_htlm = response.xpath("//div[@class='content clearfloat']").get()
        detail_text = ' '.join(response.xpath('//div[@class="content clearfloat"]//text()').extract()).strip()
        bid_public_time = response.meta['releaseDate']
        po_public_time = format_time(bid_public_time)
        contentUrl = response.meta['url']
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item['po_id'] = po_id
        item['bid_url'] = contentUrl
        item['po_province'] = '湖北省'
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