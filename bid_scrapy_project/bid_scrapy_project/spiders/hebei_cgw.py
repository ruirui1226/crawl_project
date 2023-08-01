#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/5 13:46
# @Author  : xm
# @File    : hebei_cgw.py
# @Description : 中国河北政府采购网
import time

import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import GovernmentProcurementItem


class HebeiCgwSpider(scrapy.Spider):
    name = "hebei_cgw"

    def __init__(self):
        self.city1 = [
            "石家庄$$130100000",
            "辛集市$$130181000",
            "唐山市$$130200000",
            "秦皇岛市$$130300000",
            "邯郸市$$130400000",
            "邢台市$$130500000",
            "保定市$$130600000",
            "定州市$$130682000",
            "张家口市$$130700000",
            "承德市$$130800000",
            "沧州市$$130900000",
            "廊坊市$$131000000",
            "衡水市$$131100000",
            "雄安新区$$139900000",
        ]
        self.types = {
            r"招标（采购）/资格预审": "zbgg",
            "中标（成交）结果": "zhbgg",
            "废标（终止）": "zbgg",
            "更正": "gzgg",
            "单一来源公示": "dyly",
            r"合同/验收结果": "htgg",
        }
        self.page = 2
        self.province = "河北省"
        self.category = "政府采购"
        self.website_name = "中国河北政府采购网"
        self.webUrl = "http://www.ccgp-hebei.gov.cn/province/"

    def start_requests(self):
        for city_info in self.city1:
            city_id = city_info.split("$$")[1]
            city_name = city_info.split("$$")[0]
            for typename, typeid in self.types.items():
                for i in range(1, self.page):
                    url = "http://search.hebcz.cn:8080/was5/web/search?page={page}&channelid=240117&perpage=50&outlinepage=10&lanmu={typeid}&admindivcode={city}".format(
                        page=i, typeid=typeid, city=city_id
                    )
                    items = {"cityname": city_name, "typename": typename}
                    yield scrapy.Request(url, callback=self.parse, meta={"items": items}, dont_filter=True)

    def parse(self, response, **kwargs):
        trs = response.css(".outline > #moredingannctable tr")
        for i in range(0, len(trs), 2):
            contHref = trs[i].css("a::attr(href)").get()
            title = trs[i].css("a::text").get().strip()
            # 获取其他信息
            infos = trs[i + 1].css("td.txt1 *::text").extract()
            info = "".join(x.strip() for x in infos)
            # 处理
            pubdate = info[info.index("发布时间：") + len("发布时间：") : info.index("地域")]
            source = info[info.index("采购人：") + len("采购人：") :]
            items = {"title": title, "href": contHref, "pubdate": pubdate, "souce": source}
            items.update(response.meta["items"])
            yield scrapy.Request(contHref, callback=self.getContentParse, meta={"items": items})

    def getContentParse(self, response):
        item_info = response.meta["items"]
        content_html = response.css("td > span.txt7").get()
        contents = response.css("td > span.txt7 *::text").extract()
        content = "".join(x.strip() for x in contents)
        items = {
            "po_id": get_md5(item_info.get("href")),
            "bid_url": item_info.get("href"),
            "po_province": self.province,
            "po_city": item_info.get("cityname"),
            "po_category": self.category,
            "po_info_type": item_info.get("typename"),
            "po_public_time": item_info.get("pubdate"),
            "bo_name": item_info.get("title"),
            "po_source": item_info.get("souce"),
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
