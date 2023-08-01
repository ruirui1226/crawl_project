# -*- coding: utf-8 -*-
# @Time : 2023/6/20
# @Author: mayj

"""
    吉林省政府采购网
"""
import json
import time

import scrapy
from urllib.parse import quote
from pyquery import PyQuery as pq
from lxml import etree

from bid_scrapy_project.common.common import timestamp_to_str, get_md5
from bid_scrapy_project.items import GovernmentProcurementItem


class JilinZfcgSpider(scrapy.Spider):
    name = "jilin_zfcg"
    base_url = "http://www.ccgp-jilin.gov.cn/portal/category"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
    }
    category_args = [
        {
            "category_id": "ZcyAnnouncement2",
            "category": "采购公告",
        },
        {
            "category_id": "ZcyAnnouncement1",
            "category": "采购意向公告",
        },
        {
            "category_id": "ZcyAnnouncement3",
            "category": "更正公告",
        },
        {
            "category_id": "ZcyAnnouncement4",
            "category": "结果公告",
        },
        {
            "category_id": "ZcyAnnouncement5",
            "category": "合同公告",
        },
        {
            "category_id": "ZcyAnnouncement6",
            "category": "验收、其他公告",
        },
        {
            "category_id": "ZcyAnnouncement9",
            "category": "单一来源公告",
        },
        {
            "category_id": "ZcyAnnouncement10",
            "category": "电子商城公告",
        },
        {
            "category_id": "ZcyAnnouncement14001",
            "category": "中小企业预留执行公告",
        },
        {
            "category_id": "ZcyAnnouncement20",
            "category": "框架协议征集公告",
        },
        {
            "category_id": "ZcyAnnouncement21",
            "category": "框架协议入围结果公告",
        },
    ]

    def start_requests(self):
        for category_arg in self.category_args:
            data = {
                "categoryCode": category_arg["category_id"],
                "pageNo": 1,
                "pageSize": 100,
            }
            yield scrapy.Request(
                self.base_url,
                headers=self.headers,
                body=json.dumps(data),
                meta=category_arg,
                callback=self.parse_list,
                method="POST",
                dont_filter=True,
            )

    def parse_list(self, response):
        """处理列表页数据"""
        datas = response.json()["result"]["data"]["data"]
        for data in datas:
            meta_data = {}
            meta_data["title"] = data["title"]
            meta_data["category"] = response.meta["category"]
            meta_data["info_type"] = data["pathName"]  # 二级分类
            meta_data["articleId"] = data["articleId"]  # 详情拼接id
            publishDateStamp = data["publishDate"]
            meta_data["publishDate"] = timestamp_to_str(publishDateStamp)
            meta_data["city"] = data["districtName"]
            meta_data[
                "det_url"
            ] = f'http://www.ccgp-jilin.gov.cn/luban/detail?parentId=550068&articleId={meta_data["articleId"]}'
            req_det_url = (
                f'http://www.ccgp-jilin.gov.cn/portal/detail?articleId={quote(meta_data["articleId"])}&parentId=550068'
            )

            yield scrapy.Request(req_det_url, headers=self.headers, meta=meta_data, callback=self.parse_detail)

    def parse_detail(self, response):
        """处理详情数据"""
        json_data = response.json()["result"]["data"]
        item = GovernmentProcurementItem()
        item["po_id"] = get_md5(response.meta["articleId"])
        item["bid_url"] = response.meta["det_url"]
        item["po_province"] = "吉林省"
        item["po_city"] = response.meta["city"]
        # item['po_county'] = response.meta['city']
        # item["po_category"] = response.meta["category"]
        item["po_category"] = "政府采购"
        # item["po_info_type"] = response.meta["info_type"]
        item["po_info_type"] = response.meta["category"]
        item["po_public_time"] = response.meta["publishDate"]
        item["bo_name"] = response.meta["title"]
        item["po_source"] = json_data.get("author", "")
        item["po_html_con"] = json_data.get("content", "")
        item["po_content"] = pq(json_data.get("content", "")).text()
        item["website_name"] = "吉林省政府采购网"
        item["website_url"] = "http://www.ccgp-jilin.gov.cn/"
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

        yield item
