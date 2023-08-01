#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/7/18 9:11
@Author : zhangpf
@File : guotoujituan.py
@Desc : 国投集团
@Software: PyCharm
"""
import time

import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


class guotoujituanSpider(scrapy.Spider):
    name = "guotoujituan"
    source_url = "https://www.sdicc.com.cn/"
    list_url = [
        "https://www.sdicc.com.cn/cgxx/ggList",
        "https://www.sdicc.com.cn/cgxx/ggList?caiGouType=1",
        "https://www.sdicc.com.cn/cgxx/ggList?ggXingZhi=2",
        "https://www.sdicc.com.cn/cgxx/zbhxrList",
        "https://www.sdicc.com.cn/cgxx/zbjgList",
    ]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.sdicc.com.cn",
        "Referer": "https://www.sdicc.com.cn/",
        "Sec-Fetch-Dest": "iframe",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    data = {
        "caiGouDanWei": "",
        "currentPage": "1",
        "gcName": "",
        "zbFangShi": "",
        "xmLeiXing": "",
        "startTime": "",
        "endTime": "",
        "ggName": "",
    }

    def start_requests(self):
        for url in self.list_url:
            yield scrapy.FormRequest(
                url=url,
                headers=self.headers,
                callback=self.get_totals,
                dont_filter=True,
                formdata=self.data,
                method="POST",
                cb_kwargs={"url": url},
            )

    def get_totals(self, response, url):
        res = pq(response.text)
        totals = res('button[id="page_child1"]').text()
        # for i in range(1, int(totals + 1)):
        for i in range(1, 3):
            data = {
                "caiGouDanWei": "",
                "currentPage": str(i),
                "gcName": "",
                "zbFangShi": "",
                "xmLeiXing": "",
                "startTime": "",
                "endTime": "",
                "ggName": "",
            }
            yield scrapy.FormRequest(
                url=url,
                headers=self.headers,
                callback=self.get_list_page,
                formdata=data,
                method="POST",
                cb_kwargs={"url": url},
                dont_filter=True,
            )

    def get_list_page(self, response, url):
        res = pq(response.text)
        id_list = res('div[class="tbody"] table tbody tr').items()
        for id in id_list:
            onclick = id.attr("onclick")
            ggGuid = onclick.split("',")[0].split("('")[-1]  # 第一个
            gcGuid = onclick.split("','")[-1].split("')")[0]  # 第二个
            if id("td").eq(4).text() == "":
                time = id("td").eq(3).text()
            else:
                time = id("td").eq(4).text()
            if url == "https://www.sdicc.com.cn/cgxx/ggList?ggXingZhi=2":
                detail_url = f"https://www.sdicc.com.cn/cgxx/bgggDetail?ggGuid={ggGuid}&shiXiangGuid={gcGuid}"
            elif url == "https://www.sdicc.com.cn/cgxx/zbhxrList":
                detail_url = f"https://www.sdicc.com.cn/cgxx/zbhxrDetail?bdGuid={ggGuid}&guid={gcGuid}"
            elif url == "https://www.sdicc.com.cn/cgxx/zbjgList":
                detail_url = f"https://www.sdicc.com.cn/cgxx/zbjgDetail?bdGuid={ggGuid}&guid={gcGuid}"
            else:
                detail_url = f"https://www.sdicc.com.cn/cgxx/ggDetail?gcGuid={gcGuid}&ggGuid={ggGuid}"
            yield scrapy.Request(
                url=detail_url,
                headers=self.headers,
                callback=self.detail_page,
                cb_kwargs={"detail_url": detail_url, "time": time},
            )

    def detail_page(self, response, **kwargs):
        res = pq(response.text)
        title = res('h3[class="dg-notice-title"]').text()
        # bid_public_time = res('span[class="dg-notice-state-item"]').text().split("：")[-1].split(")")[0]
        bid_content = res('div[class="dg-notice-detail"]').text()
        bid_html_con = res('div[class="dg-notice-detail"]').outer_html()
        # po_category = res('span[class="dg-head-default"] a').eq(0).text()
        po_info_type = res('span[class="dg-head-default"] a').eq(1).text()
        item = BidScrapyProjectItem()
        item["bid_id"] = get_md5(kwargs["detail_url"])
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = kwargs["detail_url"]
        item["bid_category"] = "采购信息"
        item["bid_info_type"] = po_info_type
        item["bid_name"] = title
        item["bid_public_time"] = kwargs["time"]
        item["bid_html_con"] = bid_html_con
        item["bid_content"] = bid_content
        item["website_name"] = "国投集团电子采购平台"
        item["website_url"] = self.source_url
        item["bid_orgin_url"] = kwargs["detail_url"]
        # print(item)
        yield item
