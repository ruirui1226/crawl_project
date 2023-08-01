# -*- coding: utf-8 -*-
"""
@desc: 重庆市公共资源交易网
@version: python
@author: qth
@time: 2023/6/19
"""
import datetime
import json
import time
from pyquery import PyQuery as pq
from scrapy import Selector, Request, FormRequest
import scrapy
from gne import GeneralNewsExtractor
from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class ChongqingSpider(scrapy.Spider):
    name = "Chongqing"
    start_url = "https://www.cqggzy.com/interface/rest/esinteligentsearch/getFullTextDataNew"
    # custom_settings = {"CONCURRENT_REQUESTS": 2, "DOWNLOAD_DELAY": 1}
    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d")
    page = 20
    cookies = {
        "__jsluid_h": "49aea952c346617e0b85fa002ffbcadd",
        "__jsluid_s": "881a17a507933a51d808188ff6817286",
        "cookie_www": "19398923",
        "Hm_lvt_3b83938a8721dadef0b185225769572a": "1687137900,1687138236",
        "Hm_lpvt_3b83938a8721dadef0b185225769572a": "1687156249",
    }

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # 'Cookie': '__jsluid_h=49aea952c346617e0b85fa002ffbcadd; __jsluid_s=881a17a507933a51d808188ff6817286; cookie_www=19398923; Hm_lvt_3b83938a8721dadef0b185225769572a=1687137900,1687138236; Hm_lpvt_3b83938a8721dadef0b185225769572a=1687156249',
        "Origin": "https://www.cqggzy.com",
        "Pragma": "no-cache",
        "Referer": "https://www.cqggzy.com/jyxx/transaction_detail.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    def start_requests(self):
        data = '{"token":"","pn":0,"rn":20,"sdt":"","edt":"","wd":"","inc_wd":"","exc_wd":"","fields":"","cnum":"001","sort":"{\\"istop\\":\\"0\\",\\"ordernum\\":\\"0\\",\\"webdate\\":\\"0\\",\\"rowid\\":\\"0\\"}","ssort":"","cl":10000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"014","notEqual":null,"equalList":null,"notEqualList":["014001018","004002005","014001015","014005014","014008011"],"isLike":true,"likeType":2}],"time":[{"fieldName":"webdate","startTime":"%s 00:00:00","endTime":"%s 23:59:59"}],"highlights":"","statistics":null,"unionCondition":[],"accuracy":"","noParticiple":"1","searchRange":null,"noWd":true}' % (self.time_str, self.time_str)
        # data1 = '{"token":"","pn":0,"rn":20,"sdt":"","edt":"","wd":"","inc_wd":"","exc_wd":"","fields":"","cnum":"001","sort":"{\"istop\":\"0\",\"ordernum\":\"0\",\"webdate\":\"0\",\"rowid\":\"0\"}","ssort":"","cl":10000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"014","notEqual":null,"equalList":null,"notEqualList":["014001018","004002005","014001015","014005014","014008011"],"isLike":true,"likeType":2}],"time":[{"fieldName":"webdate","startTime":"{} 00:00:00","endTime":"{} 23:59:59"}],"highlights":"","statistics":null,"unionCondition":[],"accuracy":"","noParticiple":"1","searchRange":null,"noWd":true}: '
        # data = data1.format(time_str, time_str)
        data_ = {
            "token": "",
            "pn": 0,
            "rn": 20,
            "sdt": "",
            "edt": "",
            "wd": "",
            "inc_wd": "",
            "exc_wd": "",
            "fields": "",
            "cnum": "001",
            "sort": {"istop": "0", "ordernum ": "0", "webdate ": "0 ", "rowid ": "0"},
            "ssort": "",
            "cl": 10000,
            "terminal": "",
            "condition": [{
                "fieldName": "categorynum",
                "equal": "014",
                "notEqual": "null",
                "equalList": "null",
                "notEqualList": ["014001018", "004002005", "014001015", "014005014", "014008011"],
                "isLike": "true",
                "likeType": 2
            }],
            "time": [{
                "fieldName": "webdate",
                "startTime": f"{self.time_str} 00:00:00",
                "endTime": f"{self.time_str} 23:59:59"
            }],
            "highlights": "",
            "statistics": "null",
            "unionCondition": [],
            "accuracy": "",
            "noParticiple": "1",
            "searchRange": "null",
            "noWd": "true"
        }
        yield scrapy.FormRequest(
            url=self.start_url,
            headers=self.headers,
            cookies=self.cookies,
            body=data,
            callback=self.parse_1,
            method="POST",
            )

    def parse_1(self, response, **kwargs):
        date_josn = json.loads(response.text)
        categorys = date_josn["result"]["records"]
        if categorys:
            for ca in categorys:
                infoid = ca.get("infoid", "")
                bid_public_time = ca.get("pubinwebdate", "")
                bid_name = ca.get("titlenew", "title")
                bid_category = ca.get("categorytype")
                bid_info_type = ca.get("categorytype2")
                categorynum = ca.get("categorynum")
                infoc = ca.get("infoc", "")
                if (bid_category == "工程招投标" and bid_info_type != ("招标计划" or "保证金退还")) or (bid_category == "产权交易" and bid_info_type == "交易公告"):
                    link = f"https://www.cqggzy.com/xxhz/{categorynum[:6]}/{categorynum[:9]}/{categorynum}/{self.time_str.replace('-', '')}/{infoid}.html"
                elif bid_category == "工程招投标" and bid_info_type == "保证金退还":
                    items = BidScrapyProjectItem()
                    items["bid_id"] = get_md5(response.meta["infoid"])
                    items["bid_md5_url"] = ""
                    items["bid_name"] = response.meta["bid_name"]
                    items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                    items["bid_url"] = response.url
                    items["bid_category"] = bid_category
                    items["bid_info_type"] = bid_info_type
                    items["bid_source"] = "重庆市公共资源交易网"
                    items["bid_public_time"] = response.meta["bid_public_time"]
                    items["bid_html_con"] = ""
                    items["bid_content"] = ""
                    items["bid_city"] = "重庆市"
                    items["bid_county"] = infoc
                    items["website_name"] = "重庆市公共资源交易网"
                    items["website_url"] = "http://www.cqggzy.com/"
                    items["bid_province"] = "重庆市"
                    yield items
                    continue
                else:
                    link = f"https://www.cqggzy.com/xxhz/{categorynum[:6]}/{categorynum}/{self.time_str.replace('-', '')}/{infoid}.html"
                yield scrapy.Request(
                    url=link,
                    callback=self.parse,
                    meta={
                        "infoid": infoid,
                        "bid_public_time": bid_public_time,
                        "bid_name": bid_name,
                        "bid_info_type": bid_info_type,
                        "bid_category": bid_category,
                        "infoc": infoc,
                        "categorynum": categorynum,
                    },
                )
            self.page += 20
            time.sleep(3)
            # print(f"===========当前爬取{self.page/20}页===========")
            data = '{"token":"","pn":%s,"rn":20,"sdt":"","edt":"","wd":"","inc_wd":"","exc_wd":"","fields":"","cnum":"001","sort":"{\\"istop\\":\\"0\\",\\"ordernum\\":\\"0\\",\\"webdate\\":\\"0\\",\\"rowid\\":\\"0\\"}","ssort":"","cl":10000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"014","notEqual":null,"equalList":null,"notEqualList":["014001018","004002005","014001015","014005014","014008011"],"isLike":true,"likeType":2}],"time":[{"fieldName":"webdate","startTime":"%s 00:00:00","endTime":"%s 23:59:59"}],"highlights":"","statistics":null,"unionCondition":[],"accuracy":"","noParticiple":"1","searchRange":null,"noWd":true}' % (self.page, self.time_str, self.time_str)
            yield scrapy.FormRequest(
                url=self.start_url,
                headers=self.headers,
                cookies=self.cookies,
                body=data,
                callback=self.parse_1,
                method="POST",
                )
        else:
            pass
            # print("============爬取结束============")

    def parse(self, response, **kwargs):
        sel = Selector(response)
        res_t = pq(response.text)
        bid_source = "重庆市公共资源交易网"
        # bid_html_con = sel.xpath('//div[@class="epoint-article-content"]').extract()
        bid_html_con = res_t('div[class="epoint-article-content"]')
        bid_content = " ".join(sel.xpath('//div[@class="epoint-article-content"]//text()').extract()).strip()
        bid_category = response.meta["bid_category"]
        bid_info_type = response.meta["bid_info_type"]
        bid_county = response.meta["infoc"]
        if bid_category == "政府采购":
            items = GovernmentProcurementItem()
            items["po_id"] = get_md5(response.meta["infoid"])
            items["bo_name"] = response.meta["bid_name"]
            items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items["bid_url"] = response.url
            items["po_category"] = bid_category
            items["po_info_type"] = bid_info_type
            items["po_source"] = bid_source
            items["po_public_time"] = response.meta["bid_public_time"]
            items["po_html_con"] = str(bid_html_con).replace("'", '"')
            items["po_content"] = bid_content
            items["po_city"] = "重庆市"
            items["po_county"] = bid_county
            items["website_name"] = "重庆市公共资源交易网"
            items["website_url"] = "http://www.cqggzy.com/"
            items["po_province"] = "重庆市"
            yield items
        else:
            items = BidScrapyProjectItem()
            items["bid_id"] = get_md5(response.meta["infoid"])
            items["bid_md5_url"] = ""
            items["bid_name"] = response.meta["bid_name"]
            items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items["bid_url"] = response.url
            items["bid_category"] = bid_category
            items["bid_info_type"] = bid_info_type
            items["bid_source"] = bid_source
            items["bid_public_time"] = response.meta["bid_public_time"]
            items["bid_html_con"] = str(bid_html_con).replace("'", '"')
            items["bid_content"] = bid_content
            items["bid_city"] = "重庆市"
            items["bid_county"] = bid_county
            items["website_name"] = "重庆市公共资源交易网"
            items["website_url"] = "http://www.cqggzy.com/"
            items["bid_province"] = "重庆市"
            yield items
