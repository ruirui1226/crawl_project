# -*- coding: utf-8 -*-
"""
@desc: 湖南省政府采购网
@version: python3
@author: xm
@time: 2023/06/21
"""
import datetime
import json
import time

import scrapy
from scrapy import FormRequest

from bid_scrapy_project.common.common import timestamp_to_str, get_md5
from bid_scrapy_project.items import GovernmentProcurementItem


class HunanCgwSpider(scrapy.Spider):
    name = "hunan_cgw"

    # allowed_domains = ['www.ccgp-hunan.gov.cn']
    # start_urls = ['http://www.ccgp-hunan.gov.cn/']
    def __init__(self):
        self.nTypearr = [
            "prcmNotices",
            "dealNotices",
            "invalidNotices",
            "contractNotices",
            "modfiyNotices",
            "endNotices",
            "otherNotices",
        ]
        self.nTypearr_name = ["采购公告", "中标(成交)公告", "废标公告", "合同公告", "更正公告", "终止公告", "其他公告"]
        self.dict_nty = zip(self.nTypearr_name, self.nTypearr)
        self.pTypes = {
            "公开招标": "01",
            "协议供货": "07",
            "定点采购": "06",
            "邀请招标": "02",
            "竞争性谈判": "03",
            "询价": "04",
            "单一来源": "05",
            "竞争性磋商": "11",
        }
        # "协议供货" 07  "定点采购" 06 "邀请招标" 02  "竞争性谈判"  03  "询价" 04 "单一来源" 05 "竞争性磋商" 11
        self.apiUrl = "http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do"
        self.province = "湖南省"
        self.website_url = "http://www.ccgp-hunan.gov.cn/"
        self.website_name = "湖南省政府采购网"
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": " www.ccgp-hunan.gov.cn",
            "Origin": "http://www.ccgp-hunan.gov.cn",
            "Referer": "http://www.ccgp-hunan.gov.cn/page/notice/more.jsp?noticeTypeID=prcmNotices",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
        }

    def start_requests(self):
        for i, v in dict(self.dict_nty).items():
            category = i
            for x, y in self.pTypes.items():
                info_type = x
                page = 1
                param = {
                    "nType": str(v),
                    "pType": str(y),
                    "prcmPrjName": "",
                    "prcmItemCode": "",
                    "prcmOrgName": "",
                    "startDate": str(datetime.date.today().year) + "-01-01",
                    "endDate": str(time.strftime("%Y-%m-%d", time.localtime(int(time.time())))),
                    "prcmPlanNo": "",
                    "page": str(page),
                    "pageSize": "18",
                }
                items = {
                    "po_category": "政府采购",
                    "po_info_type": category,
                }
                yield FormRequest(
                    self.apiUrl,
                    formdata=param,
                    callback=self.parse,
                    meta={"items": items},
                    headers=self.headers,
                    dont_filter=True,
                )

    def parse(self, response):
        imem_info = response.meta["items"]
        jsonDict = json.loads(response.text)
        rows = jsonDict.get("rows")
        for row in rows:
            title = row.get("NOTICE_TITLE")
            NOTICE_ID = row.get("NOTICE_ID")
            author = row.get("ORG_NAME")
            href = "http://www.ccgp-hunan.gov.cn/page/notice/notice.jsp?noticeId={}".format(NOTICE_ID)
            NEWWORK_DATE_ALL = row.get("NEWWORK_DATE_ALL")
            pubdate = NEWWORK_DATE_ALL.get("time")
            pubtime = timestamp_to_str(pubdate)
            items = {"bo_name": title, "po_source": author, "bid_url": href, "po_public_time": pubtime}
            items.update(imem_info)
            contentApiUrl = "http://www.ccgp-hunan.gov.cn/mvc/viewNoticeContent.do?noticeId={}&area_id=".format(
                NOTICE_ID
            )
            yield scrapy.Request(contentApiUrl, callback=self.getContentInfo, meta={"items": items})

    def getContentInfo(self, response):
        items_info = response.meta["items"]
        linkss = None
        if "公告链接：" in response.text:
            # 原始链接
            linkss = response.css("body a::attr(href)").get()
        # name
        title = response.css("body > h1::text").get()
        if not title:
            title = response.css("p.danyi_title::text").get()

        content_html = str(response.css("body").get())
        contents = response.css("body *::text").extract()
        content = "".join(x.strip() for x in contents)
        if not title and not content:
            print("此链接没有数据--空白", items_info["bid_url"])
            return
        if not title:
            title = items_info["bo_name"]
        dict(items_info).pop("bo_name")
        items = GovernmentProcurementItem()
        items.update(items_info)
        if linkss:
            items["bid_orgin_url"] = linkss
        items["bo_name"] = title.strip()
        items["po_content"] = content
        items["po_id"] = get_md5(items_info["bid_url"])
        items["po_province"] = self.province
        items["website_name"] = self.website_name
        items["website_url"] = self.website_url
        items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(items)
        items["po_html_con"] = content_html
        yield items
