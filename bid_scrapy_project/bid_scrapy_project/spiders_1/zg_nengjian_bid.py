#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/17 9:21
# @Author  :
# @File    : zg_nengjian_bid.py
# @Description : 中国能建电子采购平台
import datetime
import json
import time

import scrapy
from scrapy.http import JsonRequest

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


class ZgNengjianBidSpider(scrapy.Spider):
    name = "zg_nengjian_bid"

    def __init__(self):
        self.apiUrl = "https://ec.ceec.net.cn/ajaxpro/CeecBidWeb.HomeInfo.ProjectList,CeecBidWeb.ashx"
        self.contentApiUrl = "https://ec.ceec.net.cn/ajaxpro/CeecBidWeb.HomeInfo.ZiGeYSGG_Details,CeecBidWeb.ashx"
        self.params = {"_bigtype_base64": "QwBHAFkARwA=", "_smalltype_base64": "", "_pageIndex": 1, "_pageSize": 20}
        self.infotypes = {
            "采购预告": "QwBHAFkARwA=",
            "资格预审公告": "WgBHAFkAUwBHAEcA",
            "招标公告": "WgBCAEcARwA=",
            "采购公告": "QwBHAEcARwA=",
            "候选人公示": "SABYAFIARwBTAA==",
            "中标公示": "WgBCAEcAUwA=",
            "中选公示": "WgBYAEcAUwA=",
            # 弃
            # "采购动态": "QwBHAEQAVAA=",
            # "已完项目": "WQBXAFgATQA=",
        }
        self.domains = {
            "资格预审公告": "ZiGeYSGG_Details.aspx?zbxmbh={}",
            "采购预告": "YuGao_Detail.aspx?threadID={}",
            "招标公告": "ZhaoBiaoGG_Details.aspx?zbxmbh={}",
            "采购公告": "ProjectDetail.aspx?&bigtype=QwBHAEcARwA=&threadID={}",
            "候选人公示": "winDidDetails.aspx?bigtype=SABYAFIARwBTAA==&threadID={}",
            "中标公示": "winDidDetails.aspx?bigtype=WgBCAEcAUwA=&threadID={}",
            "中选公示": "winDidDetails.aspx?bigtype=WgBYAEcAUwA=&threadID={}",
            # "采购动态": "ProjectDetail.aspx?&bigtype=QwBHAEQAVAA=&threadID={}",
            # "已完项目": "ProjectDetailFinish.aspx?threadID={}",
        }
        self.headers = {
            "Content-Type": "text/plain; charset=UTF-8",
            "Host": "ec.ceec.net.cn",
            "Origin": "https://ec.ceec.net.cn",
            "Referer": "https://ec.ceec.net.cn/HomeInfo/ProjectList.aspx?InfoLevel=MQA=&bigType=WgBHAFkAUwBHAEcA",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
            # "X-AjaxPro-Method": "getdata",
        }
        self.website_name = "中国能建电子采购平台"
        self.webUrl = "https://ec.ceec.net.cn"
        self.types = {
            "货物采购": "aAB3AA==",
            "工程分包": "ZwBjAA==",
            "服务采购": "ZgB3AA==",
        }

    def start_requests(self):
        for infotypename, infotypeid in self.infotypes.items():
            if "候选人公示" in infotypename or "中标公示" in infotypename or "中选公示" in infotypename:
                for tyname, tyid in self.types.items():
                    self.params["_bigtype_base64"] = infotypeid
                    self.params["_smalltype_base64"] = tyid
                    items = {"info_type": infotypename, "category": tyname}
                    self.headers["X-AjaxPro-Method"] = "getdata"
                    yield JsonRequest(
                        url=self.apiUrl,
                        data=self.params,
                        dont_filter=True,
                        callback=self.parse,
                        meta={"items": items},
                        headers=self.headers,
                    )
            else:
                self.params["_bigtype_base64"] = infotypeid
                items = {"info_type": infotypename}
                self.headers["X-AjaxPro-Method"] = "getdata"
                yield JsonRequest(
                    url=self.apiUrl,
                    data=self.params,
                    dont_filter=True,
                    callback=self.parse,
                    meta={"items": items},
                    headers=self.headers,
                )

    def parse(self, response, **kwargs):
        jsonStr = response.text
        if not jsonStr:
            return
        jsonStr = jsonStr[: jsonStr.rindex(";")]
        jsondict = json.loads(json.loads(jsonStr))
        maindata = jsondict.get("maindata")[0]
        if not maindata:
            return
        for data in maindata:
            CaiGouLB = data.get("CaiGouLB")  ##大类别
            if not CaiGouLB:
                CaiGouLB = data.get('zhaoBiaoLB')
            title = data.get("GongGaoBT")
            if not title:
                title = data.get("ZhaoBiaoXMMC")
            if not title:
                title = data.get('zbxmmc')
            # content = data.get("YuGaoZW")
            pubdate = data.get("YuGaoFBSJ")
            if not pubdate:
                pubdate = data.get("GongGaoFBSJ")
            if not pubdate:
                pubdate = data.get("faBiaoKSSJ")
            if not pubdate:
                pubdate = data.get("fbsj")
            timeArray = time.strptime(pubdate, "%Y/%m/%d %H:%M:%S")
            pubdate = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            # 判断不是一天内 就退出
            timeNow = datetime.datetime.now()  ###现在的时间
            pdate = datetime.datetime.strptime(pubdate, "%Y-%m-%d %H:%M:%S")
            # if abs((timeNow - pdate).days) > 1:  # 判断时间间隔天数
            #     continue
            # 联系人
            LianXiR = data.get("LianXiR")
            # 联系电话
            LianXiDH = data.get("LianXiDH")

            sys_id = data.get("sys_id")
            if not sys_id:
                #需要获取详情页id
                items = {"title": title, "pubdate": pubdate, "category": CaiGouLB}
                items.update(response.meta["items"])
                # 此id不可直接拼接到详情页
                # sys_id = data.get("sys_epsid")
                sys_id = data.get("ZhaoBiaoXMBH")
                self.headers["X-AjaxPro-Method"] = "encode"
                yield JsonRequest(
                    self.apiUrl,
                    data={"s": sys_id},
                    headers=self.headers,
                    callback=self.getContent_id,
                    meta={"items": items},
                )
            else:
                #详情页id可直接用
                domain = self.domains[response.meta["items"]["info_type"]]
                href = "https://ec.ceec.net.cn/HomeInfo/{}".format(domain.format(sys_id))
                items = {"title": title, "pubdate": pubdate, "href": href}
                if CaiGouLB:
                    items["category"] = CaiGouLB
                items.update(response.meta["items"])
                info_type = response.meta["items"]["info_type"]
                if "预告" in info_type:
                    self.headers["X-AjaxPro-Method"] = "GetCaiGouYG"
                elif "采购公告" in info_type or "采购动态" in info_type:
                    self.headers["X-AjaxPro-Method"] = "GetCaiGouGG"
                if "候选人公示" in info_type or "中标公示" in info_type or "中选公示" in info_type or "已完项目" in info_type:
                    ##静态
                    yield scrapy.Request(url=href, callback=self.staticHref, meta={"items": items})
                else:
                    yield JsonRequest(
                        "https://ec.ceec.net.cn/ajaxpro/CeecBidWeb.HomeInfo.{},CeecBidWeb.ashx".format(
                            domain[: domain.index(r".aspx?")]
                        ),
                        callback=self.contentparse,
                        data={"vthreadID": sys_id},
                        headers=self.headers,
                        meta={"items": items},
                    )

    def getContent_id(self, response):
        '''
        获取部分详情页的id
        '''
        hid = response.text
        hid = hid[: hid.rindex(";")]
        hid = hid.strip('"')
        domain = self.domains[response.meta["items"]["info_type"]]
        href = "https://ec.ceec.net.cn/HomeInfo/{}".format(domain.format(hid))
        items = {"href": href}
        items.update(response.meta["items"])
        self.headers["X-AjaxPro-Method"] = "GetZhaoBiaoGG"
        yield JsonRequest(
            self.contentApiUrl,
            callback=self.contentparse,
            data={"_vProjectCode_EN": hid},
            headers=self.headers,
            meta={"items": items},
        )

    def contentparse(self, response):
        """
        详情页动态处理
        """
        item_info = response.meta["items"]
        content_json_str = response.text
        content_json = content_json_str[: content_json_str.rindex(";")]
        content_jsonDict = json.loads(json.loads(content_json))
        if isinstance(content_jsonDict, list):
            gongGaoZW = content_jsonDict[0].get("YuGaoZW")
            if not gongGaoZW:
                gongGaoZW = content_jsonDict[0].get("biaoDiWSM")
        else:
            ZhaoBiaoGG = content_jsonDict.get("ZhaoBiaoGG")
            if ZhaoBiaoGG:
                gongGaoZW = ZhaoBiaoGG[0].get("GongGaoZW")
        ## str = str.replace(RegExp("\r", "gi"), "<br/>").replace(RegExp("\n", "gi"), "<br/>").replace(RegExp("\t", "gi"), "")
        content_html = gongGaoZW.replace("\r", "<br/>").replace("\n", "<br/>").replace("\t", "")
        items = {
            "bid_id": get_md5(item_info.get("href")),
            "bid_url": item_info.get("href"),
            "bid_category": item_info["category"],
            "bid_info_type": item_info["info_type"],
            "bid_public_time": item_info["pubdate"],
            "bid_name": item_info.get("title"),
            "bid_html_con": content_html,
            "bid_content": gongGaoZW,
            "website_name": self.website_name,
            "website_url": self.webUrl,
            "bid_json_data": json.loads(content_json),
            "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }
        item_bid = BidScrapyProjectItem()
        item_bid.update(items)
        # print(items)
        yield item_bid

    def staticHref(self, response):
        """
        详情页静态处理
        """
        item_info = response.meta["items"]
        content_html = response.css("pre").get()
        contents = response.css("pre *::text").extract()
        content = "".join(x.strip() for x in contents)
        items = {
            "bid_id": get_md5(item_info.get("href")),
            "bid_url": item_info.get("href"),
            "bid_category": item_info["category"],
            "bid_info_type": item_info["info_type"],
            "bid_public_time": item_info["pubdate"],
            "bid_name": item_info.get("title"),
            "bid_html_con": content_html,
            "bid_content": content,
            "website_name": self.website_name,
            "website_url": self.webUrl,
            "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }
        item_bid = BidScrapyProjectItem()
        item_bid.update(items)
        # print(items)
        yield item_bid