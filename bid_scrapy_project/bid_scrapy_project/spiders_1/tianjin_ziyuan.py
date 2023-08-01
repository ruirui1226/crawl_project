# -*- coding: utf-8 -*-
"""
@desc: 天津建设工程信息网
@version: python3
@author: shenr
@time: 2023/07/19
"""
import json
import logging
import re
import time
import scrapy
from pyquery import PyQuery as pq
from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import GovernmentProcurementItem, BidScrapyProjectItem


class ExampleSpider(scrapy.Spider):
    name = "tianjin_ziyuan"
    start_urls = "http://www.tjconstruct.cn/Zbgg/Index/1"
    page = 1
    page_all = 1
    page_time = ""
    current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Referer": "http://www.tjconstruct.cn/Zbgg/Index/1?type=jlzb",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    cookies = {
        "ASP.NET_SessionId": "rrf4jalxeghdztfe1mcsevcm",
        "_gscu_1736133345": "89756801cyo3h724",
        "_gscbrs_1736133345": "1",
        "_gscs_1736133345": "t8981491576ualf18|pv:2"
    }
    # 招标公告
    type_zbgg = {
        "sgzb": "施工招标",
        "jlzb": "监理招标",
        "sjzb": "设计招标",
        "sbzb": "设备招标",
        "qtzb": "专业招标",
    }
    # 中标公告
    type_Zbgg = {
        "sgzb": "施工中标",
        "jlzb": "监理中标",
        "sjzb": "设计中标",
        "sbzb": "设备中标",
        "qtzb": "专业中标",
    }

    def start_requests(self):
        for each_k, each_v in self.type_zbgg.items():
            params = {"type": each_k}
            yield scrapy.FormRequest(
                url=self.start_urls,
                headers=self.headers,
                cookies=self.cookies,
                dont_filter=True,
                method="GET",
                formdata=params,
                callback=self.parse_1,
                meta={"_v": each_v, "_type": "招标公告"},
            )
        for rows_k, rows_v in self.type_Zbgg.items():
            params = {"type": rows_k}
            yield scrapy.FormRequest(
                url="http://www.tjconstruct.cn/Zbgs/Index/1",
                headers=self.headers,
                cookies=self.cookies,
                dont_filter=True,
                method="GET",
                formdata=params,
                callback=self.parse_1,
                meta={"_v": rows_v, "_type": "中标公告"},
            )

    def parse_1(self, response, **kwargs):
        res = pq(response.text)
        meta = response.meta
        _v = meta.get("_v")
        _type = meta.get("_type")
        table = res('table[class="t1"] tr')
        for each in table.items():
            title = each('td a').text()
            if title:
                detail_url = "http://www.tjconstruct.cn/" + each('td a').attr("href")
                pubtime_ = each('td').eq(3).text()
                timeArray = time.strptime(pubtime_, "%Y/%m/%d")
                ts = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                yield scrapy.Request(
                    url=detail_url,
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.detail_parse,
                    meta={"title": title, "pubtime_": ts, "_v": _v, "_type": _type}
                )

    def detail_parse(self, response, **kwargs):
        res = pq(response.text)
        meta = response.meta
        item = BidScrapyProjectItem()
        item["bid_id"] = get_md5(response.url)
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = response.url
        item["bid_md5_url"] = ""
        item["bid_province"] = "天津市"
        item["bid_city"] = "天津市"
        item["bid_county"] = ""
        item["bid_category"] = meta.get("_v")
        item["bid_info_type"] = meta.get("_type")
        item["bid_source"] = "天津市公共资源交易中心(天津市政府采购中心)"
        item["bid_name"] = meta.get("title")
        item["bid_public_time"] = meta.get("pubtime_")
        item["bid_html_con"] = str(res).replace("'", '"')
        item["bid_content"] = res.text()
        item["description"] = ""
        item["website_name"] = "天津市公共资源交易中心(天津市政府采购中心)"
        item["website_url"] = "http://www.tjconstruct.cn"
        logging.debug(f"数据======{item}")
        yield item
