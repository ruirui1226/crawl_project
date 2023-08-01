#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/10 9:24
# @Author  : xm
# @File    : guangdong_cgw.py
# @Description : 广东省政府采购网
import json
import time

import ddddocr
import requests
import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import GovernmentProcurementItem


class GuangdongCgwSpider(scrapy.Spider):
    name = "guangdong_cgw"

    def __init__(self):
        self.tytpes = {
            "采购意向公开": "59",
            "单一来源公示": "001051",
            "采购计划": "001101",
            "采购需求": "001059",
            "资格预审公告": "001052-001053",
            "采购公告": "00102",
            "更正公告": "00103",
            "终止公告": "001004-001006",
            "合同公告": "001054",
            "验收公告": "001009-00105A",
        }
        self.province = "广东省"
        self.category = "政府采购"
        self.website_name = "广东省政府采购网"
        self.webUrl = "https://gdgpo.czt.gd.gov.cn/"
        self.page = 4
        ##对比
        self.cityInfo = {
            "省本级": ["广东省省本级"],
            "广州市": ["广州市市本级", "越秀区", "海珠区", "荔湾区", "天河区", "白云区", "黄埔区", "花都区", "番禺区", "南沙区", "从化区", "增城区"],
            "珠海市": ["珠海市市本级", "香洲区", "斗门区", "金湾区", "高新区", "高栏港经济区", "万山区", "保税区"],
            "汕头市": ["汕头市市本级", "龙湖区", "金平区", "濠江区", "潮阳区", "潮南区", "澄海区", "南澳县", "华侨经济文化合作试验区", "汕头华侨经济文化合作试验区"],
            "佛山市": ["佛山市市本级", "禅城区", "南海区", "顺德区", "高明区", "三水区"],
            "韶关市": ["韶关市市本级", "浈江区", "武江区", "曲江区", "乐昌市", "南雄市", "仁化县", "始兴县", "翁源县", "新丰县", "乳源瑶族自治区", "韶关新区"],
            "河源市": ["河源市市本级", "源城区", "东源县", "和平县", "龙川县", "紫金县", "连平县", "江东新区", "高新区"],
            "梅州市": ["梅州市市本级", "梅江区", "梅县区", "兴宁市", "平远县", "蕉岭县", "大埔县", "丰顺县", "五华县"],
            "惠州市": ["惠州市市本级", "惠城区", "惠阳区", "惠东县", "博罗县", "龙门县", "大亚湾经济开发区", "惠州仲恺高新技术产业开发区"],
            "汕尾市": ["汕尾市市本级", "城区", "海丰县", "陆丰市", "陆河县", "红海湾开发区", "华侨管理区", "新区管理委员会"],
            "东莞市": [
                "东莞市市本级",
                "松山湖园区",
                "莞城街道",
                "东城街道",
                "万江街道",
                "南城街道",
                "虎门镇",
                "石龙镇",
                "中堂镇",
                "望牛墩镇",
                "道滘镇",
                "洪梅镇",
                "麻涌镇",
                "长安镇",
                "厚街镇",
                "沙田镇",
                "寮步镇",
                "大岭山镇",
                "大朗镇",
                "黄江镇",
                "清溪镇",
                "樟木头镇",
                "塘厦镇",
                "凤岗镇",
                "谢岗镇",
                "常平镇",
                "桥头镇",
                "横沥镇",
                "东坑镇",
                "企石镇",
                "石排镇",
                "茶山镇",
                "石碣镇",
                "高埗镇",
                "滨海湾新区",
                "水乡",
            ],
            "中山市": [
                "中山市市本级",
                "石岐街道",
                "东区街道",
                "火炬区",
                "西区街道",
                "南区街道",
                "小榄镇",
                "黄圃镇",
                "东凤镇",
                "古镇镇",
                "沙溪镇",
                "坦洲镇",
                "港口镇",
                "三角镇",
                "横栏镇",
                "南头镇",
                "阜沙镇",
                "三乡镇",
                "板芙镇",
                "大涌镇",
                "神湾镇",
                "五桂山街道",
                "翠亨新区",
            ],
            "江门市": ["江门市市本级", "蓬江区", "江海区", "新会区", "鹤山市", "台山市", "恩平市", "开平市"],
            "阳江市": ["阳江市市本级", "阳春市", "阳西县", "阳东区", "江城区", "海陵岛经济开发试验区", "阳江高新技术产业开发区", "阳江滨海新区"],
            "湛江市": [
                "湛江市市本级",
                "赤坎区",
                "霞山区",
                "麻章区",
                "坡头区",
                "雷州市",
                "廉江市",
                "吴川市",
                "遂溪县",
                "徐闻县",
                "湛江经济技术开发区管委会",
                "湛江经济技术开发区",
            ],
            "茂名市": ["茂名市市本级", "茂南区", "高州市", "信宜市", "化州市", "电白区", "高新技术产业开发区", "滨海新区", "水东湾新城"],
            "肇庆市": ["肇庆市市本级", "端州区", "鼎湖区", "高要区", "四会市", "广宁县", "德庆县", "封开县", "怀集县", "肇庆高新区", "肇庆新区", "粤桂合作特别试验区"],
            "清远市": [
                "清远市市本级",
                "清远高新区",
                "清城区",
                "清新区",
                "英德市",
                "连州市",
                "佛冈县",
                "连山壮族瑶族自治县",
                "连南瑶族自治区",
                "阳山县",
                "广清产业园",
                "连南瑶族自治县",
            ],
            "潮州市": ["潮州市市本级", "潮安区", "饶平县", "湘桥区", "枫溪区"],
            "揭阳市": [
                "揭阳市市本级",
                "揭阳高新技术产业开发区",
                "揭西县",
                "普宁市",
                "大南海工业区",
                "揭阳产业转移工业园",
                "揭东区",
                "榕城区",
                "惠来县",
                "粤东新城",
                "揭阳大南海石化工业区",
            ],
            "云浮市": ["云浮市市本级", "云城区", "云安区", "罗定市", "新兴县", "郁南县", "云浮新区"],
            "横琴粤澳深度合作区": ["横琴粤澳深度合作区"],
        }

    def start_requests(self):
        try:
            getCode = self.getCode()
        except:
            return
        for typename, typeid in self.tytpes.items():
            for i in range(1, self.page):
                url = "https://gdgpo.czt.gd.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?siteId=cd64e06a-21a7-4620-aebc-0576bab7e07a&channel=fca71be5-fc0c-45db-96af-f513e9abda9d&currPage={page}&pageSize=10&noticeType={typeid}&regionCode=&verifyCode={code}&subChannel=false&purchaseManner=&title=&openTenderCode=&purchaser=&agency=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime&cityOrArea=".format(
                    page=i, typeid=typeid, code=getCode
                )
                items = {"typename": typename}
                yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={"items": items, "code": getCode})

    def parse(self, response, **kwargs):
        jsonDict = json.loads(response.text)
        dataList = jsonDict.get("data")
        for data in dataList:
            title = data.get("title")
            cityname = data.get("regionName").strip()
            ##判断是哪个市的
            city_name = None
            try:
                city_name = [k for k, v in self.cityInfo.items() if cityname in v][0]
            except:
                print("erro", cityname)
            author = data.get("purchaser")
            link = data.get("pageurl")
            link = response.urljoin(link)
            noticeTime = data.get("noticeTime")  ##发布时间 2023-07-10 12:44:50
            items = {"title": title, "author": author, "city": city_name, "pubdate": noticeTime, "link": link}
            items.update(response.meta["items"])
            yield scrapy.Request(url=link, callback=self.getContent, meta={"items": items})

    def getContent(self, response):
        item_info = response.meta["items"]
        content_html = response.css(".noticeArea").get()
        contents = response.css(".noticeArea *::text").extract()
        content = "".join(contents)
        items = {
            "po_id": get_md5(item_info.get("link")),
            "bid_url": item_info.get("link"),
            "po_province": self.province,
            "po_city": item_info.get("city"),
            "po_category": self.category,
            "po_info_type": item_info.get("typename"),
            "po_public_time": item_info.get("pubdate"),
            "bo_name": item_info.get("title"),
            "po_source": item_info.get("author"),
            "po_html_con": content_html,
            "po_content": content,
            "website_name": self.website_name,
            "website_url": self.webUrl,
            "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }
        item_po = GovernmentProcurementItem()
        item_po.update(items)
        # print(items)
        yield item_po

    # 工具
    def getCode(self):
        url = "https://gdgpo.czt.gd.gov.cn/freecms/verify/verifyCode.do?createTypeFlag=n&name=notice&d{nowtime}".format(
            nowtime=int(time.time() * 1000)
        )
        r = requests.get(url)
        ocr = ddddocr.DdddOcr()
        res = ocr.classification(r.content)
        return res
