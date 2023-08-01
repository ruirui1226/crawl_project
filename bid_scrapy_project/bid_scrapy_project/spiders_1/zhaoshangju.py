# -*- coding: utf-8 -*-
"""
@desc: 招商局集团-ip封禁
@version: python3
@author: shenr
@time: 2023/07/18
"""
import json
import re
import time
import scrapy
from pyquery import PyQuery as pq
from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import GovernmentProcurementItem


class ExampleSpider(scrapy.Spider):
    name = "zhaoshangju"
    start_urls = "https://dzzb.ciesco.com.cn/gg/cgggList"
    page = 1
    page_all = 1
    page_time = ""
    current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    custom_settings = {"CONCURRENT_REQUESTS": 1, "DOWNLOAD_DELAY": 2}

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://dzzb.ciesco.com.cn",
        "Referer": "https://dzzb.ciesco.com.cn/gg/cgggList.do",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }
    cookies = {"SF_cookie_199": "78866174", "SF_cookie_198": "18449693"}

    def start_requests(self):
        data = {
            "currentPage": "1",
            "xmLeiXing": "",
            "zbFangShi": "",
            "jiTuanId": "",
            "danWei": "",
            "xm_BH": "",
            "ggName": "",
            "zbr": "",
            "danWeiName": "",
            "keyWord": "",
        }
        yield scrapy.FormRequest(
            url=self.start_urls,
            headers=self.headers,
            cookies=self.cookies,
            body=json.dumps(data),
            dont_filter=True,
            method="POST",
            callback=self.parse_1,
        )

    def parse_1(self, response, **kwargs):
        res = pq(response.text)
        time_ = ""
        zbgg_table = res('div[class="list-content-between"]')
        for each in zbgg_table.items():
            title = each('span[class="list-content-start"] a').attr("title")
            if title:
                detail_url = "https://dzzb.ciesco.com.cn/" + each('span[class="list-content-start"] a').attr("href")
                time_ = each('span[class="list-content-end"]').text()
                if self.current_time == time_[:10]:
                    yield scrapy.Request(
                        url=detail_url,
                        headers=self.headers,
                        cookies=self.cookies,
                        callback=self.detail_parse,
                        meta={"title": title, "time_": time_},
                    )
        if self.current_time == time_[:10]:
            self.page += 1
            data = {
                "currentPage": f"{self.page}",
                "xmLeiXing": "",
                "zbFangShi": "",
                "jiTuanId": "",
                "danWei": "",
                "xm_BH": "",
                "ggName": "",
                "zbr": "",
                "danWeiName": "",
                "keyWord": "",
            }
            yield scrapy.Request(
                url=self.start_urls,
                headers=self.headers,
                cookies=self.cookies,
                body=json.dumps(data),
                dont_filter=True,
                method="POST",
                callback=self.parse_1,
            )

    def detail_parse(self, response, **kwargs):
        res = pq(response.text)
        meta = response.meta
        title = meta.get("title")
        time_ = meta.get("time_")
        if title in str(res):
            bid_html_con = str(res('div[class="template"]').html()).replace("'", '"')
            bid_content = str(res('div[class="template"]').text()).replace("'", '"')
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(response.url)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = response.url
            item["po_province"] = ""
            item["po_city"] = ""
            item["po_county"] = ""
            item["po_category"] = "采购公告"
            item["po_info_type"] = ""
            item["po_source"] = "招商局集团电子招标采购交易平台"
            item["bo_name"] = title
            item["po_public_time"] = time_
            item["po_html_con"] = bid_html_con
            item["po_content"] = bid_content
            item["description"] = ""
            item["website_name"] = "招商局集团电子招标采购交易平台"
            item["website_url"] = "https://dzzb.ciesco.com.cn/gg/cgggList"
            yield item
        else:
            guid_ = re.findall("guid=(.*?)&xinXi", str(response.url), re.S)[0]
            yield scrapy.Request(
                url=f"https://node.dzzb.ciesco.com.cn/xunjia-mh/gonggaoxinxi/gongGao_view_3.html?guid={guid_}&callBackUrl=https://dzzb.ciesco.com.cn/html/crossDomainForFeiZhaoBiao.html",
                headers=self.headers,
                cookies=self.cookies,
                callback=self.detail_guid_parse,
                meta={"title": title, "time_": time_},
            )

    def detail_guid_parse(self, response, **kwargs):
        res = pq(response.text)
        meta = response.meta
        title = meta.get("title")
        time_ = meta.get("time_")
        bid_html_con = str(res('div[class="divMainContent"]').html()).replace("'", '"')
        bid_content = str(res('div[class="divMainContent"]').text()).replace("'", '"')
        item = GovernmentProcurementItem()
        item["po_id"] = get_md5(response.url)
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = response.url
        item["po_province"] = ""
        item["po_city"] = ""
        item["po_county"] = ""
        item["po_category"] = "采购公告"
        item["po_info_type"] = ""
        item["po_source"] = "招商局集团电子招标采购交易平台"
        item["bo_name"] = title
        item["po_public_time"] = time_
        item["po_html_con"] = bid_html_con
        item["po_content"] = bid_content
        item["description"] = ""
        item["website_name"] = "招商局集团电子招标采购交易平台"
        yield item
