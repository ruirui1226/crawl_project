#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/7/12 15:11
@Author : zhangpf
@File : huizhaobiao.py
@Desc : 惠招标-请求限制
@Software: PyCharm
"""
import json
import math
import re
import time

import scrapy
from loguru import logger

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class huizhaobiaoSpider(scrapy.Spider):
    name = "huizhaobiao"
    source_url = "http://www.hbidding.com/"
    list_url = "http://www.hbidding.com/web/index/information/getjyinfopg.json?random=1689155470560&pageindex=1&pagesize=10&type={}&citycode=&hycode=&leixing=&zbdl=&searchtype=ggname&searchcontent=&starttime=&endtime="
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Cookie": "UM_distinctid=1894959aa3ed53-02522b407317f3-26031d51-1fa400-1894959aa3f1f59; CNZZDATA1281276074=1181723066-1689150640-%7C1689150640",
        "Referer": "http://www.hbidding.com/hbiddingWeb/pages/jyinfo/list.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "pageuser": "",
    }
    url_code_list = [
        "zbgg",
        "bggg",
        "bydy",
        "hxrgs",
        "ycgg",
        "zhongbiaogg",
    ]

    # url_code_list = [
    #     "zbgg",
    #     # "bggg",
    #     # "bydy",
    #     # "hxrgs",
    #     # "ycgg",
    #     # "zhongbiaogg",
    # ]

    custom_settings = {"CONCURRENT_REQUESTS": 1, "DOWNLOAD_DELAY": 3}

    def start_requests(self):
        for code in self.url_code_list:
            yield scrapy.Request(
                url=self.list_url.format(code),
                headers=self.headers,
                callback=self.get_totals,
                dont_filter=True,
                cb_kwargs={"code": code},
            )

    def get_totals(self, response, code):
        response = json.loads(response.text)
        total = response.get("total")
        totals = math.ceil(int(total) / 10)
        for i in range(1, 3):
            yield scrapy.Request(
                url=f"http://www.hbidding.com/web/index/information/getjyinfopg.json?random=1689155470560&pageindex={i}&pagesize=10&type={code}&citycode=&hycode=&leixing=&zbdl=&searchtype=ggname&searchcontent=&startti                                                me=&endtime=",
                headers=self.headers,
                callback=self.get_list_page,
                dont_filter=True,
                cb_kwargs={"code": code},
            )

    def get_list_page(self, response, **kwargs):
        # print(response.text)
        response = json.loads(response.text)
        data_list = response.get("rows")
        for data in data_list:
            ggcode = data.get("ggcode")
            leixing = data.get("leixing")
            url = f"http://www.hbidding.com/hbiddingWeb/pages/jyinfo/detail.html?active=0&&infoid={ggcode}&&categoryid={kwargs['code']}"
            if kwargs["code"] == "zbgg":
                detail_url = f"http://www.hbidding.com/web/index/notice/zbggDetail?random=1689211028158&infoid={ggcode}&categoryid={kwargs['code']}"
            else:
                detail_url = f"http://www.hbidding.com/web/index/information/getjyinfodetail.json?random=1689213293460&infoid={ggcode}&categoryid={kwargs['code']}"
            yield scrapy.Request(
                url=detail_url,
                callback=self.detail_page,
                headers=self.headers,
                cb_kwargs={"detail_url": detail_url, "code": kwargs["code"], "url": url, "leixing": leixing},
            )

    def detail_page(self, response, **kwargs):
        res = json.loads(response.text)
        data = res.get("tdata")
        bid_public_time = data.get("Data_ggfbtime")
        Data_title = data.get("Data_title")
        po_category = data.get("title_page")
        po_info_type = data.get("zbfsname")
        cityname = data.get("cityname")
        po_city = cityname.split("-")[0]
        po_zone = cityname.split("-")[1]
        # zbprocode = data.get("zbprocode")
        Data_content = data.get("Data_content")
        pre = re.compile(">(.*?)<")
        bid_content = "".join(pre.findall(str(Data_content)))
        if kwargs["leixing"] == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(kwargs["detail_url"])
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = kwargs["url"]
            item["po_province"] = "河北省"
            item["po_city"] = po_city
            item["po_zone"] = po_zone
            item["po_category"] = po_category
            item["po_info_type"] = kwargs["leixing"]
            item["bo_name"] = Data_title
            item["po_public_time"] = bid_public_time
            item["po_html_con"] = Data_content
            item["po_content"] = bid_content
            item["website_name"] = "惠招标"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = kwargs["detail_url"]
            item["po_json_data"] = response.text
            # print(item)
            # yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(kwargs["url"])
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = kwargs["url"]
            item["bid_province"] = "河北省"
            item["bid_city"] = po_city
            item["bid_zone"] = po_zone
            item["bid_category"] = po_category
            item["bid_info_type"] = kwargs["leixing"]
            item["bid_name"] = Data_title
            item["bid_public_time"] = bid_public_time
            item["bid_html_con"] = Data_content
            item["bid_content"] = bid_content
            item["website_name"] = "惠招标"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = kwargs["detail_url"]
            item["bid_json_data"] = response.text
            # print(item)
            # yield item
