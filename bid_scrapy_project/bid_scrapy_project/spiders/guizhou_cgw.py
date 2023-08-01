# -*- coding: utf-8 -*-
"""
@desc: 贵州省政府采购网
@version: python3
@author: xm
@time: 2023/06/16
"""

import json
import time
from urllib.parse import quote

import scrapy
from bs4 import BeautifulSoup
from lxml import html
from scrapy.http import JsonRequest

from bid_scrapy_project.common.common import get_md5, timestamp_to_str, remove_node
from bid_scrapy_project.items import GovernmentProcurementItem


class GuizhouCgwSpider(scrapy.Spider):
    name = "guizhou_cgw"

    # allowed_domains = ['ccgp-guizhou.gov.cn']
    # start_urls = ['http://ccgp-guizhou.gov.cn/']
    def __init__(self):
        self.apiUrl = "http://www.ccgp-guizhou.gov.cn/portal/category"
        self.leixings = {
            "采购意向": {
                # "code": "ZcyAnnouncement1",
                "采购意向公开": "ZcyAnnouncement10016"
            },
            "采购需求公示": {
                # "code": "ZcyAnnouncement2",
                "采购文件需求公示": "ZcyAnnouncement3014",
                "单一来源公示": "ZcyAnnouncement3012",
            },
            "采购公告": {
                # "code": "ZcyAnnouncement3",
                "资格预审公告": "ZcyAnnouncement33",
                "招标公告": "ZcyAnnouncement3001",
                "非招标公告": "ZcyAnnouncement333",
            },
            "更正公告": {
                # "code": "ZcyAnnouncement4",
                "更正公告": "ZcyAnnouncement3005"
            },
            "采购结果公告": {
                # "code": "ZcyAnnouncement5",
                "中标(成交)结果公告": "ZcyAnnouncement3004",
                "终止公告": "ZcyAnnouncement3015",
                "采购结果变更公告": "ZcyAnnouncement3017",
            },
            "采购合同公告": {
                # "code": "ZcyAnnouncement6",
                "采购合同公告": "ZcyAnnouncement3010"
            },
            "履约验收公告": {
                # "code": "ZcyAnnouncement7",
                "履约验收公告": "ZcyAnnouncement3016"
            },
        }
        self.province = "贵州省"
        self.website_name = "贵州省政府采购网"
        self.website_url = "http://www.ccgp-guizhou.gov.cn/"

    def start_requests(self):
        # 区{"pageNo":1,"pageSize":15,"categoryCode":"ZcyAnnouncement10016","_t":1686894293000,"districtCode":["529900"],"isProvince":false}
        # 省 {"pageNo":1,"pageSize":15,"categoryCode":"ZcyAnnouncement2","_t":1686885307000,"districtCode":["529900"],"isProvince":true}

        # http://www.ccgp-guizhou.gov.cn/admin/category/home/categoryTreeFind?parentId=190013&siteId=96
        # items = GovernmentProcurementItem()
        for name, value in self.leixings.items():
            for type, typeValue in value.items():
                for page in range(1, 3):
                    # 区
                    countyParam = {
                        "pageNo": page,
                        "pageSize": 15,
                        "categoryCode": "{}".format(typeValue),
                        "_t": int(time.time() * 1000),
                        "districtCode": ["529900"],
                        "isProvince": False,
                    }
                    items = {
                        "po_category": "政府采购",
                        "po_info_type": name,
                    }
                    yield JsonRequest(
                        self.apiUrl, data=countyParam, callback=self.parse, meta={"items": items}, dont_filter=True
                    )
                    # 省
                    provinParam = {
                        "pageNo": page,
                        "pageSize": 15,
                        "categoryCode": "{}".format(typeValue),
                        "_t": int(time.time() * 1000),
                        "districtCode": ["529900"],
                        "isProvince": True,
                    }
                    yield JsonRequest(
                        self.apiUrl, data=provinParam, callback=self.parse, meta={"items": items}, dont_filter=True
                    )

    def parse(self, response):
        items_info = response.meta["items"]
        jsonDcit = json.loads(response.text)
        try:
            datas = jsonDcit.get("result").get("data").get("data")
        except:
            return
        for data in datas:
            title = data.get("title")
            publishDate = data.get("publishDate")
            publishDate = timestamp_to_str(publishDate)
            districtName = data.get("districtName")  ## 区还是省  贵州省本级需要处理
            items = {}
            if "贵州省" in districtName:
                districtName = "贵州省"
                items["po_province"] = self.province
            elif "市" in districtName:
                items["po_city"] = districtName
            else:
                items["po_county"] = districtName
            # http://www.ccgp-guizhou.gov.cn/luban/detail?parentId=190013&articleId=vmzhsXcBH/P66UYvjgPTOA==
            articleId = data.get("articleId")
            href = "http://www.ccgp-guizhou.gov.cn/luban/detail?parentId=190013&articleId=" + articleId
            items.update(items_info)
            items["bid_url"] = href
            items["po_id"] = get_md5(articleId)
            items["bo_name"] = title
            items["po_public_time"] = publishDate
            hrefApi = "http://www.ccgp-guizhou.gov.cn/portal/detail?articleId={}&parentId=190013".format(
                quote(articleId, "utf-8")
            )
            yield scrapy.Request(hrefApi, callback=self.contentParse, meta={"items": items})

    def contentParse(self, response):
        items_info = response.meta["items"]
        jsonDict = json.loads(response.text)
        data = jsonDict.get("result").get("data")
        content_html = data.get("content")
        author = data.get("author")
        items = GovernmentProcurementItem()
        items.update(items_info)

        content = remove_node(content_html, ["style"]).text
        items["po_content"] = content
        items["po_province"] = self.province
        items["po_source"] = author
        items["website_name"] = self.website_name
        items["website_url"] = self.website_url
        items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(items)
        items["po_html_con"] = content_html
        # print(items)
        yield items
