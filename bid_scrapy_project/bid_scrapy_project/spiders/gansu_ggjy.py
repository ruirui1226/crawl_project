# -*- coding: utf-8 -*-
"""
@desc: 甘肃省公共资源交易中心-待完成
@version: python3
@author: shenr
@time: 2023/06/14
"""
import base64
import json
import re
import time

import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


class ExampleSpider(scrapy.Spider):
    name = "gansu_ggjy"
    allowed_domains = ["https://pzxx.ggzyjy.gansu.gov.cn/f/newprovince/annogoods/list"]
    start_urls = "https://pzxx.ggzyjy.gansu.gov.cn/f/newprovince/annogoods/list"
    list_urls = "https://pzxx.ggzyjy.gansu.gov.cn/f/newprovince/annogoods/getAnnoList"
    page = 0
    page_all = 1

    headers = {
        "authority": "pzxx.ggzyjy.gansu.gov.cn",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "referer": "https://pzxx.ggzyjy.gansu.gov.cn/f/Economization/newsTradeIndex",
        "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    cookies = {
        "JSESSIONID": "9BBA715DF387106212B2C0E32425BB8D",
        "yfx_c_g_u_id_10000005": "_ck23041809165813498211680198955",
        "pageNo": "0",
        "jeeplus.session.id": "c970177e8c4245c187cca3c95d839b29",
        "yfx_f_l_v_t_10000005": "f_t_1681780618340__r_t_1686632763211__v_t_1686637017649__r_c_1",
    }

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls,
            headers=self.headers,
            cookies=self.cookies,
            dont_filter=True,
            callback=self.parse_1,
        )

    def parse_1(self, response, **kwargs):
        pq_res = pq(response.text)
        div_dq = pq_res('dl[class="sTradingInformationType clear areaType"] dt ul li')
        sjdm_list = []
        other_list = []
        xqdm_list = []
        dq_list = []
        for each in div_dq.items():
            dq_list.append(
                {each('label[class="icheck-radio"]').text(): each('label[class="icheck-radio"] input').attr("value")}
            )
        div_jylx = pq_res('dl[class="sTradingInformationType clear main-projecttype"] dt ul li')
        for rows in div_jylx.items():
            jydm = {rows('label[class="icheck-radio"]').text(): rows('input[type="radio"]').attr("value")}
            sjdm_list.append(jydm)
            if rows('label[class="icheck-radio"]').text() in ("工程建设", "政府采购", "土地和矿业权", "药品采购"):
                other_list.append(jydm)
            if rows('label[class="icheck-radio"]').text() in ("工程建设", "政府采购", "土地和矿业权", "招标计划"):
                xqdm_list.append(jydm)
        print(dq_list)
        print(sjdm_list)
        print(other_list)
        print(xqdm_list)
        # 进入列表页
        for dq in dq_list:
            if list(dq.keys())[0] == "省级平台（中心）":
                for dm in sjdm_list:
                    params = {
                        "pageNo": "0",
                        "pageSize": "",
                        "area": str(list(dq.values())[0]),
                        "projecttype": str(list(dm.values())[0]),
                        "prjpropertynewI": "I",
                        "prjpropertynewA": "A",
                        "prjpropertynewD": "D",
                        "prjpropertynewC": "C",
                        "prjpropertynewB": "B",
                        "prjpropertynewE": "E",
                        "prjpropertynewZ": "Z",
                        "projectname": "",
                    }
                    yield scrapy.FormRequest(
                        url=self.list_urls,
                        headers=self.headers,
                        formdata=params,
                        callback=self.parse_list,
                        dont_filter=True,
                        method="POST",
                        meta={
                            "area": str(list(dq.values())[0]),
                            "city": list(dq.keys())[0],
                            "category": list(dm.keys())[0],
                            "projecttype": str(list(dm.values())[0]),
                        },
                    )
            if list(dq.keys())[0] == "省级平台（兰州新区）":
                for dm in xqdm_list:
                    params = {
                        "pageNo": "0",
                        "pageSize": "",
                        "area": str(list(dq.values())[0]),
                        "projecttype": str(list(dm.values())[0]),
                        "prjpropertynewI": "I",
                        "prjpropertynewA": "A",
                        "prjpropertynewD": "D",
                        "prjpropertynewC": "C",
                        "prjpropertynewB": "B",
                        "prjpropertynewE": "E",
                        "prjpropertynewZ": "Z",
                        "projectname": "",
                    }
                    yield scrapy.FormRequest(
                        url=self.list_urls,
                        headers=self.headers,
                        formdata=params,
                        callback=self.parse_list,
                        dont_filter=True,
                        method="POST",
                        meta={
                            "area": str(list(dq.values())[0]),
                            "city": list(dq.keys())[0],
                            "category": list(dm.keys())[0],
                            "projecttype": str(list(dm.values())[0]),
                        },
                    )
            else:
                for dm in other_list:
                    params = {
                        "pageNo": "0",
                        "pageSize": "",
                        "area": str(list(dq.values())[0]),
                        "projecttype": str(list(dm.values())[0]),
                        "prjpropertynewI": "I",
                        "prjpropertynewA": "A",
                        "prjpropertynewD": "D",
                        "prjpropertynewC": "C",
                        "prjpropertynewB": "B",
                        "prjpropertynewE": "E",
                        "prjpropertynewZ": "Z",
                        "projectname": "",
                    }
                    yield scrapy.FormRequest(
                        url=self.list_urls,
                        headers=self.headers,
                        formdata=params,
                        callback=self.parse_list,
                        dont_filter=True,
                        method="POST",
                        meta={
                            "area": str(list(dq.values())[0]),
                            "city": list(dq.keys())[0],
                            "category": list(dm.keys())[0],
                            "projecttype": str(list(dm.values())[0]),
                        },
                    )

    def parse_list(self, response, **kwargs):
        """逐一访问列表页"""
        res = pq(response.text)
        meta = response.meta
        area = meta.get("area")
        city = meta.get("city")
        category = meta.get("category")
        projecttype = meta.get("projecttype")
        sDisclosurLeftConDetailList = res('dl[class="sDisclosurLeftConDetailList"]')
        for each in sDisclosurLeftConDetailList.items():
            tenderprojectid = re.findall("loadTender\('(.*?)'\,'", str(each), re.S)[0]
            if not tenderprojectid:
                tenderprojectid = re.findall("tenderproject/(.*?)/loadTenderprojectIndex", str(each), re.S)[0]
            detail_url = "https://pzxx.ggzyjy.gansu.gov.cn/f/newprovince/tenderproject/flowpage"
            params = {"bidpackages": "", "tenderprojectid": str(tenderprojectid[0]), "index": "0", "area": str(area)}
            bs_code = base64.b64encode(str(tenderprojectid[0]).encode()).decode()
            detail_get_url = (
                f"https://pzxx.ggzyjy.gansu.gov.cn/f/newprovince/tenderproject/{bs_code}/tenderprojectIndex?area={area}"
            )
            yield scrapy.FormRequest(
                url=detail_url,
                formdata=params,
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse_detail,
                dont_filter=True,
                method="POST",
                meta={
                    "tenderprojectid": tenderprojectid,
                    "city": city,
                    "category": category,
                    "detail_get_url": detail_get_url,
                },
            )
        if self.page == 1:
            self.page_all = re.findall("总共 (.*?) 条记录", str(res), re.S)[0]

        self.page += 1
        if self.page / 10 > int(self.page_all):
            if str(area) == "620000":
                params = {
                    "pageNo": self.page,
                    "pageSize": 10,
                    "area": area,
                    "projecttype": projecttype,
                    "prjpropertynewI": "I",
                    "prjpropertynewA": "A",
                    "prjpropertynewD": "D",
                    "prjpropertynewC": "C",
                    "prjpropertynewB": "B",
                    "prjpropertynewE": "E",
                    "prjpropertynewZ": "Z",
                    "projectname": "",
                }
                yield scrapy.FormRequest(
                    url=self.list_urls,
                    headers=self.headers,
                    formdata=params,
                    callback=self.parse_list,
                    dont_filter=True,
                    method="POST",
                    meta={
                        "area": area,
                        "city": city,
                        "category": category,
                        "projecttype": projecttype,
                    },
                )
            if str(area) == "620001":
                params = {
                    "pageNo": self.page,
                    "pageSize": 10,
                    "area": area,
                    "projecttype": projecttype,
                    "prjpropertynewI": "I",
                    "prjpropertynewA": "A",
                    "prjpropertynewD": "D",
                    "prjpropertynewC": "C",
                    "prjpropertynewB": "B",
                    "prjpropertynewE": "E",
                    "prjpropertynewZ": "Z",
                    "projectname": "",
                }
                yield scrapy.FormRequest(
                    url=self.list_urls,
                    headers=self.headers,
                    formdata=params,
                    callback=self.parse_list,
                    dont_filter=True,
                    method="POST",
                    meta={
                        "area": area,
                        "city": city,
                        "category": category,
                        "projecttype": projecttype,
                    },
                )
            else:
                params = {
                    "pageNo": self.page,
                    "pageSize": 10,
                    "area": area,
                    "projecttype": projecttype,
                    "prjpropertynewI": "I",
                    "prjpropertynewA": "A",
                    "prjpropertynewD": "D",
                    "prjpropertynewC": "C",
                    "prjpropertynewB": "B",
                    "prjpropertynewE": "E",
                    "prjpropertynewZ": "Z",
                    "projectname": "",
                }
                yield scrapy.FormRequest(
                    url=self.list_urls,
                    headers=self.headers,
                    formdata=params,
                    callback=self.parse_list,
                    dont_filter=True,
                    method="POST",
                    meta={
                        "area": area,
                        "city": city,
                        "category": category,
                        "projecttype": projecttype,
                    },
                )

    def parse_detail(self, response, **kwargs):
        res = pq(response.text)
        meta = response.meta
        tenderprojectid = meta.get("tenderprojectid")
        city = meta.get("city")
        category = meta.get("category")
        detail_get_url = meta.get("detail_get_url")
        item = BidScrapyProjectItem()
        item["bid_id"] = get_md5(tenderprojectid)
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = detail_get_url
        item["bid_md5_url"] = ""
        item["bid_province"] = "甘肃省"
        item["bid_city"] = city
        item["bid_county"] = ""
        item["bid_category"] = category
        item["bid_info_type"] = ""
        item["bid_source"] = "https://pzxx.ggzyjy.gansu.gov.cn/f/newprovince/annogoods/list"
        item["bid_name"] = res('div[class="jxTenderObjMain"] table tr td').eq(1).text()
        item["bid_public_time"] = re.findall("项目进场日期：\" [+] '(.*?)'\)", str(res), re.S)[0].replace("'", '"')
        item["bid_html_con"] = res.html().replace("'", '"')
        item["bid_content"] = res.text().replace("'", '"')
        item["description"] = ""
        item["website_name"] = "甘肃省公共资源交易中心"
        item["website_url"] = "https://pzxx.ggzyjy.gansu.gov.cn/"

        yield item
