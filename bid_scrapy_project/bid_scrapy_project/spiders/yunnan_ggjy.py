# -*- coding: utf-8 -*-
# @Time : 2023/6/15
# @Author: mayj

"""
    云南省公共资源交易信息网
"""
import json
import re
import time
import logging

import scrapy
from lxml import etree

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import GovernmentProcurementItem, BidScrapyProjectItem


class YunnanGgjySpider(scrapy.Spider):
    name = "yunnan_ggjy"
    headers = {
        "Content-Type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68",
    }
    start_urls = [
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getTenserPlanList",
            "category": "工程建设",
            "type": "招标计划",
            "colCode": "1",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getTenserPlanDetail?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "tradeType": "gcjs",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getZbggList",
            "category": "工程建设",
            "type": "招标公告",
            "colCode": "1",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/findZbggByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "tradeType": "gcjs",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getGzsxList",
            "category": "工程建设",
            "type": "变更通知",
            "colCode": "1",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/findGzsxByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "tradeType": "gcjs",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getPbbgList",
            "category": "工程建设",
            "type": "中标候选人公示",
            "colCode": "1",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/findPbbgByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "tradeType": "gcjs",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getZbJgGgList",
            "category": "工程建设",
            "type": "中标结果公示",
            "colCode": "1",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/findZbJgGgByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "tradeType": "gcjs",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getContractList",
            "category": "工程建设",
            "type": "合同及履约公示",
            "colCode": "1",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getGcjsContractDetail?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "tradeType": "gcjs",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getZbycList",
            "category": "工程建设",
            "type": "异常公告",
            "colCode": "1",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/findZbycByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 10,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "tradeType": "gcjs",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/zfcg/getCgggList",
            "category": "政府采购",
            "type": "采购公告",
            "colCode": "2",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/zfcg/findCgggByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/zfcg/getGzsxList",
            "category": "政府采购",
            "type": "变更通知",
            "colCode": "2",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/zfcg/findGzsxByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/zfcg/getZbjgList",
            "category": "政府采购",
            "type": "结果公示",
            "colCode": "2",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/zfcg/findZbjgByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/zfcg/getHtgsList",
            "category": "政府采购",
            "type": "合同公示",
            "colCode": "2",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/zfcg/findHtgsByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/zfcg/getYcggList",
            "category": "政府采购",
            "type": "异常公告",
            "colCode": "2",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/zfcg/findYcggByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getTenserPlanList",
            "category": "综合交易",
            "type": "招标计划",
            "colCode": "7",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getTenserPlanDetail?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "tenderSpecializedType": "",
                "childType": "",
                "tradeType": "zhjy",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getZbggList",
            "category": "综合交易",
            "type": "招标公告",
            "colCode": "7",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/findZbggByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "tenderSpecializedType": "",
                "childType": "",
                "tradeType": "zhjy",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getGzsxList",
            "category": "综合交易",
            "type": "变更通知",
            "colCode": "7",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/findGzsxByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "tenderSpecializedType": "",
                "childType": "",
                "tradeType": "zhjy",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getPbbgList",
            "category": "综合交易",
            "type": "中标候选人公示",
            "colCode": "7",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/findPbbgByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "tenderSpecializedType": "",
                "childType": "",
                "tradeType": "zhjy",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getZbJgGgList",
            "category": "综合交易",
            "type": "中标结果公示",
            "colCode": "7",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/findZbJgGgByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "tenderSpecializedType": "",
                "childType": "",
                "tradeType": "zhjy",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getZbycList",
            "category": "综合交易",
            "type": "异常公告",
            "colCode": "7",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/findZbycByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "tenderSpecializedType": "",
                "childType": "",
                "tradeType": "zhjy",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/tdsyq/getTdsyqList",
            "category": "土地使用权",
            "type": "出让公告",
            "colCode": "3",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/tdsyq/findTdsyqByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
                "bulletinNature": 1,
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/tdsyq/getTdsyqList",
            "category": "土地使用权",
            "type": "补充公告",
            "colCode": "3",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/tdsyq/findTdsyqByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
                "bulletinNature": 2,
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/tdsyq/getTdcjzdList",
            "category": "土地使用权",
            "type": "结果公示",
            "colCode": "3",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/tdsyq/findTdcjzdByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/cqjy/getGpggList",
            "category": "国有产权",
            "type": "出让公告",
            "colCode": "4",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/cqjy/findGpggByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
                "bulletinNature": 1,
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/cqjy/getGpggList",
            "category": "国有产权",
            "type": "变更公告",
            "colCode": "4",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/cqjy/findGpggByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
                "bulletinNature": 2,
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/cqjy/getJyjgList",
            "category": "国有产权",
            "type": "交易结果",
            "colCode": "4",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/kyq/getNotificationDetail?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        # {
        #     "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/kyq/getZpcrggList",
        #     "category": "矿业权出让",
        #     "type": "挂牌公告",
        #     "colCode": "5",
        #     "deturl":"https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/kyq/findZpcrggByGuid?guid={}",
        #     "data": {
        #         "pageNum": 1,
        #         "pageSize": 50,
        #         "title": "",
        #         "startTime": "",
        #         "endTime": "",
        #         "areaCode": "018",
        #         "naAppName": "",
        #         "bulletinNature": 1,
        #     },
        # },
        # {
        #     "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/kyq/getBidAnnouncementList",
        #     "category": "矿业权出让",
        #     "type": "报价公告",
        #     "colCode": "5",
        #     "deturl":"https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/kyq/getBidAnnouncementDetail?guid={}",
        #     "data": {
        #         "pageNum": 1,
        #         "pageSize": 50,
        #         "title": "",
        #         "startTime": "",
        #         "endTime": "",
        #         "areaCode": "018",
        #         "naAppName": "",
        #         "type": "",
        #         "bulletinNature": 4,
        #     },
        # },
        # {
        #     "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/kyq/getZpcrggList",
        #     "category": "矿业权出让",
        #     "type": "变更公告",
        #     "colCode": "5",
        #     "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/kyq/findZpcrggByGuid?guid={}",
        #     "data": {
        #         "pageNum": 1,
        #         "pageSize": 50,
        #         "title": "",
        #         "startTime": "",
        #         "endTime": "",
        #         "areaCode": "018",
        #         "naAppName": "",
        #         "type": "",
        #         "bulletinNature": 2,
        #     },
        # },
        # {
        #     "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/kyq/getZpcrggList",
        #     "category": "矿业权出让",
        #     "type": "结果公示",
        #     "colCode": "5",
        #     "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/kyq/findZpJggsByGuid?guid={}",
        #     "data": {
        #         "pageNum": 1,
        #         "pageSize": 50,
        #         "title": "",
        #         "startTime": "",
        #         "endTime": "",
        #         "areaCode": "018",
        #         "naAppName": "",
        #         "type": "",
        #         "bulletinNature": 3,
        #     },
        # },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/tax/getDSCWList",
            "category": "抵税财物",
            "type": "资产公告",
            "colCode": "8",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/tax/getDSCWDetail?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "title": "",
                "startTime": "",
                "endTime": "",
                "cityId": "018",
                "type": "",
                "dscwType": 4,
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/tax/getDSCWList",
            "category": "抵税财物",
            "type": "变更公告",
            "colCode": "8",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/tax/getDSCWDetail?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "title": "",
                "startTime": "",
                "endTime": "",
                "cityId": "018",
                "dscwType": 1,
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/tax/getDSCWList",
            "category": "抵税财物",
            "type": "交易结果",
            "colCode": "8",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/tax/getDSCWDetail?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 10,
                "title": "",
                "startTime": "",
                "endTime": "",
                "cityId": "018",
                "dscwType": 2,
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/otherJy/getJyGgList",
            "category": "其他",
            "type": "招标公告",
            "colCode": "6",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/otherJy/findJyGgByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/otherJy/getGzGgList",
            "category": "其他",
            "type": "变更公告",
            "colCode": "6",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/otherJy/findGzGgByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
        {
            "url": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/otherJy/getJgGsList",
            "category": "其他",
            "type": "结果公示",
            "colCode": "6",
            "deturl": "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/otherJy/findJgGsByGuid?guid={}",
            "data": {
                "pageNum": 1,
                "pageSize": 50,
                "cityId": "018",
                "industryCode": "",
                "childType": "",
                "title": "",
                "startTime": "",
                "endTime": "",
            },
        },
    ]
    area_codes = [
        {"id": "001", "areaName": "省本级", "orderid": 2, "areaWord": "yunnan", "routediqucode": 53e4},
        {"id": "002", "areaName": "昆明市", "orderid": 3, "areaWord": "kunming", "routediqucode": 530100},
        {"id": "003", "areaName": "曲靖市", "orderid": 4, "areaWord": "qujing", "routediqucode": 530300},
        {"id": "004", "areaName": "玉溪市", "orderid": 5, "areaWord": "yuxi", "routediqucode": 530400},
        {"id": "005", "areaName": "保山市", "orderid": 6, "areaWord": "baoshan", "routediqucode": 530500},
        {"id": "006", "areaName": "昭通市", "orderid": 7, "areaWord": "zhaotong", "routediqucode": 530600},
        {"id": "007", "areaName": "丽江市", "orderid": 8, "areaWord": "lijiang", "routediqucode": 530700},
        {"id": "008", "areaName": "普洱市", "orderid": 9, "areaWord": "puer", "routediqucode": 530800},
        {"id": "009", "areaName": "临沧市", "orderid": 10, "areaWord": "lincang", "routediqucode": 530900},
        {"id": "010", "areaName": "德宏州", "orderid": 16, "areaWord": "dehong", "routediqucode": 533100},
        {"id": "011", "areaName": "怒江州", "orderid": 17, "areaWord": "nujiang", "routediqucode": 533300},
        {"id": "012", "areaName": "迪庆州", "orderid": 18, "areaWord": "diqing", "routediqucode": 533400},
        {"id": "013", "areaName": "大理州", "orderid": 15, "areaWord": "dali", "routediqucode": 532900},
        {"id": "014", "areaName": "楚雄州", "orderid": 11, "areaWord": "chuxiong", "routediqucode": 532300},
        {"id": "015", "areaName": "红河州", "orderid": 12, "areaWord": "honghe", "routediqucode": 532500},
        {"id": "016", "areaName": "文山州", "orderid": 13, "areaWord": "wenshan", "routediqucode": 532600},
        {"id": "017", "areaName": "西双版纳", "orderid": 14, "areaWord": "xishuangbanna", "routediqucode": 532800},
        {"id": "018", "areaName": "信息网", "orderid": 15, "areaWord": "xishuangbanna"},
    ]

    def start_requests(self):
        for url_dict in self.start_urls:
            data = json.dumps(url_dict["data"])
            yield scrapy.Request(
                url=url_dict["url"],
                body=data,
                method="POST",
                headers=self.headers,
                meta=url_dict,
                callback=self.parse_list,
                dont_filter=True,
            )

    def parse_list(self, response):
        res_vals = response.json()["value"]["list"]
        for res_val in res_vals:
            meta_data = {}

            meta_data["county"] = res_val.get("jyptid", "")
            # 获取开始时间
            meta_data["pub_time"] = ""
            start_time_str_list = [
                "bulletinissuetime",
                "publishTime",
                "fabutime",
                "publicitystarttime",
                "gongshiTime",
                "bulletinstarttime",
                "modificationstarttime",
                "winbidbulletinstarttime",
                "createtime",
                "publishingTime",
                "publishDate",
                "startTime",
            ]
            for start_time_str in start_time_str_list:
                if meta_data["pub_time"]:
                    break
                for res_val_key in list(res_val.keys()):
                    if start_time_str == res_val_key:
                        meta_data["pub_time"] = res_val.get(res_val_key, "")
                        if meta_data["pub_time"]:
                            break
            # 获取结束时间
            # end_time_str_list = ["bulletinendtime"]
            # meta_data["end_time"] = ""
            # for end_time_str in end_time_str_list:
            #     if meta_data["end_time"]:
            #         break
            #     for end_key in list(res_val.keys()):
            #         if end_time_str == end_key:
            #             meta_data["end_time"] = res_val.get(end_time_str, "")
            #             if meta_data["end_time"]:
            #                 break

            # 获取标题
            meta_data["po_name"] = ""
            po_name_str_list = [
                "tenderprojectcode",
                "bulletinname",
                "changetitle",
                "publicityname",
                "contractName",
                "exceptionName",
                "bulletintitle",
                "terminationbulletintitle",
                "winbidbulletintitle",
                "purchaseprojectname",
                "tenderProjectName",
                "announcementTitle",
                "naAppName",
                "title",
                "projectName",
            ]
            for po_name_str in po_name_str_list:
                if meta_data["po_name"]:
                    break
                for po_name_key in list(res_val.keys()):
                    if po_name_str == po_name_key:
                        meta_data["po_name"] = res_val.get(po_name_str, "")
                        if meta_data["po_name"]:
                            break

            # 获取城市名称
            areaCode = res_val.get("areaCode", "")
            city = ""
            if areaCode:
                for area_code in self.area_codes:
                    if area_code["id"] == areaCode:
                        city = area_code["areaName"]
                        break
            meta_data["city"] = city

            meta_data["type"] = response.meta["type"]
            meta_data["category"] = response.meta["category"]

            # 获取详情链接相关
            rowCode = response.meta["type"]
            colCode = response.meta["colCode"]
            guid = res_val.get("guid", "")
            announcementGuid = res_val.get("announcementGuid", "")
            det_url = f"https://ggzy.yn.gov.cn/tradeHall/tradeDetail?"
            if guid:
                det_url += f"guid={guid}"
                req_det_url = response.meta["deturl"].format(guid)
            elif announcementGuid:
                det_url += f"announcementGuid={announcementGuid}"
                req_det_url = response.meta["deturl"].format(announcementGuid)

            det_url += f"&colCode={colCode}&rowCode={rowCode}&from=jiaoYi"
            resultType = res_val.get("resultType", "")
            if resultType:
                det_url += f"&resultType={resultType}"
            conrtractType = res_val.get("conrtractType", "")
            if conrtractType:
                det_url += f"&conrtractType={conrtractType}"

            childType = res_val.get("type", "")
            if childType:
                det_url += f"&type={childType}"
                req_det_url += f"&childType={childType}"
            meta_data["data"] = res_vals
            if response.meta["category"] == "国有产权" and response.meta["type"] == "交易结果":
                projectCode = res_val.get("projectCode", "")
                if projectCode:
                    req_det_url = re.sub(
                        "ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/kyq/getNotificationDetail",
                        "ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/cqjy/findJyjgByGuid",
                        req_det_url,
                    )

            if response.meta["category"] == "土地使用权" and response.meta["type"] == "结果公示":
                if resultType == "1":
                    req_det_url = re.sub(
                        "ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/tdsyq/findTdcjzdByGuid",
                        "ggzy.yn.gov.cn/ynggfwpt-home-api/jyInfo/kyq/getNotificationDetail",
                        req_det_url,
                    )

            meta_data["det_url"] = det_url
            yield scrapy.Request(url=req_det_url, meta=meta_data, callback=self.parse_detail)

    def parse_detail(self, response):
        json_data = response.json()["value"]
        if not json_data:
            logging.warning(
                json.dumps(
                    {
                        "res_url": response.url,
                        "url": response.meta["det_url"],
                        "cate": response.meta["category"],
                    }
                )
            )
            return
        po_id = get_md5(response.url)
        bid_url = response.meta["det_url"]
        po_province = "云南省"
        po_city = response.meta["city"]
        po_county = response.meta["county"]
        po_category = response.meta["category"]
        po_info_type = response.meta["type"]
        po_public_time = response.meta["pub_time"]
        # bid_end_time = response.meta["end_time"]
        bo_name = response.meta["po_name"]
        # po_source = scrapy.Field()  # 采购数据来源

        # 获取带标签的content
        po_html_con = ""
        content_str_list = [
            "bulletincontent",
            "content",
            "changecontent",
            "publicitycontent",
            "contractContent",
            "exceptionInfor",
            "terminationbulletincontent",
            "winbidbulletincontent",
            "contractContent",
            "announcementConnect",
            "ggNeirong",
        ]
        for content_str in content_str_list:
            if po_html_con:
                break
            for po_html_con_key in list(json_data.keys()):
                if content_str == po_html_con_key:
                    po_html_con = json_data.get(content_str, "")
                    if po_html_con:
                        break
        po_html_con = po_html_con.replace("'", "’")
        po_content = ""
        if po_html_con:
            tree_html = etree.HTML(po_html_con)
            po_content = tree_html.xpath("string(.)").replace("'", "’")
        website_name = "云南省公共资源交易信息网"
        website_url = "https://ggzy.yn.gov.cn/homePage"
        # bid_orgin_url = scrapy.Field()  # 原始网页链接
        create_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

        if response.meta["category"] == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = po_id
            item["bid_url"] = bid_url
            item["po_province"] = po_province
            item["po_city"] = po_city
            item["po_county"] = po_county
            item["po_category"] = po_category
            item["po_info_type"] = po_info_type
            item["po_public_time"] = po_public_time
            item["bo_name"] = bo_name
            item["po_html_con"] = po_html_con
            item["po_content"] = po_content
            item["website_name"] = website_name
            item["website_url"] = website_url
            item["create_datetime"] = create_datetime
            item["po_json_data"] = str(response.json())

        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = po_id
            item["create_datetime"] = create_datetime
            item["bid_url"] = bid_url
            item["bid_province"] = po_province
            item["bid_city"] = po_city
            item["bid_county"] = po_county
            item["bid_category"] = po_category
            item["bid_info_type"] = po_info_type
            item["bid_name"] = bo_name
            item["bid_public_time"] = po_public_time
            item["bid_html_con"] = po_html_con
            item["bid_content"] = po_content
            item["website_name"] = website_name
            item["website_url"] = website_url
            item["bid_json_data"] = str(response.json())

        yield item
