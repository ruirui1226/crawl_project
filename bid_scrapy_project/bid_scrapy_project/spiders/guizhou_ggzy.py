# -*- coding: utf-8 -*-
"""
@desc: 贵州省公共资源交易网
@version: python3
@author: xm
@time: 2023/06/15
"""
import json
import time

import scrapy
from bs4 import BeautifulSoup
from lxml import html
from scrapy.http import JsonRequest

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class GuizhouGgzySpider(scrapy.Spider):
    custom_settings = {"COOKIES_ENABLED": True}
    name = "guizhou_ggzy"

    # allowed_domains = ['ggzy.guizhou.gov.cn']
    # start_urls = ['http://ggzy.guizhou.gov.cn/']
    def __init__(self):
        self.apiUrl = "https://ggzy.guizhou.gov.cn/tradeInfo/es/list"
        self.citys = ["贵州省", "贵阳市", "遵义市", "六盘水市", "安顺市", "毕节市", "铜仁市", "黔东南州", "黔南州", "黔西南州"]
        self.categorys = {
            "政府采购": {"id": 5904543, "公告公示": ["采购需求公示", "变更公告（澄清与答疑）", "采购公告", "交易结果公示", "交易证明书", "其他公告", "合同公示"]},
            "工程建设": {"id": 5904475, "公告公示": ["交易公告", "变更公告（澄清与答疑）", "中标候选人公示", "交易结果公示", "交易证明书", "其他公告", "合同公示"]},
            "土地及矿业权": {"id": 5904476},
            "产权交易": {"id": 5904477, "公告公示": ["交易公告", "成交公示", "变更公告（澄清与答疑）", "其他公告", "交易证明书"]},
            "其他": {"id": 5904479, "公告公示": ["交易公告", "交易结果公示"]},
        }
        ##不同的两个
        self.othUrl = "https://ggzy.guizhou.gov.cn/irs/front/list"
        self.params = {
            "医用耗材": {
                "pageNo": 1,
                "pageSize": 20,
                "tenantId": 320,
                "tableName": "t_179d11f03ab",
                "sorts": [{"sortField": "save_time", "sortOrder": "DESC"}],
                "customFilter": {
                    "operator": "or",
                    "properties": [{"property": "f_202163485346", "operator": "eq", "value": "5906829"}],
                },
            },
            "药品及二类疫苗": {
                "pageNo": 1,
                "pageSize": 20,
                "tenantId": 320,
                "tableName": "t_179d11f03ab",
                "sorts": [{"sortField": "save_time", "sortOrder": "DESC"}],
                "customFilter": {
                    "operator": "or",
                    "properties": [{"property": "f_202163485346", "operator": "eq", "value": "5906830"}],
                },
            },
        }
        self.bid_province = "贵州省"
        self.website_name = "贵州省公共资源交易网"
        self.website_url = "https://ggzy.guizhou.gov.cn/"
        self.headers = {
            # "Content-Length": "236",
            "Content-Type": "application/json;charset=UTF-8",
            "Host": "ggzy.guizhou.gov.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
            # 'Cookie': 'SESSION=YTE3ZDcwYzMtZTNhMi00OGQ0LTk2NDMtMDllNWFmODYxZTlm'
        }
        self.cookies = {
            # SESSION=MDljNDNjMzMtMjRhMC00NGI2LWIxNGEtOTAwMjc5MjQ2YWI0; _trs_uv=liwt88ey_4151_ibtm; JSESSIONID=B01CAF400C90948C676BDC9AB2A91E04; _trs_ua_s_1=lj27j7do_4151_dcjh; gboatsessionid=c21747fd53584684b029eaaa2995ce67
            "SESSION": "MDljNDNjMzMtMjRhMC00NGI2LWIxNGEtOTAwMjc5MjQ2YWI0",
            "_trs_uv": "liwt88ey_4151_ibtm",
            "JSESSIONID": "B01CAF400C90948C676BDC9AB2A91E04",
            "_trs_ua_s_1": "lj27j7do_4151_dcjh",
            "gboatsessionid": "c21747fd53584684b029eaaa2995ce67",
        }

    def start_requests(self):
        """
        两个的处理  2023.6.15记录: 第二页的第一条时间为2023.6.13
        """
        for i, v in self.categorys.items():
            category = i  ##大分类
            categoryid = v.get("id")
            print("++++++++", category)
            for city in self.citys:
                print("省：：：", city)
                if "市" in city or "州" in city:
                    city_1 = city
                for page in range(1, 2):
                    ##{"channelId":"5904479","pageNum":1,"pageSize":20,"announcement":"交易公告"}
                    gonggao = v.get("公告公示", None)
                    if not gonggao:
                        print("**************", category)
                        param = {
                            "channelId": "{}".format(categoryid),
                            "pageNum": page,
                            "pageSize": 20,
                            "docSourceName": "{}".format(city),
                        }
                        items = {"bid_city": city_1, "bid_category": category}
                        yield JsonRequest(
                            self.apiUrl, data=param, callback=self.parse, meta={"items": items}, dont_filter=True
                        )
                    else:
                        for info_type in gonggao:
                            print("**************", category)
                            param = {
                                "channelId": "{}".format(categoryid),
                                "pageNum": page,
                                "pageSize": 20,
                                "docSourceName": "{}".format(city),
                                "announcement": "{}".format(info_type),
                            }
                            ##{"channelId":"5904479","pageNum":1,"pageSize":20}
                            yield JsonRequest(
                                self.apiUrl,
                                data=param,
                                callback=self.parse,
                                meta={
                                    "items": {"bid_city": city_1, "bid_category": category, "bid_info_type": info_type}
                                },
                                dont_filter=True,
                            )
                break
        for leixing, pa in self.params.items():
            for page_p in range(1, 3):
                yaopinitems = {"bid_category": "药械采购", "bid_info_type": leixing}
                pa["pageNo"] = page_p
                yield JsonRequest(
                    self.othUrl,
                    data=pa,
                    callback=self.othListParse,
                    meta={"items": yaopinitems},
                    headers=self.headers,
                    cookies=self.cookies,
                    dont_filter=True,
                )

    def othListParse(self, response):
        items_info = response.meta.get("items")
        jsonDict = json.loads(response.text)
        datas = jsonDict.get("data")
        if not datas:
            return
        list_content = datas.get("list")
        for li in list_content:
            doc_pub_url = li.get("doc_pub_url")
            title = li.get("f_20216323178")  ##title
            save_time = li.get("save_time")
            source = li.get("f_202163340436")  ##来源
            items = {}
            items.update(items_info)
            items["bid_name"] = title
            items["bid_public_time"] = save_time
            items["bid_source"] = source
            yield scrapy.Request(doc_pub_url, callback=self.getContentParse, meta={"items": items})

    def parse(self, response):
        items = response.meta.get("items")
        jsonDcit = json.loads(response.text)
        jsonList = jsonDcit.get("list")
        if not jsonList:
            return
        for json_li in jsonList:
            docSourceName = json_li.get("docSourceName")  ##信息来源
            docTitle = json_li.get("docTitle")  ##标题
            mid = json_li.get("id")  ## id
            docRelTime = json_li.get("docRelTime")  ##时间戳 处理一下 13位的
            pubdate = self.custom_time(int(str(docRelTime)[:10]), "%Y-%m-%d %H:%M:%S")
            href = json_li.get("apiUrl")
            items_info = {}
            items_info.update(items)
            items_info["bid_source"] = docSourceName
            items_info["bid_name"] = docTitle
            items_info["bid_public_time"] = pubdate
            yield scrapy.Request(href, callback=self.getContentParse, meta={"items": items_info})

    def getContentParse(self, response):
        """
        详情页信息
        #"""
        contents = response.css("div.view_con *::text").extract()

        items_info = response.meta.get("items")
        if not contents:
            contents = response.css("#Zoom *::text").extract()
            content_html = str(response.css("#Zoom").get()).replace("'", "’").strip()
            content = "".join(x.strip() for x in contents)
        else:
            value = remove_node(str(response.css("div.view_con").get()), ["style"])
            content = value.text
            content_html = str(response.css("div.view_con").get()).strip()
        if "政府采购" in items_info["bid_category"]:
            items_cg = GovernmentProcurementItem()
            items_cg["po_province"] = self.bid_province
            items_cg["website_name"] = self.website_name
            items_cg["website_url"] = self.website_url
            items_cg["po_source"] = items_info.get("bid_source", None)
            items_cg["bo_name"] = items_info.get("bid_name", None)
            items_cg["po_public_time"] = items_info.get("bid_public_time", None)
            items_cg["po_category"] = items_info.get("bid_category", None)
            items_cg["po_info_type"] = items_info.get("bid_info_type", None)
            items_cg["po_city"] = items_info.get("bid_city", None)
            items_cg["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items_cg["bid_url"] = response.request.url
            items_cg["po_id"] = get_md5(response.request.url)
            items_cg["po_html_con"] = content_html
            items_cg["po_content"] = content.strip()
            yield items_cg
        else:
            items = BidScrapyProjectItem()
            items["bid_province"] = self.bid_province
            items["website_name"] = self.website_name
            items["website_url"] = self.website_url
            items.update(items_info)
            items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items["bid_url"] = response.request.url
            items["bid_id"] = get_md5(response.request.url)
            items["bid_html_con"] = content_html
            items["bid_content"] = content.strip()
            yield items

    def custom_time(self, timestamp, timeTypr):
        """
        时间戳转时间
        """
        # 转换成localtimews
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime(timeTypr, time_local)
        return dt
