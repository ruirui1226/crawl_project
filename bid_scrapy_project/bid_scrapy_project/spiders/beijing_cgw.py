# -*- coding: utf-8 -*-
"""
@desc: 北京市政府采购网
@version: python3
@author: xm
@time: 2023/06/15
"""
import datetime
import re
import time

import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import GovernmentProcurementItem


class BeijingCgwSpider(scrapy.Spider):
    """
    北京市政府采购网
    """

    name = "beijing_cgw"

    # allowed_domains = ['www.ccgp-beijing.gov.cn']
    # start_urls = ['http://www.ccgp-beijing.gov.cn/']
    def __init__(self):
        self.urlList = {
            "市级信息公告": {
                "招标公告": "http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjzbgg/index.html",
                "中标公告": "http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjzbjggg/index.html",
                "合同公告": "http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjhtgg/index.html",
                "更正公告": "http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjgzgg/index.html",
                "废标公告": "http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjfbgg/index.html",
                "单一公告": "http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjdygg/index.html",
                "其他公告": "http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjqtgg/index.html",
                "集采成交": "http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjjcjl/index.html",
            },
            "区级信息公告": {
                "招标公告": "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjzbgg/index.html",
                "中标公告": "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjzbjggg/index.html",
                "合同公告": "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjhtgg/index.html",
                "更正公告": "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjgzgg/index.html",
                "废标公告": "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjfbgg/index.html",
                "单一公告": "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjdygg/index.html",
                "其他公告": "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjqtgg/index.html",
                "集采成交": "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjjcjl/index.html",
            },
        }

    def start_requests(self):
        for i, v in self.urlList.items():
            po_category = i  # 大类型  备用
            for x, y in v.items():
                po_info_type = x  # 小类型  备用
                for page in range(0, 4):
                    url = y if page == 0 else y.replace("index.html", "index_{}.html".format(page))
                    yield scrapy.Request(
                        url,
                        callback=self.parse,
                        meta={"po_category": po_category, "po_info_type": po_info_type},
                        dont_filter=True,
                    )

    def parse(self, response):
        """
        列表页处理
        """
        lis = response.css("div.inner-l-i > ul > li")
        for li in lis:
            href = li.css("a::attr(href)").get()
            href = response.urljoin(href)
            title = li.css("a::text").get()  ##备用 优先存储详情页title
            pubdate = li.css("span::text").get()  ###此时间用来备用当详情页没有时间的时候存储此时间
            meta = {"title": title, "pubdate": pubdate}
            meta.update(response.meta)
            yield scrapy.Request(href, callback=self.contentParse, meta=meta)

    def contentParse(self, response):
        """
        详情页处理  此 无 来源
        """
        title = response.css("div.xl-box-header  p::text").get()
        pubtime = response.css("div.xl-box-header > div > span::text").get()
        if not pubtime:
            pubtime = response.meta["pubdate"]
        if not ":" in pubtime:
            if re.match("\s*(\d+)-(\d+)-(\d+)$", pubtime):  # 2018-12-17
                datas = "{0} {1}:{2}:{3}".format(pubtime, self.hours, self.minutes, self.seconds)
                dt = datetime.datetime.strptime(datas, "%Y-%m-%d %H:%M:%S")
                utc_dt = dt - datetime.timedelta()
                if isinstance(utc_dt, datetime.datetime):
                    pubtime = str(utc_dt.strftime("%Y-%m-%d %H:%M:%S"))
        content_html = str(response.css("div#mainText").get()).replace("'", "’").strip()
        contents = response.css("div#mainText *::text").extract()
        content = "".join(x.strip() for x in contents)
        contentUrl = response.request.url
        items = GovernmentProcurementItem(
            po_city="北京市",
            website_name="北京市政府采购网",
            website_url="https://ggzyfw.beijing.gov.cn/",
            po_province="北京",
            po_category="政府采购",
        )
        items["po_id"] = get_md5(contentUrl)
        items["bid_url"] = contentUrl
        items["po_public_time"] = pubtime
        items["po_html_con"] = content_html
        items["po_content"] = content
        items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # items["po_category"] = response.meta["po_category"]
        items["po_info_type"] = response.meta["po_info_type"]
        items["bo_name"] = title
        # print(items["po_id"], items["bid_url"], items["po_category"], items.get("po_info_type", None))
        yield items

    @property
    def hours(self):
        hours = str(datetime.datetime.now().hour)
        if len(hours) == 1:
            hours = "0" + hours
            return hours
        return hours

    @property
    def minutes(self):
        minutes = str(datetime.datetime.now().minute)
        if len(minutes) == 1:
            minutes = "0" + minutes
            return minutes
        return minutes

    @property
    def seconds(self):
        seconds = str(datetime.datetime.now().second)
        if len(seconds) == 1:
            seconds = "0" + seconds
            return seconds
        return seconds
