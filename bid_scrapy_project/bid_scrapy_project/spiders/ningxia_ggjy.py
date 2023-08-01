# -*- coding: utf-8 -*-
# @Time : 2023/6/26
# @Author: mayj

"""
    全国公共资源交易平台(宁夏回族自治区)
"""
import datetime
import json
import math
import re
import time

import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import GovernmentProcurementItem, BidScrapyProjectItem


class NingxiaGgjySpider(scrapy.Spider):
    name = "ningxia_ggjy"
    base_url = "http://www.nxggzyjy.org/inteligentsearch_es/rest/esinteligentsearch/getFullTextDataNew"
    categorys = {
        "002001": "工程建设",
        "002002": "政府采购",
        "002003": "药品采购",
        "002004": "产权交易",
        "002005": "土地及矿业权",
    }
    date_now = datetime.date.today()
    date_now_rep = str(date_now).replace("-", "")
    data = {
        "token": "",
        "pn": 0,
        "rn": 20,
        "sdt": "",
        "edt": "",
        "wd": "",
        "inc_wd": "",
        "exc_wd": "",
        "fields": "",
        "cnum": "",
        "sort": '{"istop":"0","ordernum":"0","webdate":"0","infoid":"0"}',
        "ssort": "",
        "cl": 10000,
        "terminal": "",
        "condition": [
            {
                "fieldName": "categorynum",
                "equal": "002",
                "notEqual": None,
                "equalList": None,
                "notEqualList": None,
                "isLike": True,
                "likeType": 2,
            }
        ],
        "time": [{"fieldName": "webdate", "startTime": f"{date_now} 00:00:00", "endTime": f"{date_now} 23:59:59"}],
        "highlights": "",
        "statistics": None,
        "unionCondition": None,
        "accuracy": "",
        "noParticiple": "1",
        "searchRange": None,
        "noWd": True,
    }

    def start_requests(self):
        yield scrapy.Request(
            self.base_url, body=json.dumps(self.data), meta={"next": True}, callback=self.parse_list, dont_filter=True
        )

    def parse_list(self, response):
        """处理列表页信息"""
        # 遍历列表json
        datas = response.json()["result"]["records"]
        for data in datas:
            meta_data = {}
            categorynum = data.get("categorynum")
            category_id = re.search("(\d{6})", categorynum).group(1)
            meta_data["category_name"] = self.categorys.get(category_id, "")
            meta_data["info_type_name"] = data.get("categoryname")
            meta_data["title"] = data.get("title")
            meta_data["pub_date"] = data.get("webdate")
            id = data.get("id").split("_")[0]
            meta_data["id"] = id
            url = f"http://www.nxggzyjy.org/ningxiaweb/002/{category_id}/{categorynum}/{self.date_now_rep}/{id}.html"
            yield scrapy.Request(url, meta=meta_data, callback=self.parse_detail)

        # 遍历获取下一页
        if response.meta.get("next", ""):
            pages = math.ceil(response.json()["result"]["totalcount"] / 20)
            for num in range(1, pages):
                data = self.data
                data["pn"] = num * 20
                yield scrapy.Request(
                    self.base_url, body=json.dumps(self.data), callback=self.parse_list, dont_filter=True
                )

    def parse_detail(self, response):
        """处理详情信息"""
        meta = response.meta
        md5_id = get_md5(meta["id"])
        category_name = meta["category_name"]
        info_type_name = meta["info_type_name"]
        title = meta["title"]
        pub_date = meta["pub_date"]
        url = response.url
        html_con = response.xpath('//div[@class="ewb-main"]').extract_first()
        content = response.xpath('string(//div[@class="ewb-main"])').extract_first()
        website_name = "宁夏回族自治区公共资源交易网"
        website_url = "http://www.nxggzyjy.org"
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        province = "宁夏"

        if category_name == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = md5_id
            item["bid_url"] = url
            item["po_province"] = province
            item["po_category"] = category_name
            item["po_info_type"] = info_type_name
            item["po_public_time"] = pub_date
            item["bo_name"] = title
            item["po_html_con"] = html_con
            item["po_content"] = content
            item["website_name"] = website_name
            item["website_url"] = website_url
            item["create_datetime"] = create_date

        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = md5_id
            item["create_datetime"] = create_date
            item["bid_url"] = url
            item["bid_province"] = province
            item["bid_category"] = category_name
            item["bid_info_type"] = info_type_name
            item["bid_name"] = title
            item["bid_public_time"] = pub_date
            item["bid_html_con"] = html_con
            item["bid_content"] = content
            item["website_name"] = website_name
            item["website_url"] = website_url

        yield item
