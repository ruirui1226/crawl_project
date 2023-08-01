# -*- coding: utf-8 -*-
"""
@desc: 国家电网新一代电子商务平台
@version: python3
@author: shenr
@time: 2023/06/26
"""
import base64
import json
import logging
import re
import time

import requests
import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class ExampleSpider(scrapy.Spider):
    name = "gjdw_ggjy"
    # allowed_domains = ["https://ecp.sgcc.com.cn/ecp2.0/portal/#/"]
    start_urls = "https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/noteList"
    page = 1
    page_all = 1
    body_list = {
        "2018032700290425": "资格预审公告",
        "2018032700291334": "招标公告及投标邀请书",
        "2018032900295987": "采购公告",
        "2018060501171107": "推荐中标候选人公示",
        "2018060501171111": "中标（成交）结果公告",
        "2019071434439387": "公共信息",
    }
    det_url_list = {
        "doci-bid": "getNoticeBid",
        "doci-change": "getChangeBid",
        "doc-spec": "getDoc",
        "doci-win": "getNoticeWin",
        "doc-com": "getDoc",
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "$Cookie": "BIGipServerpool_ecp2_0=\\u0021+qEABJauzch01PtHuvsVfH4Y05Q7kvnCL/39J/OAkS+QhvqkS4OFdtSIScDiTD/aXl529jKAvD8AHw==; JSESSIONID=1527B892DFB31C89D24941F11F439A51",
        "Origin": "https://ecp.sgcc.com.cn",
        "Referer": "https://ecp.sgcc.com.cn/ecp2.0/portal/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    def start_requests(self):
        for ii in self.body_list:
            data_ = {
                "index": 1,
                "size": 20,
                "firstPageMenuId": ii,
                "purOrgStatus": "",
                "purOrgCode": "",
                "purType": "",
                "noticeType": "",
                "orgId": "",
                "key": "",
                "orgName": "",
            }
            yield scrapy.FormRequest(
                url=self.start_urls,
                headers=self.headers,
                body=json.dumps(data_),
                meta={"bid_info_type": self.body_list[ii]},
                dont_filter=True,
                callback=self.parse_1,
                method="POST",
            )

    def parse_1(self, response, **kwargs):
        meta = response.meta
        bid_info_type = meta.get("bid_info_type")
        if int(response.status) == 200:
            res = json.loads(response.text)
            noteList = res.get("resultValue").get("noteList")
            logging.debug(f"============当前爬取{self.page}页==========")
            for each in noteList:
                detail_url = (
                    "https://ecp.sgcc.com.cn/ecp2.0/portal/#/doc/"
                    + str(each.get("doctype"))
                    + "/"
                    + str(each.get("id"))
                    + "_"
                    + str(each.get("firstPageMenuId"))
                )
                id_ = str(each.get("id"))
                title = each.get("title")
                topBeginTime = each.get("topBeginTime")
                noticePublishTime = each.get("noticePublishTime")
                po_public_time = topBeginTime or noticePublishTime
                det_url = f"https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/{self.det_url_list.get(str(each.get('doctype')))}"
                yield scrapy.FormRequest(
                    url=det_url,
                    headers=self.headers,
                    body=str(each.get("id")),
                    meta={
                        "id_": id_,
                        "detail_url": detail_url,
                        "title": title,
                        "po_public_time": po_public_time,
                        "bid_info_type": bid_info_type,
                    },
                    # dont_filter=True,
                    method="POST",
                    callback=self.detail_parse,
                )
        else:
            logging.debug("==========爬取结束============")

    def detail_parse(self, response, **kwargs):
        res = json.loads(response.text)
        meta = response.meta
        detail_url = meta.get("detail_url")
        title = meta.get("title")
        po_public_time = meta.get("po_public_time")
        id_ = meta.get("id_")
        bid_info_type = meta.get("bid_info_type")
        if bid_info_type == "采购公告":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(id_)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = detail_url
            item["po_province"] = ""
            item["po_city"] = ""
            item["po_county"] = ""
            item["po_category"] = "招标采购"
            item["po_info_type"] = bid_info_type
            item["po_source"] = ""
            item["bo_name"] = title
            item["po_public_time"] = po_public_time
            item["po_html_con"] = str(res.get("resultValue").get("notice")).replace("'", '"')
            item["po_content"] = str(res.get("resultValue").get("notice")).replace("'", '"')
            item["po_json_data"] = str(res).replace("'", '"')
            item["description"] = ""
            item["website_name"] = "国家电网新一代电子商务平台"
            item["website_url"] = "https://ecp.sgcc.com.cn/ecp2.0/portal/#/"
            logging.debug(item)
            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(id_)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = detail_url
            item["bid_md5_url"] = ""
            item["bid_province"] = ""
            item["bid_city"] = ""
            item["bid_county"] = ""
            item["bid_category"] = "招标采购"
            item["bid_info_type"] = bid_info_type
            item["bid_source"] = ""
            item["bid_name"] = title
            item["bid_public_time"] = po_public_time
            item["bid_html_con"] = str(res.get("resultValue").get("notice")).replace("'", '"')
            item["bid_content"] = str(res.get("resultValue").get("notice")).replace("'", '"')
            item["bid_json_data"] = str(res).replace("'", '"')
            item["description"] = ""
            item["website_name"] = "国家电网新一代电子商务平台"
            item["website_url"] = "https://ecp.sgcc.com.cn/ecp2.0/portal/#/"
            logging.debug(item)
            yield item
