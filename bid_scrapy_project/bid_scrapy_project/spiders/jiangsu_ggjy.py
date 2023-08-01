# -*- coding: utf-8 -*-
"""
@desc: 江苏-采购网
@version: python3
@author: shenr
@time: 2023/06/26
"""
import base64
import datetime
import json
import logging
import re
import time

import ddddocr
import requests
import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

st_url = "http://www.ccgp-jiangsu.gov.cn/pss/servlet/validateCodeServlet"


def get_request_cookies(st_url, headers):
    try:
        r = requests.get(st_url, headers=headers, verify=False)
        cookies = r.cookies.get("JSESSIONID")
        return cookies
    except:
        return {}


headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Referer": f"http://www.ccgp-jiangsu.gov.cn/jiangsu/cggg_search.html?lmid=cggg&qh=notic_c2&_t={int(time.time() * 1000)}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

cookies = {"JSESSIONID": get_request_cookies(st_url, headers)}


def ocr_num():
    """
    根据链接获取到返回的验证码图片 并进行识别
    """
    url = f"http://www.ccgp-jiangsu.gov.cn/pss/servlet/validateCodeServlet?{int(time.time() * 1000)}"
    r = requests.get(url, headers=headers, cookies=cookies)
    ocr = ddddocr.DdddOcr()
    res = ocr.classification(r.content)
    return res


