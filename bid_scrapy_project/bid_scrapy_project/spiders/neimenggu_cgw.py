#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 14:30
# @Author  : xm
# @File    : neimenggu_cgw.py
# @Description : 内蒙古自治区政府采购网
import json
import random
import time

import ddddocr
import requests
import scrapy

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import GovernmentProcurementItem


class NeimengguCgwSpider(scrapy.Spider):
    """
    记录：需要用 https://www.ccgp-neimenggu.gov.cn/category/cgggg 给的cookie 去请求验证码
    """

    name = "neimenggu_cgw"

    def __init__(self):
        self.category = "政府采购"
        self.citys = {
            "内蒙古自治区本级": "150000",
            "呼和浩特市": "150100",
            "包头市": "150200",
            "呼伦贝尔市": "150700",
            "兴安盟": "152200",
            "通辽市": "150500",
            "赤峰市": "150400",
            "锡林郭勒盟": "152500",
            "乌兰察布市": "150900",
            "鄂尔多斯市": "150600",
            "巴彦淖尔市": "150800",
            "乌海市": "150300",
            "阿拉善盟": "152900",
            "满洲里市": "150781",
            "二连浩特市": "152501",
        }
        self.province = "内蒙古自治区"
        # area 城市id  listcode 验证码  type_name 类型
        self.params = {
            "type_name": "1",
            "purmet": "",
            "area": "150000",
            "keyword": "",
            "annstartdate_S": "",
            "annstartdate_E": "",
            "annenddate_S": "",
            "annenddate_E": "",
            "byf_page": "1",
            "fun": "cggg",
            "page_size": "18",
            "listcode": "10",
        }
        self.webname = "内蒙古自治区政府采购网"
        self.webUrl = "https://www.ccgp-neimenggu.gov.cn/"
        self.apiUrl = "https://www.ccgp-neimenggu.gov.cn/zfcgwslave/web/index.php?r=pro%2Fanndata"
        self.types = {
            "资格预审公告": "6",
            "资格预审更正公告": "7",
            "招标公告": "1",
            "招标更正公告": "2",
            "中标(成交)公告": "3",
            "中标(成交)更正公告": "4",
            "合同公告": "8",
            "履约验收公示": "10",
            "废标公告": "5",
        }
        self.page = 2
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "Cookie": "PHPSESSID=q1cfphvl1t487it8299lj894o2;",
        }
        self.now_data = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

    def start_requests(self):
        """
        列表页的列表类型
        """
        cookie = self.getCookie()
        if not cookie:
            return
        code = None
        try:
            code = self.getNum(cookie)
        except:
            print("验证码获取错误")
            code = None
        if not code:
            return
        print(cookie, code)
        for cityname, cityid in self.citys.items():
            for typename, typeid in self.types.items():
                for i in range(1, self.page):
                    self.params["type_name"] = typeid
                    self.params["area"] = cityid
                    self.params["listcode"] = str(code)
                    self.params["annstartdate_S"] = self.now_data
                    self.params["annstartdate_E"] = self.now_data
                    self.params["byf_page"] = str(i)
                    # self.headers["Cookie"] = cookie

                    cookie = cookie.split(";")[0]
                    items = {"city": cityname, "type": typename, "typeid": typeid, "cityid": cityid, "page": i}
                    yield scrapy.FormRequest(
                        self.apiUrl,
                        formdata=self.params,
                        dont_filter=True,
                        callback=self.parse,
                        headers=self.headers,
                        cookies={cookie.split("=")[0]: cookie.split("=")[1]},
                        meta={"items": items},
                    )

    def parse(self, response, **kwargs):
        """
        列表页
        """
        print("=========内蒙古{}开始采集第{}页=======".format(response.meta["items"]["type"], response.meta["items"]["page"]))
        if "[[]" in response.text:
            print("没有新数据退出")
            return

        if '[null,0,"no"]' in response.text:
            ##验证码失效重试
            cookie = self.getCookie()
            cookie = cookie.split(";")[0]
            code = None
            try:
                code = self.getNum(cookie)
            except:
                print("预防出现 1减n2的情况")
                code = self.getNum()
            if not code:
                return
            num = response.meta.get("num")
            if not num:
                num = 2
            else:
                num += 1
            if num > 3:
                return
            self.params["type_name"] = response.meta["items"]["typeid"]
            self.params["area"] = response.meta["items"]["cityid"]
            self.params["listcode"] = str(code)
            self.params["annstartdate_S"] = self.now_data
            self.params["annstartdate_E"] = self.now_data
            self.params["byf_page"] = str(response.meta["items"]["page"])
            items_num = {}
            items_num.update(response.meta)
            items_num["num"] = num
            return scrapy.FormRequest(
                self.apiUrl,
                formdata=self.params,
                dont_filter=True,
                callback=self.parse,
                headers=self.headers,
                cookies={cookie.split("=")[0]: cookie.split("=")[1]},
                meta=items_num,
            )
        # 数据处理
        jsonDict = json.loads(response.text)
        datas = jsonDict[0]
        for data in datas:
            title = data.get("TITLE")
            contentid = data.get("wp_mark_id")
            #'[发布：2020-10-28]'
            pubdatStr = data.get("SUBDATE")
            # pubdate = pubdatStr[pubdatStr.index("发布：") + len("发布：") : pubdatStr.rindex("]")]
            tb_id = response.meta["items"]["typeid"]
            type = data.get("type")
            link = "https://www.ccgp-neimenggu.gov.cn/category/cgggg?tb_id={}&p_id={}&type={}".format(
                tb_id, contentid, type
            )
            items = {"title": title, "link": link}
            items.update(response.meta["items"])
            yield scrapy.Request(link, callback=self.contentParse, meta={"items": items})

    def contentParse(self, response):
        item_info = response.meta["items"]
        content_html = response.css("div.content-box-1").get()
        contents = response.css("div.content-box-1 *::text").extract()
        content = remove_node(content_html, ["style"]).text
        ##发布时间
        pubdate = response.css(".feed-time::text").get()
        pubdatetime = pubdate[pubdate.index("发布时间：") + len("发布时间：") :].strip()
        timeArray = time.strptime(pubdatetime, "%Y年%m月%d日")
        pubdatetime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        items = {
            "po_id": get_md5(item_info.get("link")),
            "bid_url": item_info.get("link"),
            "po_province": self.province,
            "po_city": item_info.get("city"),
            "po_category": self.category,
            "po_info_type": item_info.get("type"),
            "po_public_time": pubdatetime,
            "bo_name": item_info.get("title"),
            "po_html_con": content_html,
            "po_content": content,
            "website_name": self.webname,
            "website_url": self.webUrl,
            "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }
        item_po = GovernmentProcurementItem()
        item_po.update(items)
        # print(items["po_id"])
        yield item_po

    # 工具
    def getNum(self, cookie=None, num=0):
        if num > 10:
            return None
        url = "https://www.ccgp-neimenggu.gov.cn/wp-content/themes/zfcgw_red/security_code/security_code.php?{}".format(
            random.random()
        )
        # r = requests.get(url, headers={"cookie": cookie})
        r = requests.get(
            url,
            headers={
                # "cookie": "PHPSESSID=760rud2ivq5d7fpfj8dmtaogg2",
                "cookie": cookie,
                "Referer": "https://www.ccgp-neimenggu.gov.cn/category/cgggg",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
            },
        )
        ocr = ddddocr.DdddOcr()
        res = ocr.classification(r.content)
        print(res)
        f = lambda x="ddd": sum([1 if "\u4e00" <= i <= "\u9fff" else 0 for i in x]) > 0
        if f(res):
            try:
                if "加" in res:
                    return int(res.split("加")[0]) + int(res.split("加")[1])
                elif "乘" in res:
                    return int(res.split("乘")[0]) * int(res.split("乘")[1])
                elif "减" in res:
                    return int(res.split("减")[0]) - int(res.split("减")[1])
                elif "除" in res:
                    return int(res.split("除")[0]) / int(res.split("除")[1])
                else:
                    time.sleep(0.5)
                    num += 1
                    return self.getNum(cookie, num)
            except:
                print("格式问题 重试", res)
                time.sleep(0.5)
                num += 1
                return self.getNum(cookie, num)
        else:
            # 做个重试
            time.sleep(0.5)
            num += 1
            return self.getNum(cookie, num)

    def getCookie(self):
        """
        获取cookie
        """
        for i in range(3):
            s = requests.get("https://www.ccgp-neimenggu.gov.cn/category/cgggg")
            if s.headers.get("Set-Cookie"):
                return s.headers.get("Set-Cookie")
