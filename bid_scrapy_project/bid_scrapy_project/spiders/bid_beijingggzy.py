# -*- coding: utf-8 -*-
"""
@desc: 北京市公共资源交易服务平台
@version: python3
@author: xm
@time: 2023/06/14
"""

import time
import scrapy
from bs4 import BeautifulSoup
from lxml import html

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class BidBeijingggzySpider(scrapy.Spider):
    """
    北京市公共资源交易服务平台
    """

    name = "bid_beijingggzy"

    # allowed_domains = ['ggzyfw.beijing.gov.cn']
    # start_urls = ['http://ggzyfw.beijing.gov.cn/']
    def __init__(self):
        pass

    def start_requests(self):
        URL = "https://ggzyfw.beijing.gov.cn/jyxxgcjszbjh/index.html"
        yield scrapy.Request(URL, callback=self.parse)

    def parse(self, response):
        """
        业务类型
        """

        lis = response.css("div.panel-search > div > ul > li")
        for li in lis:
            items = {}
            data_href = li.css("li::attr(data-href)").get()
            data_href = response.urljoin(data_href)
            businessName = str(li.css("li::text").get()).strip()
            items["bid_category"] = businessName
            yield scrapy.Request(data_href, callback=self.data_Parse, meta={"items": items}, dont_filter=True)

    def data_Parse(self, response):
        """
        公示类型   翻页
        """
        ass = response.css("ul.panel-tab2.clearfix > li:nth-child(1) > ul > li > a")
        items = response.meta["items"]
        for a in ass:
            href = a.css("a::attr(href)").get()
            href = response.urljoin(href)
            formulaName = str(a.css("a::text").get()).strip()
            items["bid_info_type"] = formulaName
            yield scrapy.Request(href, callback=self.getContentParse, meta={"items": items})
            ##翻页
            # https://ggzyfw.beijing.gov.cn/jyxxgcjszbjh/index_3.html    https://ggzyfw.beijing.gov.cn/jyxxggjtbyqs/index.html
            for page in range(2, 4):
                nextPageUrl = href.replace("index.html", "index_" + str(page) + ".html")
                yield scrapy.Request(
                    nextPageUrl, callback=self.getContentParse, meta={"items": items}, dont_filter=True
                )

    def getContentParse(self, response):
        """
        获取文章url，标题 时间
        """

        items = response.meta["items"]
        lis = response.css("#cmsContent > ul > li")
        for li in lis:
            contentUrl = li.css("a::attr(href)").get()
            contentUrl = response.urljoin(contentUrl)
            title = li.css("a::attr(title)").get()
            times1 = li.css("div.list-times1 *::text").extract()
            ##此时间用来备用 当详情页没有时间的时候就将这个时间复制到发布时间的字段中
            times = "".join(x.strip() for x in times1)
            metas = {"title": title, "times": times}
            item_info = {}
            item_info["bid_url"] = contentUrl
            item_info["bid_name"] = title
            item_info["bid_id"] = get_md5(contentUrl)
            item_info.update(items)
            metas["items"] = item_info
            yield scrapy.Request(contentUrl, callback=self.getContentInfo, meta=metas)

    def getContentInfo(self, response):
        """
        获取文章内容 html等
        """
        items_info = response.meta["items"]
        title2 = response.css("div.div-title2::text").get().strip()
        pudate = (
            (title2[title2.index("发布时间：") + len("发布时间：") : title2.index("信息来源")].strip())
            if "发布时间" in title2 and "信息来源" in title2
            else None
        )
        # 信息来源
        author = (
            (title2[title2.index("信息来源：") + len("信息来源：") : title2.index("浏览次数")].strip())
            if "信息来源" in title2 and "浏览次数" in title2
            else None
        )
        contentHtml = str(response.css("div.zt-child").get()).replace("'", "’")
        if not contentHtml or contentHtml == "None":
            contentHtml = str(response.css("div.newsCon").get()).replace("'", "’")
            if "<style" in contentHtml:
                contents = [remove_node(str(response.css("div.newsCon").get()), ["style"]).text]
            else:
                contents = response.css("div.newsCon *::text").extract()
        else:
            contents = response.css("div.zt-child *::text").extract()
        content = ("".join(x.strip() for x in contents)).replace("'", "’")
        if not pudate:
            pudate = response.meta["times"]
        if "政府采购" in items_info["bid_category"]:
            items_cg = GovernmentProcurementItem()
            items_cg["po_province"] = "北京"
            items_cg["website_name"] = "北京市公共资源交易服务平台"
            items_cg["website_url"] = "https://ggzyfw.beijing.gov.cn/"
            items_cg["po_source"] = author
            items_cg["bo_name"] = items_info.get("bid_name", None)
            items_cg["po_public_time"] = pudate
            items_cg["po_category"] = items_info.get("bid_category", None)
            items_cg["po_info_type"] = items_info.get("bid_info_type", None)
            items_cg["po_city"] = "北京市"
            items_cg["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items_cg["bid_url"] = response.request.url
            items_cg["po_id"] = get_md5(response.request.url)
            items_cg["po_html_con"] = contentHtml
            items_cg["po_content"] = content.strip()
            # print(
            #     items_cg["po_id"],
            #     items_cg["bid_url"],
            #     items_cg["po_category"],
            #     items_cg.get("po_info_type", None),
            #     items_cg["bo_name"],
            #     items_cg["po_source"],
            #     items_cg["po_public_time"],
            # )
            yield items_cg
        else:
            ##修改格式
            items = BidScrapyProjectItem(
                bid_city="北京市",
                website_name="北京市公共资源交易服务平台",
                website_url="https://ggzyfw.beijing.gov.cn/",
                bid_province="北京",
            )
            items.update(items_info)
            items["bid_public_time"] = pudate
            items["bid_html_con"] = contentHtml
            items["bid_content"] = content
            items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items["bid_source"] = author
            # print(
            #     items["bid_id"],
            #     items["bid_url"],
            #     items["bid_category"],
            #     items.get("bid_info_type", None),
            #     items["bid_name"],
            #     items["bid_source"],
            #     items["bid_public_time"],
            # )
            yield items
