# -*- coding: utf-8 -*-
"""
@desc: 甘肃省公共资源交易中心
@version: python3
@author: shenr
@time: 2023/07/11
"""
import base64
import json
import re
import time

import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class ExampleSpider(scrapy.Spider):
    name = "gansu_ggjy_2"
    start_urls = "https://pzxx.ggzyjy.gansu.gov.cn/f/newprovince/annogoods/getAnnoList"
    page = 0
    page_all = 1

    headers = {
        "authority": "pzxx.ggzyjy.gansu.gov.cn",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    cookies = {
        "JSESSIONID": "DE7FBD29F88A2633AA34DDB97D0DDC69",
        "yfx_c_g_u_id_10000005": "_ck23061409250510872479134241219",
        "pageNo": "0",
        "yfx_f_l_v_t_10000005": "f_t_1686705905085__r_t_1689038148161__v_t_1689038148161__r_c_4",
        "jeeplus.session.id": "a8f7839419434e9c8b34df8ff5a0eedc",
    }
    area_dic = {
        "620000": "省级平台（中心）",
        "620100": "兰州",
        "620200": "嘉峪关",
        "620300": "金昌",
        "620400": "白银",
        "620500": "天水",
        "620600": "威武",
        "620700": "张掖",
        "620800": "平凉",
        "620900": "酒泉",
        "621000": "庆阳",
        "621100": "定西",
        "621200": "陇南",
        "622900": "临夏",
        "623000": "甘南",
        "620001": "省级平台（兰州新区）",
    }
    projecttype_dic = {
        "A": "工程建设",
        "D": "政府采购",
        "B": "土地和矿业权",
    }
    zhongxin_dic = {
        "I": "重大项目",
        "A": "工程建设",
        "D": "政府采购",
        "C": "国有产权",
        "B": "土地和矿业权",
        "GD": "耕地占补平衡指标",
        "getAnnoList?type=purchase&annomentTitle=": "协议供货阳光采购",
        "getAnnoList?type=engineer&annomentTitle=": "限额以下工程建设",
        "getAnnoList?type=gover&annomentTitle=": "政府采购限额以下",
    }

    def start_requests(self):
        for area_k, area_v in self.area_dic.items():
            if area_k == "620000":
                for zhongxin_k, zhongxin_v in self.zhongxin_dic.items():
                    if zhongxin_k == "GD":
                        urls_1 = "https://pzxx.ggzyjy.gansu.gov.cn/f/plough/ploughList"
                    elif zhongxin_k == "B":
                        urls_1 = "https://pzxx.ggzyjy.gansu.gov.cn/f/newprovince/annogoodsmine/getLandAnnoList"
                    elif zhongxin_k in ("getAnnoList?type=purchase&annomentTitle=", "getAnnoList?type=engineer&annomentTitle=", "getAnnoList?type=gover&annomentTitle="):
                        urls_1 = f"https://pzxx.ggzyjy.gansu.gov.cn/f/purchase/purchaseAnnoment/{zhongxin_k}"
                        yield scrapy.Request(
                            url=urls_1,
                            headers=self.headers,
                            cookies=self.cookies,
                            dont_filter=True,
                            callback=self.parse_1,
                            meta={"pro_k": zhongxin_k, "pro_v": zhongxin_v, "area_k": area_k, "area_v": area_v},
                        )
                        continue
                    else:
                        urls_1 = self.start_urls
                    data = {
                        "pageNo": "0",
                        "pageSize": "",
                        "area": str(area_k),
                        "projecttype": zhongxin_k,
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
                        url=urls_1,
                        headers=self.headers,
                        cookies=self.cookies,
                        formdata=data,
                        dont_filter=True,
                        callback=self.parse_1,
                        method="POST",
                        meta={"pro_k": zhongxin_k, "pro_v": zhongxin_v, "area_k": area_k, "area_v": area_v},
                    )
            else:
                for pro_k, pro_v in self.projecttype_dic.items():
                    data = {
                        "pageNo": "0",
                        "pageSize": "",
                        "area": str(area_k),
                        "projecttype": pro_k,
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
                        url=self.start_urls,
                        headers=self.headers,
                        cookies=self.cookies,
                        formdata=data,
                        dont_filter=True,
                        callback=self.parse_1,
                        method="POST",
                        meta={"pro_k": pro_k, "pro_v": pro_v, "area_k": area_k, "area_v": area_v},
                    )

    def parse_1(self, response, **kwargs):
        meta = response.meta
        pq_res = pq(response.text)
        div_dq = pq_res('div[class="sTradingInformationSelectedBtoList"] dl')
        if not div_dq:
            div_dq = pq_res('dl')
        for each in div_dq.items():
            title = each("a").text()
            url_ = each("dd p a").attr("href")
            public_time = each("dd i").text()
            if url_ and "loadTenderprojectIndex" not in url_:
                "https://pzxx.ggzyjy.gansu.gov.cn/f/purchase/purchaseAnnoment/40/getAnnoDetail?annoId=40"
                "https://pzxx.ggzyjy.gansu.gov.cn/f/purchase/purchaseAnnoment/40/getAnnoDetail?annoId=40"
                detail_url = "https://pzxx.ggzyjy.gansu.gov.cn" + url_
                yield scrapy.Request(
                    url=detail_url,
                    headers=self.headers,
                    callback=self.parse_detail,
                    meta={
                        "type_": "1",
                        "pro_k": meta.get("pro_k"),
                        "pro_v": meta.get("pro_v"),
                        "area_k": meta.get("area_k"),
                        "area_v": meta.get("area_v"),
                        "detail_url": detail_url,
                        "title": title,
                        "public_time": public_time,
                    },
                )
            elif url_ and "loadTenderprojectIndex" in url_:
                detail_url = "https://pzxx.ggzyjy.gansu.gov.cn" + url_
                numm = re.findall('tenderproject/(.*?)/loadTenderprojectIndex', str(detail_url), re.S)[0]
                if meta.get("pro_k") == "getAnnoList?type=purchase&annomentTitle=":
                    url = "https://pzxx.ggzyjy.gansu.gov.cn/f/purchase/purchaseAnnoment/getPurchaseByProject"
                    annoId = re.findall('annoId=(.*?)', str(detail_url), re.S)[0]
                    data__ = {
                        "projectId": str(annoId),
                        "annoId": str(annoId),
                    }
                else:
                    url = "https://pzxx.ggzyjy.gansu.gov.cn/f/newprovince/tenderproject/flowListAndAuctionpage"
                    data__ = {
                        "bidpackages": "",
                        "tenderprojectid": str(numm),
                        "index": "0",
                    }
                yield scrapy.FormRequest(
                    url=url,
                    headers=self.headers,
                    callback=self.parse_detail,
                    formdata=data__,
                    meta={
                        "type_": "4",
                        "pro_k": meta.get("pro_k"),
                        "pro_v": meta.get("pro_v"),
                        "area_k": meta.get("area_k"),
                        "area_v": meta.get("area_v"),
                        "detail_url": detail_url,
                        "title": title,
                        "public_time": public_time,
                        "id_num": numm,
                    },
                )
            else:
                div_ = "openDetail"
                parame_ = re.findall(f"{div_}\('(.*?)'\)\"", str(each), re.S)
                if parame_:
                    parame = parame_[0].split("','")
                    bs_code = base64.b64encode(str(parame[0]).encode()).decode()
                    detail_url = f"https://pzxx.ggzyjy.gansu.gov.cn/f/cityTenderProject/{bs_code}/cityTenderprojectIndex?projectType={parame[1]}&table=&platformCode={parame[3]}&pubServicePlatCode={parame[4]}"
                    data_2 = {
                        "tradingCode": parame[0],
                        "platformCode": parame[3],
                        "pubServicePlatCode": parame[3],
                        "index": "0",
                        "projectType": meta.get("pro_k"),
                        "tableName": ""
                    }
                    yield scrapy.FormRequest(
                        url="https://pzxx.ggzyjy.gansu.gov.cn/f/cityTenderProject/flowpage",
                        headers=self.headers,
                        formdata=data_2,
                        callback=self.parse_detail,
                        meta={
                            "type_": "2",
                            "pro_k": meta.get("pro_k"),
                            "pro_v": meta.get("pro_v"),
                            "area_k": meta.get("area_k"),
                            "area_v": meta.get("area_v"),
                            "detail_url": detail_url,
                            "title": title,
                            "public_time": public_time,
                            "id_num": parame[0],
                        },
                    )
                else:
                    div_ = "loadTender"
                    parame_ = re.findall(f"{div_}\('(.*?)\)\"", str(each), re.S)
                    parame = parame_[0].split("','")
                    bs_code = base64.b64encode(str(parame[0]).encode()).decode()
                    detail_url = f"https://pzxx.ggzyjy.gansu.gov.cn/f/newprovince/tenderproject/{bs_code}/tenderprojectIndex?area={meta.get('area_k')}"
                    data_3 = {
                        "tradingCode": parame[0],
                        "platformCode": parame[3],
                        "pubServicePlatCode": parame[3],
                        "index": "0",
                        "projectType": meta.get("pro_k"),
                        "tableName": ""
                    }
                    yield scrapy.FormRequest(
                        url=detail_url,
                        headers=self.headers,
                        formdata=data_3,
                        callback=self.parse_detail,
                        meta={
                            "type_": "3",
                            "pro_k": meta.get("pro_k"),
                            "pro_v": meta.get("pro_v"),
                            "area_k": meta.get("area_k"),
                            "area_v": meta.get("area_v"),
                            "detail_url": detail_url,
                            "title": title,
                            "public_time": public_time,
                            "id_num": parame[0],
                        },
                    )

    def parse_detail(self, response, **kwargs):
        meta = response.meta
        res = pq(response.text)
        detail_url = meta.get("detail_url")
        id_ = get_md5(detail_url)
        url_ = meta.get("detail_url")
        city_ = meta.get("area_v")
        info_type_ = meta.get("pro_v")
        name_ = meta.get("title")
        public_time = meta.get("public_time")
        if info_type_ == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = id_
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = url_
            # item["bid_md5_url"] = meta.get("md5_url")
            item["po_province"] = "甘肃省"
            item["po_city"] = city_
            item["po_county"] = ""
            item["po_category"] = ""
            item["po_info_type"] = info_type_
            item["po_source"] = "甘肃省公共资源交易中心"
            item["bo_name"] = name_
            item["po_public_time"] = public_time
            item["po_html_con"] = str(res).replace("'", '"')
            item["po_content"] = res.text()
            item["description"] = ""
            item["website_name"] = "甘肃省公共资源交易中心"
            item["website_url"] = "https://ggzyjy.gansu.gov.cn/ggzyjy/index.shtml"
            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = id_
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = url_
            item["bid_md5_url"] = ""
            item["bid_province"] = "甘肃省"
            item["bid_city"] = city_
            item["bid_county"] = ""
            item["bid_category"] = ""
            item["bid_info_type"] = info_type_
            item["bid_source"] = "甘肃省公共资源交易中心"
            item["bid_name"] = name_
            item["bid_public_time"] = public_time
            item["bid_html_con"] = str(res).replace("'", '"')
            item["bid_content"] = res.text()
            item["description"] = ""
            item["website_name"] = "甘肃省公共资源交易中心"
            item["website_url"] = "https://ggzyjy.gansu.gov.cn/ggzyjy/index.shtml"
            yield item