class ExampleSpider(scrapy.Spider):
    name = "jiangsu_ggjy"
    # allowed_domains = ["http://www.ccgp-jiangsu.gov.cn/pss/jsp/search_cggg.jsp"]
    start_urls = "http://www.ccgp-jiangsu.gov.cn/pss/jsp/search_cggg.jsp"
    page = 1
    page_all = 1
    repetition_num = 0
    page_time = ""
    current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

    gglx_dict = {
        "cgyx": "采购意向",
        "dyly": "单一来源公示",
        "zgys": "资格预审",
        "cggg": "采购公告",
        "zjgg": "征集公告",
        "rwjg": "入围结果公告",
        "zbgg": "中标公告",
        "cjgg": "成交公告",
        "zzgg": "终止公告",
        "gzgg": "更正公告",
        "jzcs": "集中采购",
        "gkzb": "公开招标",
        "htgg": "合同公告",
        "cjhz": "成交结果汇总公告",
        "qtgg": "其他公告",
    }

    headers_ = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://www.ccgp-jiangsu.gov.cn",
        "Referer": "http://www.ccgp-jiangsu.gov.cn/jiangsu/js_cggg/details.html?gglb=cgyx&ggid=21526dd15e4b41069763a1228800cfd7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    def start_requests(self):
        verifyCode = ocr_num()
        params = {
            "cgr": "",
            "xmbh": "",
            "pqy": "",
            # "sd": str(int(time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")) * 1000)),
            # "ed": str(
            #     int(time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")) * 1000)
            #     + 86399000
            # ),
            "sd": "1688572800000",
            "ed": "1688659199000",
            "dljg": "",
            "cglx": "",
            "bt": "",
            "code": str(verifyCode),
            "nr": "",
            "cgfs": "",
            "page": "1",
        }
        yield scrapy.Request(
            # url=f"http://www.ccgp-jiangsu.gov.cn/pss/jsp/search_cggg.jsp?cgr=&xmbh=&pqy=&sd=1688572800000&ed=1688659199000&dljg=&cglx=&bt=&code={ccc}&nr=&cgfs=&page=1",
            url=f'http://www.ccgp-jiangsu.gov.cn/pss/jsp/search_cggg.jsp?cgr=&xmbh=&pqy=&sd={str(int(time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")) * 1000))}&ed={str(int(time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")) * 1000) + 86399000)}&dljg=&cglx=&bt=&code={verifyCode}&nr=&cgfs=&page=1',
            headers=headers,
            cookies=cookies,
            dont_filter=True,
            callback=self.parse_1,
            method="GET",
        )

    def parse_1(self, response, **kwargs):
        res = json.loads(response.text)
        time.sleep(1)
        if res.get("message") == "验证码不正确。" and self.repetition_num < 10:
            self.repetition_num += 1
            verifyCode = ocr_num()
            logging.debug(f"==========验证码未识别成功，正在第{self.repetition_num}次重新识别=============")
            params = {
                "cgr": "",
                "xmbh": "",
                "pqy": "",
                "sd": str(
                    int(time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")) * 1000)
                ),
                "ed": str(
                    int(time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")) * 1000)
                    + 86399000
                ),
                "dljg": "",
                "cglx": "",
                "bt": "",
                "code": str(verifyCode),
                "nr": "",
                "cgfs": "",
                "page": "1",
            }
            yield scrapy.FormRequest(
                # url=f'http://www.ccgp-jiangsu.gov.cn/pss/jsp/search_cggg.jsp?cgr=&xmbh=&pqy=&sd={str(int(time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")) * 1000))}&ed={str(int(time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")) * 1000) + 86399000)}&dljg=&cglx=&bt=&code={verifyCode}&nr=&cgfs=&page={self.page}',
                url=response.url,
                headers=headers,
                cookies=cookies,
                # formdata=params,
                dont_filter=True,
                callback=self.parse_1,
                method="GET",
            )
        if self.repetition_num >= 10:
            logging.debug("==========验证码识别失败次数过多，程序退出============")
        elif self.repetition_num < 10 and res.get("result").get("list"):
            self.repetition_num = 0
            list_data = res["result"]["list"]
            meta = response.meta
            for each in list_data:
                title = each.get("title")
                ggCode = each.get("ggCode")
                id_ = each.get("id")
                pZoneName = each.get("pZoneName")
                zoneName = each.get("zoneName")
                publishDate = each.get("publishDate")
                self.page_time = publishDate[:10]
                detail_url = f"http://www.ccgp-jiangsu.gov.cn/jiangsu/js_cggg/details.html?gglb={ggCode}&ggid={id_}"
                json_url_ById = "http://www.ccgp-jiangsu.gov.cn/pss/jsp/relevantCgggGetById.jsp"
                # json_url_ProjId = "http://www.ccgp-jiangsu.gov.cn/pss/jsp/relevantCgggListByProjId.jsp"
                yield scrapy.FormRequest(
                    url=json_url_ById,
                    headers=self.headers_,
                    cookies=cookies,
                    formdata={"ggid": id_},
                    callback=self.detail_parse,
                    meta={
                        "detail_url": detail_url,
                        "title": title,
                        "id_": id_,
                        "ggCode": ggCode,
                        "pZoneName": pZoneName,
                        "zoneName": zoneName,
                        "publishDate": publishDate,
                    },
                    method="POST",
                )
            if self.current_time == self.page_time:
                self.page += 1
                verifyCode = ocr_num()
                yield scrapy.FormRequest(
                    # url=f"http://www.ccgp-jiangsu.gov.cn/pss/jsp/search_cggg.jsp?cgr=&xmbh=&pqy=&sd=1688572800000&ed=1688659199000&dljg=&cglx=&bt=&code={ccc}&nr=&cgfs=&page=1",
                    url=f'http://www.ccgp-jiangsu.gov.cn/pss/jsp/search_cggg.jsp?cgr=&xmbh=&pqy=&sd={str(int(time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")) * 1000))}&ed={str(int(time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")) * 1000) + 86399000)}&dljg=&cglx=&bt=&code={verifyCode}&nr=&cgfs=&page={self.page}',
                    headers=headers,
                    cookies=cookies,
                    dont_filter=True,
                    callback=self.parse_1,
                    method="GET",
                )

    def detail_parse(self, response, **kwargs):
        res_t = json.loads(response.text)
        meta = response.meta
        data = res_t.get("data")
        item = GovernmentProcurementItem()
        item["po_id"] = get_md5(meta.get("id_"))
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = meta.get("detail_url")
        item["po_province"] = "江苏省"
        item["po_city"] = meta.get("pZoneName")
        item["po_county"] = meta.get("zoneName")
        item["po_zone"] = ""
        item["po_category"] = "政府采购"
        item["po_info_type"] = self.gglx_dict.get(meta.get("ggCode")) or ""
        item["po_source"] = "江苏政府采购网"
        item["bo_name"] = meta.get("title")
        item["po_public_time"] = meta.get("publishDate")
        item["po_html_con"] = str(data.get("content")).replace("'", '"') or str(data.get("extend")).replace("'", '"')
        item["po_content"] = (
            pq(data.get("content")).text() if data.get("content") else str(data.get("extend")).replace("'", '"')
        )
        item["po_json_data"] = str(res_t).replace("'", '"')
        item["description"] = ""
        item["website_name"] = "江苏政府采购网"
        item["website_url"] = "http://www.ccgp-jiangsu.gov.cn/"
        yield item
