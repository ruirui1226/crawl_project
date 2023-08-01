# -*- coding: utf-8 -*-
"""
@desc: 湖南省公共资源交易中心
@version: python3
@author: xm
@time: 2023/06/19
"""
import time
from urllib.parse import quote

import scrapy

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import GovernmentProcurementItem, BidScrapyProjectItem


class HunanGgjySpider(scrapy.Spider):
    name = "hunan_ggjy"

    # allowed_domains = ['www.hnsggzy.com']
    # start_urls = ['http://www.hnsggzy.com/']
    def __init__(self):
        # https://www.hnsggzy.com/queryContent-jygk.jspx?title=&origin=%E7%9C%81&inDates=&channelId=853&ext=%E5%85%AC%E5%BC%80%E6%8B%9B%E6%A0%87&beginTime=&endTime=
        # https://www.hnsggzy.com/queryContent-jygk.jspx?title=&origin=%E7%9C%81&inDates=&channelId=857&ext=&beginTime=&endTime=
        self.categoryList = [
            # https://www.hnsggzy.com/queryContent-jygk.jspx?title=&origin=&inDates=&channelId=848&ext=%E6%8B%9B%E6%A0%87%2F%E8%B5%84%E5%AE%A1%E5%85%AC%E5%91%8A&beginTime=&endTime=
            {
                "工程建设类": {
                    "value": "846",
                    "招标类型": {"房建市政工程": "848", "工业工程": "847", "水利工程": "849", "交通工程": "850", "其他": "3770"},
                    "信息类型": {"招标/资审公告": None, "招标澄清": None, "中标候选人公示": None, "中标结果公告": None},
                }
            },
            # https://www.hnsggzy.com/queryContent-jygk.jspx?title=&origin=&inDates=&channelId=853&ext=%E5%85%AC%E5%BC%80%E6%8B%9B%E6%A0%87&beginTime=&endTime=
            {
                "政府采购类": {
                    "value": "851",
                    "招标类型": {"公开招标": None, "邀请招标": None, "竞争性谈判": None, "竞争性磋商": None, "单一来源": None, "询价": None},
                    "信息类型": {"采购公告": "853", "更正事项": "854", "中标公告": "855"},
                }
            },
            {"土地使用权": {"value": "856", "招标类型": {"出让公告": "857", "成交宗地": "858"}, "信息类型": {}}},
            {
                "矿业权出让": {
                    "value": "859",
                    "招标类型": {"出让公告": "860", "出让结果": "861", "公开信息": "862", "登记公告信息": "863"},
                    "信息类型": {},
                }
            },
            {"产权交易类": {"value": "864", "招标类型": {"挂牌披露": "865", "交易结果": "866"}, "信息类型": {}}},
            {"其他交易": {"value": "869", "招标类型": {"交易公告": "870", "成交公示": "871"}, "信息类型": {}}},
            # {
            #     "医药采购类": {
            #         "招标类型": {"药品集中采购": "868", "耗材集中采购": "3530", "二类疫苗集中采购": "3531"},
            #         "信息类型": {},
            #     }
            # },
            # {
            #     "限下项目": {
            #         "招标类型": {"招标公告": "3590", "中标结果公告": "3591", "中标候选人公示": "3592"},
            #         "信息类型": {},
            #     }
            # },
            # {
            #     "国际招投标": {
            #         "招标类型": {"资格预审公告": "3594", "澄清公告": "3595", "招标公告": "3596", "投标邀请书": "3597"},
            #         "信息类型": {},
            #     }
            # },
            # {"林权交易": {"招标类型": {"挂牌披露": "3993", "成交公告": "3994"}, "信息类型": {}}},
            # {
            #     "排污权交易": {
            #         "招标类型": {"出让交易公告": "3995", "转让交易公告": "3996", "出让结果公告": "3997", "转让结果公告": "3998"},
            #         "信息类型": {},
            #     }
            # },
            # {"碳排放交易": {"招标类型": {"出售公告": "3999", "出售结果公示": "4000"}, "信息类型": {}}},
            # {"土地指标": {"招标类型": {"交易公告": "4001", "结果公告": "4002"}, "信息类型": {}}},
        ]

        """  其他类型
            "交易过程信息": {},
            "市场主体基本信息": {},
            {
                "信用信息": {
                    "违法违规信息": {
                        "id": "895",
                        "招标类型": {"禁止参加招标代理活动": None, "禁止参加投标活动": None, "禁止参加评标、评审活动": None, "其他": None},
                        "信息类型": {},
                    },
                    "黑名单": {"id": "896", "招标类型": {"自然人": None, "法人": None, "其他": None}, "信息类型": {}},
                    "撤销黑名单信息": {"id": "897", "招标类型": {"自然人": None, "法人": None, "其他": None}, "信息类型": {}},
                    "奖励信息": {"id": "898", "招标类型": {"自然人": None, "法人": None, "其他": None}, "信息类型": {}},
                    "履约信息": {"id": "899", "招标类型": {"自然人": None, "法人": None, "其他": None}, "信息类型": {}},
                }
            },
            {"监管信息": {"行政监管事项": {"id": "902", "招标类型": {"是": None, "否": None}, "信息类型": {}}}},
            "药品信息": {
                "药品信息": {"招标类型": {}, "信息类型": {}},
                "耗材信息": {"招标类型": {}, "信息类型": {}},
                "疫苗信息": {"招标类型": {}, "信息类型": {}},
            },
        """
        # self.citys = ["省本级", "长沙", "株洲", "湘潭", "衡阳", "邵阳", "岳阳", "常德", "张家界", "益阳", "娄底", "郴州", "永州", "怀化", "湘西"]
        self.province = "湖南省"
        self.website_name = "湖南省公共资源交易中心"
        self.website_url = "http://www.hnsggzy.com/"
        self.page = 15

    def start_requests(self):
        for i in self.categoryList:
            # for city in self.citys:
            # 循环城市
            for category_name, v in i.items():
                page = 1
                #  https://www.hnsggzy.com/queryContent-jygk.jspx?title=&origin=&inDates=1&channelId=869&ext=&beginTime=&endTime=  当天
                url_list = "https://www.hnsggzy.com/queryContent_{}-jygk.jspx?title=&origin=&inDates=1&channelId={}&ext=&beginTime=&endTime=".format(
                    page, v.get("value")
                )
                items = {
                    "bid_category": category_name,
                    # "bid_info_type": info_type_name,
                }
                yield scrapy.Request(
                    url_list, self.parse, meta={"items": items, "page": 1, "valueid": v.get("value")}, dont_filter=True
                )

    def parse(self, response):
        """
        文章列表页
        """
        items_info = response.meta["items"]
        lis = response.css(".article-list2 >li")
        if not lis:
            ##此类别没有数据
            print(items_info, "该类别没有数据")
            return
        for li in lis:
            href = li.css(".article-list3-t > a::attr(href)").get()
            titles = li.css(".article-list3-t > a *::text").extract()
            title = "".join(x.strip() for x in titles)
            info_div = li.css(".article-list3-t2 > div")
            source = None
            infoType = None
            for div in info_div:
                info = div.css("div::text").get().strip()
                if "来源" in info:
                    source = info[info.index("来源：") + len("来源：") :]
                elif "信息类型" in info:
                    infoType = info[info.index("信息类型：") + len("信息类型：") :]
            items = {"bid_name": title, "bid_url": href, "cityName": source, "infoType": infoType}
            items.update(items_info)
            yield scrapy.Request(href, self.getContent, meta={"items": items})
        ##下一页
        page_all = response.css("ul.pages-list > li:nth-child(1) > a::text").get()
        try:
            page = page_all[
                page_all.index(r"{}/".format(response.meta["page"]))
                + len(r"{}/".format(response.meta["page"])) : page_all.rindex("页")
            ]
        except:
            print()
            return
        page_next = response.meta["page"] + 1
        if not page == "1":
            if page_next < int(page) or page_next == int(page):
                if page_next < self.page:
                    url_list = "https://www.hnsggzy.com/queryContent_{}-jygk.jspx?title=&origin=&inDates=1&channelId={}&ext=&beginTime=&endTime=".format(
                        page_next, response.meta["valueid"]
                    )
                    yield scrapy.Request(
                        url_list,
                        self.parse,
                        meta={"items": response.meta["items"], "page": page_next, "valueid": response.meta["valueid"]},
                        dont_filter=True,
                    )

    def getContent(self, response):
        """
        文章页
        """
        items_info = response.meta["items"]
        spans = response.css("div.content-title2 > span")
        pubdate = None
        for span in spans:
            span_info = span.css("span::text").get().strip()
            if "时间" in span_info:
                pubdate = span_info[span_info.index("时间：") + len("时间：") :]
                break
        contents = response.css(".div-article2 *::text").extract()
        if not contents:
            contents = response.css(".content-article *::text").extract()
            content_html = str(response.css(".content-article").get())
        else:
            content_html = str(response.css(".div-article2").get())
        content = remove_node(content_html, ["style"]).text
        if "省本级" in items_info["cityName"]:
            city = None
        else:
            city = items_info["cityName"]
        # print(
        #     get_md5(items_info["bid_url"]),
        #     items_info["bid_url"],
        #     items_info["bid_category"],
        #     items_info["infoType"],
        #     items_info["bid_name"],
        #     pubdate,
        # )
        if "政府采购" in items_info["bid_category"]:
            items_cg = GovernmentProcurementItem()
            items_cg["po_id"] = get_md5(items_info["bid_url"])
            items_cg["bid_url"] = items_info["bid_url"]
            items_cg["bo_name"] = items_info["bid_name"]
            items_cg["po_category"] = items_info["bid_category"]
            items_cg["po_info_type"] = items_info["infoType"]
            items_cg["po_city"] = city
            items_cg["po_province"] = self.province
            items_cg["website_name"] = self.website_name
            items_cg["website_url"] = self.website_url
            items_cg["po_public_time"] = pubdate
            items_cg["po_content"] = content
            items_cg["po_html_con"] = content_html
            items_cg["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            yield items_cg
        else:
            items = BidScrapyProjectItem()
            items["bid_id"] = get_md5(items_info["bid_url"])
            items["bid_url"] = items_info["bid_url"]
            items["bid_name"] = items_info["bid_name"]
            items["bid_category"] = items_info["bid_category"]
            items["bid_info_type"] = items_info["infoType"]
            items["bid_city"] = city
            items["bid_province"] = self.province
            items["website_name"] = self.website_name
            items["website_url"] = self.website_url
            items["bid_public_time"] = pubdate
            items["bid_content"] = content
            items["bid_html_con"] = content_html
            items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            yield items
