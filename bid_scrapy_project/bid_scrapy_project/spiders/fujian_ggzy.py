# -*- coding: utf-8 -*-
"""
@desc: 福建省公共资源交易电子公共服务平台
@version: python3
@author: xm
@time: 2023/06/27
"""
import hashlib
import json
import time

import redis
import scrapy
from Crypto.Cipher import AES
from scrapy.http import JsonRequest
from bs4 import BeautifulSoup
from scrapy.utils.project import get_project_settings

from bid_scrapy_project.common.aesDecode import AEScryptor
from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.common.my_filter import Redis_Fingerprint
from bid_scrapy_project.items import BidScrapyProjectItem


class FujianGgzySpider(scrapy.Spider):
    """
    详情获取 有ts 时间戳
    """

    name = "fujian_ggzy"

    # allowed_domains = ['ggzyfw.fujian.gov.cn']
    # start_urls = ['http://ggzyfw.fujian.gov.cn/']
    def __init__(self):
        self.webName = "福建省公共资源交易电子公共服务平台"
        self.webUrl = "http://ggzyfw.fujian.gov.cn/"
        self.citys = [
            {"label": "省本级", "value": "350000", "name": "省本级"},
            {"label": "福州市", "value": "350100", "name": "福州市"},
            {"label": "平潭综合实验区", "value": "350128", "name": "平潭综合实验区"},
            {"label": "厦门市", "value": "350200", "name": "厦门市"},
            {"label": "莆田市", "value": "350300", "name": "莆田市"},
            {"label": "三明市", "value": "350400", "name": "三明市"},
            {"label": "泉州市", "value": "350500", "name": "泉州市"},
            {"label": "漳州市", "value": "350600", "name": "漳州市"},
            {"label": "南平市", "value": "350700", "name": "南平市"},
            {"label": "龙岩市", "value": "350800", "name": "龙岩市"},
            {"label": "宁德市", "value": "350900", "name": "宁德市"},
        ]
        # 业务类型列表
        self.businessTypes = {
            "工程建设": {
                "value": "GCJS",
                "GGTYPE": [
                    {"label": "招标公告", "value": "1", "name": "招标公告"},
                    {"label": "变更公告", "value": "2,3,7", "name": "变更公告"},
                    {"label": "中标候选人公示", "value": "4", "name": "中标候选人公示"},
                    {"label": "中标结果公告", "value": "5", "name": "中标结果公告"},
                    {"label": "资格预审公告", "value": "6", "name": "资格预审公告"},
                ],
                "children": [
                    # {"value": "A01", "label": "房屋建筑", "children": []},
                    # {"value": "A02", "label": "市政", "children": []},
                    # {"value": "A98", "label": "园林绿化", "children": []},
                    # {"value": "A03", "label": "公路", "children": []},
                    # {"value": "A04", "label": "铁路", "children": []},
                    # {"value": "A06", "label": "水运", "children": []},
                    # {"value": "A07", "label": "水利", "children": []},
                    # {"value": "A14", "label": "工业制造", "children": []},
                    # {"value": "A97", "label": "海洋渔港", "children": []},
                    # {"value": "A13", "label": "信息网络", "children": []},
                    # {"value": "A08", "label": "能源", "children": []},
                    # {"value": "A09", "label": "邮电通信", "children": []},
                    # {"value": "A99", "label": "其他", "children": []},
                ],
            },
            # "政府采购": {
            #     "value": "ZFCG",
            #     "GGTYPE": [
            #         {"label": "采购/资格预审公告", "value": "1", "name": "采购/资格预审公告"},
            #         {"label": "中标公告", "value": "2", "name": "中标公告"},
            #         {"label": "采购合同", "value": "3", "name": "采购合同"},
            #         {"label": "更正事项", "value": "4", "name": "更正事项"},
            #     ],
            #     "children": [
            #         {"value": "D01", "label": "货物类（含药品集中采购）", "children": []},
            #         {"value": "D02", "label": "工程类", "children": []},
            #         {"value": "D03", "label": "服务类", "children": []},
            #     ],
            # },
            # "土地使用权": {
            #     "value": "TDSYQ",
            #     "GGTYPE": [
            #         {"label": "出让公示", "value": "1", "name": "出让公示"},
            #         {"label": "成交宗地", "value": "2", "name": "成交宗地"},
            #     ],
            #     "children": [{"value": "B01", "label": "土地使用权出让", "children": []}],
            # },
            # "矿业权": {
            #     "value": "KYQ",
            #     "GGTYPE": [
            #         {"label": "出让公告", "value": "1", "name": "出让公告"},
            #         {"label": "出让结果", "value": "2", "name": "出让结果"},
            #     ],
            #     "children": [{"value": "B03", "label": "采矿权出让", "children": []}],
            # },
            # "国有产权": {
            #     "value": "GYCQ",
            #     "GGTYPE": [
            #         {"label": "挂牌披露", "value": "1", "name": "挂牌披露"},
            #         {"label": "交易结果", "value": "2", "name": "交易结果"},
            #     ],
            #     "children": [
            #         {"value": "C01", "label": "行政事业单位产权交易", "children": []},
            #         {"value": "C02", "label": "国有及国有控股企业产权交易", "children": []},
            #         {"value": "C03", "label": "金融企业国有资产转让交易", "children": []},
            #     ],
            # },
            # "其他交易": {
            #     "value": "QT",
            #     "GGTYPE": [
            #         {"label": "交易公告", "value": "1", "name": "交易公告"},
            #         {"label": "成交公示", "value": "2", "name": "成交公示"},
            #     ],
            #     "children": [],
            # },
        }
        ##项目类型
        # self.proType = {"依法必须招投标项目": "1", "其他招投标项目": "2"}
        self.apiUrl = "https://ggzyfw.fujian.gov.cn/FwPortalApi/Trade/TradeInfo"
        self.salt = "3637CB36B2E54A72A7002978D0506CDF"
        self.province = "福建省"
        self.param = {
            "pageNo": 1,  # 页面
            "pageSize": 20,  # 每页的条数
            "total": 0,  # 一共数据多少  测试硬性么
            "AREACODE": "",  # 省 市 id
            "M_PROJECT_TYPE": "",  # 项目类型
            "KIND": "",  # 业务类型
            "GGTYPE": "",  ##信息类型
            "PROTYPE": "",  ##行业类型
            "timeType": "1",
            "BeginTime": None,  # 开始时间
            "EndTime": "2023-06-27 23:59:59",  # 结束时间
            "createTime": [],
            "ts": None,
        }
        self.headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
            # "portal-sign": "e9ffd984986008299fdeeda6841e84c8",
        }
        self.key = b"BE45D593014E4A4EB4449737660876CE"
        self.iv = b"A8909931867B0425"
        self.content_api = "https://ggzyfw.fujian.gov.cn/FwPortalApi/Trade/TradeInfoContent"
        self.aes = AEScryptor(
            self.key, AES.MODE_CBC, self.iv, paddingMode="PKCS7Padding", characterSet="utf-8", isHeskey_iv=True
        )
        self.redis_u = Redis_Fingerprint()

    def start_requests(self):
        # 获取一下当前的时间 和当前的年
        # 当前时间
        nows = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
        # 循环省市
        for city in self.citys:
            cityId = city.get("value")
            cityName = city.get("label")
            bid_city = None
            if not "省本级" in cityName:
                bid_city = cityName
            # 循环业务类型
            for businessname, business in self.businessTypes.items():
                kind = business.get("value")
                # 循环信息类型
                # 判断是否有信息类型
                info_type = business.get("GGTYPE")
                for info in info_type:
                    infoName = info.get("label")
                    infoId = info.get("value")
                    children = business.get("children")
                    if children:
                        for child in children:
                            param = {
                                "pageNo": 1,  # 页面
                                "pageSize": 20,  # 每页的条数
                                "total": 0,  # 一共数据多少  测试硬性么
                                "timeType": "1",
                                "createTime": [],
                                "M_PROJECT_TYPE": "",
                            }
                            childName = child.get("label")
                            childId = child.get("value")
                            timeNow = int((time.time()) * 1000)
                            param["AREACODE"] = cityId  # 省 市 id
                            param["KIND"] = kind  # 业务类型
                            param["GGTYPE"] = infoId  ##信息类型
                            param["PROTYPE"] = childId  ##行业类型
                            param["BeginTime"] = "{} 00:00:00".format(nows)
                            param["EndTime"] = "{} 23:59:59".format(nows)
                            param["ts"] = timeNow
                            # 3637CB36B2E54A72A7002978D0506CDFAREACODE350000BeginTime2022-12-28 00:00:00createTime[]EndTime2023-06-28 23:59:59GGTYPE2,3,7KINDGCJSpageNo1pageSize20PROTYPEA01timeType6total1263ts1687915162644
                            jiamiStr = "{salt}AREACODE{AREACODE}BeginTime{BeginTime}createTime[]EndTime{EndTime}GGTYPE{GGTYPE}KIND{KIND}pageNo1pageSize40PROTYPE{PROTYPE}timeType6total0ts{ts}".format(
                                salt=self.salt,
                                BeginTime="{} 00:00:00".format(nows),
                                EndTime="{} 23:59:59".format(nows),
                                GGTYPE=infoId,
                                KIND=kind,
                                PROTYPE=childId,
                                ts=timeNow,
                                AREACODE=cityId,
                            )
                            self.headers["portal-sign"] = self.get_md5(jiamiStr)
                            items_info = {
                                "bid_city": bid_city,
                                "bid_category": businessname,
                                "bid_info_type": infoName,
                            }
                            yield JsonRequest(
                                self.apiUrl,
                                data=param,
                                callback=self.parse,
                                headers=self.headers,
                                meta={"items": items_info},
                                dont_filter=True,
                            )
                    else:
                        param = {
                            "pageNo": 1,  # 页面
                            "pageSize": 20,  # 每页的条数
                            "total": 0,  # 一共数据多少  测试硬性么
                            "timeType": "1",
                            "createTime": [],
                            "M_PROJECT_TYPE": "",
                            # "PROTYPE": "",
                        }
                        ##{"pageNo":1,"pageSize":20,"total":3673,"AREACODE":"","M_PROJECT_TYPE":"","KIND":"GCJS","GGTYPE":"1","PROTYPE":"","timeType":"1","BeginTime":"2023-07-13 00:00:00","EndTime":"2023-07-13 10:22:37","createTime":[],"ts":1689214957508}
                        timeNow = int((time.time()) * 1000)
                        param["AREACODE"] = cityId  # 省 市 id
                        param["KIND"] = kind  # 业务类型
                        param["GGTYPE"] = infoId  ##信息类型
                        param["BeginTime"] = "{} 00:00:00".format(nows)
                        param["EndTime"] = "{} 23:59:59".format(nows)
                        param["ts"] = timeNow
                        # '3637CB36B2E54A72A7002978D0506CDFAREACODE350100BeginTime2023-07-13 00:00:00createTime[]EndTime2023-07-13 10:22:37GGTYPE1KINDGCJSpageNo1pageSize20timeType1total3ts1689215295732'
                        jiamiStr = "{salt}AREACODE{AREACODE}BeginTime{BeginTime}createTime[]EndTime{EndTime}GGTYPE{GGTYPE}KIND{KIND}pageNo1pageSize20timeType1total0ts{ts}".format(
                            salt=self.salt,
                            BeginTime="{} 00:00:00".format(nows),
                            EndTime="{} 23:59:59".format(nows),
                            GGTYPE=infoId,
                            KIND=kind,
                            ts=timeNow,
                            AREACODE=cityId,
                        )
                        self.headers["portal-sign"] = self.get_md5(jiamiStr)
                        items_info = {
                            "bid_city": bid_city,
                            "bid_category": businessname,
                            "bid_info_type": infoName,
                        }
                        yield JsonRequest(
                            self.apiUrl,
                            data=param,
                            callback=self.parse,
                            headers=self.headers,
                            meta={"items": items_info},
                            dont_filter=True,
                        )
        # 医疗用品无法用省份
        # "医疗药品": {"value": "YLYP", "GGTYPE": [], "children": []},
        param_yp = {
            "pageNo": 1,
            "pageSize": 20,
            # "total": 3517,
            "total": 0,
            "AREACODE": "",
            "M_PROJECT_TYPE": "",
            "KIND": "YLYP",
            "GGTYPE": "",
            "PROTYPE": "",
            "timeType": "1",
            "createTime": [],
            "DIRCODE": "",
        }
        timeNow = int((time.time()) * 1000)
        param_yp["BeginTime"] = "{} 00:00:00".format(nows)
        param_yp["EndTime"] = "{} 23:59:59".format(nows)
        param_yp["ts"] = timeNow
        # param_yp["ts"] = "1687857044088"
        # print(json.dumps(param_yp, ensure_ascii=False))
        # 3637CB36B2E54A72A7002978D0506CDFBeginTime2022-12-27 00:00:00createTime[]EndTime2023-06-27 23:59:59KINDYLYPpageNo1pageSize40timeType6total3517ts1687854359292
        jiamiStr = "{salt}BeginTime{BeginTime}createTime[]EndTime{EndTime}KIND{KIND}pageNo1pageSize40timeType6total0ts{ts}".format(
            salt=self.salt,
            BeginTime="{} 00:00:00".format(nows),
            EndTime="{} 23:59:59".format(nows),
            KIND="YLYP",
            ts=timeNow,
        )
        items_yp = {"bid_category": "医疗药品"}
        self.headers["portal-sign"] = self.get_md5(jiamiStr)
        # yield JsonRequest(
        #     self.apiUrl,
        #     data=param_yp,
        #     callback=self.parse,
        #     headers=self.headers,
        #     meta={"items": items_yp},
        # )

    def parse(self, response):
        items = response.meta["items"]
        jsonDict = json.loads(response.text)
        if "未知错误" in jsonDict.get("Msg"):
            return
        dataInfo = jsonDict.get("Data")

        dataStr = str(self.aes.decryptFromBase64(dataInfo).data, "utf-8")
        dataDict = json.loads(dataStr)
        if not dataDict.get("Table"):
            return
        tables = dataDict.get("Table")
        for table in tables:
            title = table.get("NAME")
            cid = table.get("M_ID")
            type = table.get("KIND")
            GGTYPE = table.get("GGTYPE")
            M_TM = table.get("M_TM")
            AREANAME = table.get("AREANAME")  ##所在的区  福建省除外
            bid_county = None
            if not "福建省" in AREANAME:
                bid_county = AREANAME
            link = "https://ggzyfw.fujian.gov.cn/business/detail?cid={cid}&type={type}".format(cid=cid, type=type)
            ##判断  只存储当前mid的html
            timeNow = int((time.time()) * 1000)
            # timeNow = 1688973723000
            # 3637CB36B2E54A72A7002978D0506CDFm_id234649ts1687921385066type2
            linksign = "{salt}m_id{cid}ts{ts}type{type}".format(salt=self.salt, cid=cid, ts=timeNow, type=GGTYPE)
            linkParam = {"type": GGTYPE, "m_id": str(cid), "ts": timeNow}
            item_info = {
                "bid_url": link,
                "bid_id": get_md5(link),
                "bid_name": title,
                "bid_public_time": M_TM,
            }
            if bid_county:
                item_info["bid_county"] = bid_county
            item_info.update(items)
            self.headers["portal-sign"] = self.get_md5(linksign)
            ##文章去重 redis
            if self.redis_u.run(self.name, link):
                # true 已经存在
                continue
            yield JsonRequest(
                self.content_api,
                data=linkParam,
                callback=self.Contentparse,
                headers=self.headers,
                meta={"items": item_info},
                dont_filter=True,
            )

    def Contentparse(self, response):
        items_info = response.meta["items"]
        jsonDict = json.loads(response.text)
        datastr_d = jsonDict.get("Data")
        dataStr = str(self.aes.decryptFromBase64(datastr_d).data, "utf-8")
        dataDict = json.loads(dataStr)
        contents = dataDict.get("Contents")
        if not contents:
            return
        soup = BeautifulSoup(contents, "lxml")
        content_html = soup.select("body")[0]
        content = soup.select("body")[0].text.strip()
        items = BidScrapyProjectItem()
        items.update(items_info)
        items["bid_province"] = self.province
        items["website_name"] = self.webName
        items["website_url"] = self.webUrl
        items["bid_content"] = content
        items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        items["bid_html_con"] = str(content_html)
        # items["bid_json_data"] = response.text
        yield items

    # 工具
    def get_md5(self, key: str):
        md5_obj = hashlib.md5(key.encode(encoding="utf-8"))
        return md5_obj.hexdigest().lower()
