#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 9:13
# @Author  : xm
# @File    : xinjiang_cgw.py
# @Description :新疆政府采购网
import json
import time
from urllib.parse import quote

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import JsonRequest

from bid_scrapy_project.common.common import timestamp_to_str, get_md5, remove_node
from bid_scrapy_project.items import GovernmentProcurementItem


class XinjiangCgwSpider(scrapy.Spider):
    name = "xinjiang_cgw"

    def __init__(self):
        self.province = "新疆"
        self.website_name = "新疆政府采购网"
        self.webUrl = "http://www.ccgp-xinjiang.gov.cn/"
        self.type_infos = [
            {
                "id": 139095,
                "code": "ZcyAnnouncement11",
                "name": "采购意向",
                "children": [{"id": 139096, "code": "ZcyAnnouncement10016", "name": "采购意向公开", "children": []}],
            },
            {
                "id": 3662,
                "code": "ZcyAnnouncement2",
                "name": "采购项目公告",
                "children": [
                    {"id": 3663, "code": "ZcyAnnouncement3001", "name": "公开招标公告"},
                    {"id": 3664, "code": "ZcyAnnouncement3002", "name": "竞争性谈判公告"},
                    {"id": 3665, "code": "ZcyAnnouncement3003", "name": "询价公告"},
                    {"id": 3666, "code": "ZcyAnnouncement3008", "name": "邀请招标资格预审公告"},
                    {"id": 3667, "code": "ZcyAnnouncement3011", "name": "竞争性磋商公告"},
                    {"id": 3724, "code": "ZcyAnnouncement2001", "name": "公开招标资格预审公告"},
                    {"id": 139146, "code": "ZcyAnnouncement3020", "name": "邀请招标公告"},
                ],
            },
            {
                "id": 3717,
                "code": "ZcyAnnouncement1",
                "name": "采购公示",
                "children": [
                    {"id": 3720, "code": "ZcyAnnouncement3014", "name": "采购文件需求公示"},
                    {"id": 3718, "code": "ZcyAnnouncement3012", "name": "单一来源公示"},
                ],
            },
            {
                "id": 3696,
                "code": "ZcyAnnouncement4",
                "name": "采购结果公告",
                "children": [
                    {"id": 3697, "code": "ZcyAnnouncement3004", "name": "中标(成交)结果公告"},
                    {"id": 3699, "code": "ZcyAnnouncement3009", "name": "邀请招标资格入围公告"},
                    {"id": 3700, "code": "ZcyAnnouncement3015", "name": "终止公告"},
                    {"id": 3701, "code": "ZcyAnnouncement3017", "name": "采购结果变更公告"},
                    {"id": 3726, "code": "ZcyAnnouncement4004", "name": "公开招标资格入围公告"},
                    {"id": 139147, "code": "ZcyAnnouncement4005", "name": "中标公告"},
                ],
            },
            {
                "id": 3715,
                "code": "ZcyAnnouncement5",
                "name": "采购合同公告",
                "children": [{"id": 3716, "code": "ZcyAnnouncement3010", "name": "采购合同公告"}],
            },
            {
                "id": 3668,
                "code": "ZcyAnnouncement3",
                "name": "澄清变更公告",
                "children": [
                    {"id": 3669, "code": "ZcyAnnouncement3005", "name": "更正公告"},
                    {"id": 3670, "code": "ZcyAnnouncement3006", "name": "澄清（修改）公告"},
                    {"id": 3725, "code": "ZcyAnnouncement3018", "name": "中止（暂停）公告"},
                ],
            },
            {
                "id": 3723,
                "code": "ZcyAnnouncement10",
                "name": "废标公告",
                "children": [{"id": 3698, "code": "ZcyAnnouncement3007", "name": "废标公告"}],
            },
            {
                "id": 3721,
                "code": "ZcyAnnouncement6",
                "name": "履约验收",
                "children": [{"id": 3722, "code": "ZcyAnnouncement3016", "name": "履约验收公告（服务类）"}],
            },
            # {
            #     "id": 3702,
            #     "code": "ZcyAnnouncement8",
            #     "name": "电子卖场公告",
            #     "children": [
            #         {"id": 5392, "code": "ZcyAnnouncement8014", "name": "电子卖场采购公告"},
            #         {"id": 5393, "code": "ZcyAnnouncement8013", "name": "电子卖场成交公告-采购成功"},
            #         {"id": 541285, "code": "ZcyAnnouncement9005", "name": "电子卖场合同公告（网上超市)"},
            #         {"id": 3706, "code": "ZcyAnnouncement5001", "name": "电子卖场合同公告（在线询价）"},
            #         {"id": 3707, "code": "ZcyAnnouncement7001", "name": "电子卖场合同公告（反向竞价）"},
            #         {"id": 3709, "code": "ZcyAnnouncement8001", "name": "电子卖场合同公告（汽车馆）"},
            #         {"id": 3712, "code": "ZcyAnnouncement9001", "name": "电子卖场合同公告（服务市场）"},
            #     ],
            # },
            {
                "id": 560130,
                "code": "ZcyAnnouncement88",
                "name": "框架协议征集公告",
                "children": [
                    {"id": 560136, "code": "ZcyAnnouncement2004", "name": "封闭式征集公告"},
                    {"id": 560137, "code": "ZcyAnnouncement2005", "name": "开放式征集公告"},
                ],
            },
            {
                "id": 560131,
                "code": "ZcyAnnouncement12",
                "name": "框架协议入围结果公告",
                "children": [
                    {"id": 560132, "code": "ZcyAnnouncement4009", "name": "封闭式入围结果公告"},
                    {"id": 560133, "code": "ZcyAnnouncement8043", "name": "开放式入围结果公告"},
                ],
            },
            {
                "id": 560134,
                "code": "ZcyAnnouncement13",
                "name": "框架协议成交结果公告",
                "children": [{"id": 560135, "code": "ZcyAnnouncement8042", "name": "顺序轮候成交结果公告"}],
            },
            {
                "id": 560138,
                "code": "ZcyAnnouncement14",
                "name": "框架协议成交结果汇总公告",
                "children": [{"id": 560139, "code": "ZcyAnnouncement8040", "name": "成交结果汇总公告"}],
            },
            # {
            #     "id": 3671,
            #     "code": "ZcyAnnouncement9",
            #     "name": "非政府采购公告",
            #     "children": [
            #         {"id": 5395, "code": "ZcyAnnouncement10015", "name": "委托代理公告"},
            #         {"id": 3684, "code": "ZcyAnnouncement10011", "name": "其他非政府采购公告"},
            #     ],
            # },
            # {"id": 550117, "code": "ZcyAnnouncement14001", "name": "中小企业预留情况公告", "children": []},
        ]
        self.citys = [
            {"code": "650100", "name": "乌鲁木齐市"},
            {"code": "650200", "name": "克拉玛依市"},
            {"code": "650400", "name": "吐鲁番市"},
            {"code": "650500", "name": "哈密市"},
            {"code": "652300", "name": "昌吉回族自治州"},
            {"code": "652700", "name": "博尔塔拉蒙古自治州"},
            {"code": "652800", "name": "巴音郭楞蒙古自治州"},
            {"code": "652900", "name": "阿克苏地区"},
            {"code": "653000", "name": "克孜勒苏柯尔克孜自治州"},
            {"code": "653100", "name": "喀什地区"},
            {"code": "653200", "name": "和田地区"},
            {"code": "654000", "name": "伊犁哈萨克自治州"},
            {"code": "654200", "name": "塔城地区"},
            {"code": "654300", "name": "阿勒泰地区"},
            {"code": "659900", "name": "新疆维吾尔自治区本级"},
        ]
        self.apiUrl = "http://www.ccgp-xinjiang.gov.cn/portal/category"
        self.params = {
            "pageNo": 1,
            "pageSize": 15,
            "categoryCode": "ZcyAnnouncement14001",
            "districtCode": ["650100"],
            "_t": 1688608746000,
        }
        self.pages = 2
        self.headers = {
            "Content-Type": "application/json",
            # 'Cookie': 'acw_tc=ac11000116886099742821444e44c8a0df1b006606eeaa0061c0d7e33b0f73'
        }
        self.category = "政府采购"

    def start_requests(self):
        for city in self.citys:
            cityId = city.get("code")
            cityName = city.get("name")
            for type in self.type_infos:
                for page in range(1, self.pages):
                    # 网页大类型名称 不用   type.get("name")
                    if not type.get("children"):
                        infotype = type.get("name")
                        self.params["pageNo"] = page
                        self.params["categoryCode"] = type.get("code")
                        self.params["districtCode"][0] = cityId
                        self.params["_t"] = str(int(time.time() * 1000))
                        items = {"city": cityName, "infotype": infotype}
                        yield JsonRequest(
                            self.apiUrl,
                            data=self.params,
                            callback=self.parse,
                            headers=self.headers,
                            meta={"items": items},
                            dont_filter=True
                        )
                    else:
                        for child in type.get("children"):
                            typeId = child.get("code")
                            infoName = child.get("name")
                            self.params["pageNo"] = page
                            self.params["categoryCode"] = typeId
                            self.params["districtCode"][0] = cityId
                            self.params["_t"] = str(int(time.time() * 1000))
                            items = {"city": cityName, "infotype": infoName}
                            yield JsonRequest(
                                self.apiUrl,
                                data=self.params,
                                callback=self.parse,
                                headers=self.headers,
                                meta={"items": items},
                                dont_filter=True
                            )

    def parse(self, response, **kwargs):
        jsonDict = json.loads(response.text)
        result = jsonDict.get("result")
        if not result:
            return
        datas = None
        try:
            datas = result.get("data").get("data")
        except:
            return
        if not datas:
            return
        for data in datas:
            author = data.get("author")
            articleId = data.get("articleId")
            title = data.get("title")
            publishDate = data.get("publishDate")
            publishtime = timestamp_to_str(publishDate)
            contentUrl = "http://www.ccgp-xinjiang.gov.cn/luban/detail?articleId={}".format(articleId)
            itmes = {"title": title, "author": author, "publishtime": publishtime, "contentUrl": contentUrl}
            itmes.update(response.meta["items"])
            # http://www.ccgp-xinjiang.gov.cn/portal/detail?articleId=8ED6yfKAhWn%2BHYYPuC9BvA%3D%3D
            contentApi = "http://www.ccgp-xinjiang.gov.cn/portal/detail?articleId={}".format(quote(articleId, "utf-8"))
            yield scrapy.Request(url=contentApi, callback=self.contentParse, meta={"items": itmes})

    def contentParse(self, response):
        item_info = response.meta["items"]
        jsonDict = json.loads(response.text)
        if not jsonDict.get("success"):
            return
        data = jsonDict.get("result").get("data")
        try:
            content_html = data.get("content")
        except:
            # print()
            return
        content = remove_node(content_html, ["style"]).text
        items = {
            "po_id": get_md5(item_info.get("contentUrl")),
            "bid_url": item_info.get("contentUrl"),
            "po_province": self.province,
            "po_city": item_info.get("city"),
            "po_category": self.category,
            "po_info_type": item_info.get("infotype"),
            "po_public_time": item_info.get("publishtime"),
            "bo_name": item_info.get("title"),
            "po_source": item_info.get("author"),
            "po_html_con": content_html,
            "po_content": content,
            "website_name": self.website_name,
            "website_url": self.webUrl,
            "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }
        item_po = GovernmentProcurementItem()
        item_po.update(items)
        # print(items)
        yield item_po
