# -*- coding: utf-8 -*-
"""
@desc: 西藏采购网
@version: python3
@author: liuwx
@time: 2023/07/06
"""

import scrapy
import json
import time

from lxml import etree
from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import GovernmentProcurementItem

class XizangCgwSpider(scrapy.Spider):
    name = 'xizang_cgw'
    # custom_settings = {"CONCURRENT_REQUESTS": 1, 'DOWNLOAD_DELAY': 3}

    """
    二级类型 直接列出
    """
    def __init__(self):
        self.noticeType = {
            "采购公告": "00101",
            "中标（成交）公告": "00102",
            "更正公告": "001003,001031,001032",
            "废标（终止）公告": "001004,001006",
            "其他公告": "001052,001053,001055,001056,001057,001058,001059",
            "单一来源公示": "001051",
            "验收结果公告": "001009",
            "合同公告": "001054",
            "采购意向公开": "59"
        }

    """
    列表页链接请求
    """
    def start_requests(self):
        for info_type, notice_id in self.noticeType.items():
            items = {"po_info_type": info_type}
            # 列表页接口获取
            link = f"http://www.ccgp-xizang.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=18de62f0-2fb0-4187-a6c1-cd8fcbfb4585&channel=b541ffff-03ee-4160-be64-b11ccf79660d&currPage=1&pageSize=100&noticeType={notice_id}&cityOrArea=&noticeName=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime"
            yield scrapy.Request(
                link,
                callback=self.parse,
                meta={"items": items},
                dont_filter=True
            )

    """
    列表页详情获取（标题、发布时间、详情页链接）
    """
    def parse(self, response):
        item_info = response.meta["items"]
        # 获取详情页json数据
        listjson = json.loads(response.text)
        data_list = listjson['data']
        for data in data_list:
            # 获取发布时间
            pubtime = data["fieldValues"]["f_noticeTime"]
            # 截取发布时间年月日
            pubday = pubtime.split(' ')[0]
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if pubday != nowday:
                # print(pubtime + "不是当天最新文章，跳过")
                break
            # 获取文章标题
            title = data['title']
            # 获取文章链接
            url = data['pageurl']
            url = response.urljoin(url)
            # 获取文章简介
            description = data['description']
            items = {
                "po_public_time": pubtime,
                "bid_url": url,
                "bo_name": title,
                "po_id": get_md5(url),
                "description": description
            }
            items.update(item_info)
            yield scrapy.Request(
                url,
                callback=self.getContentInfo,
                meta={"items": items}
            )

    """
    文章详情获取（发布内容）
    """
    def getContentInfo(self, response):
        items_info = response.meta["items"]
        # 带有html的文本
        str_html_content = etree.HTML(response.text).xpath('//div[@class="notice-con"]')
        if str_html_content:
            contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        else:
            print("未获取到html文本")
        # 纯净文本
        content = remove_node(contentHtml, ["style"]).text
        items_infos = GovernmentProcurementItem()
        items_infos['po_category'] = "政府采购"
        items_infos['po_info_type'] = items_info["po_info_type"]
        items_infos['po_province'] = "西藏自治区"
        # items_infos['po_city'] = items_info["po_city"]
        # items_infos['po_county'] = item_info["po_county"]
        # items_infos['po_json_data'] = listjson
        items_infos['po_public_time'] = items_info["po_public_time"]
        items_infos['bo_name'] = items_info["bo_name"]
        items_infos['po_html_con'] = contentHtml
        items_infos['po_content'] = content
        items_infos['bid_url'] = items_info["bid_url"]
        items_infos["po_id"] = items_info["po_id"]
        items_infos['website_name'] = "西藏采购网"
        items_infos['website_url'] = "http://www.ccgp-xizang.gov.cn/"
        items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(
        #     items_infos["po_id"],
        #     items_infos["bid_url"],
        #     items_infos["po_public_time"]
        # )
        yield items_infos