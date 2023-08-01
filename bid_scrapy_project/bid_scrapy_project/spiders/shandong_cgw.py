#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/3 16:02
# @Author  : xm
# @File    : shandong_cgw.py
# @Description : 中国山东政府采购网
import time

import scrapy
from bs4 import BeautifulSoup

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import GovernmentProcurementItem


class ShandongCgwSpider(scrapy.Spider):
    name = "shandong_cgw"

    def __init__(self):
        self.webUrl = "http://www.ccgp-shandong.gov.cn/"
        self.webName = "中国山东政府采购网"
        self.url_f = "http://www.ccgp-shandong.gov.cn/sdgp2017/site/"
        self.tableName = "t_zx_po_crawl_info"
        self.REDISNAME = "shandongcgwqc"

    def start_requests(self):
        url = "http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?grade=province&colcode=0301"
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        listSoup = BeautifulSoup(response.text, "lxml")
        ass = listSoup.select("body > ul > li > a")
        if not ass:
            ass = listSoup.select("div.n_left  li> a")
        for a in ass:
            listHref = a.attrs["href"]
            listName = a.text
            if "grade=province=2500" in listHref:
                yield self.dealInfo(response, listName)
            else:
                listHref = response.urljoin(listHref)
                ##访问子列表
                yield scrapy.Request(listHref, callback=self.apiUrlParse, meta={"listName": listName}, dont_filter=True)

    def apiUrlParse(self, response):
        return self.dealInfo(
            response, response.meta["listName"], response.meta.get("page"), response.meta.get("colcode")
        )

    def dealInfo(self, response, listName, curpage=1, colcode=None):
        contentListSoup = BeautifulSoup(response.text, "lxml")
        lis = contentListSoup.select("div.subCont li")
        for li in lis:
            content_url = li.select("a")[0].attrs["href"]
            if str(content_url).startswith(r"/"):
                content_url = content_url[1:]
            content_url = self.webUrl + content_url
            # 列表页标题
            content_title = li.select("a")[0].text
            ##文章页标题
            detail_title = li.select("a")[0].attrs["title"]
            ##列表页时间
            content_data = li.select("span.hits")[0].text
            items = {"title": detail_title, "listName": listName}
            ##获取详情页信息
            yield scrapy.Request(content_url, callback=self.getContent, meta={"items": items})
        # 获取页数  第二页之后就是post的
        if curpage == None:
            curpage = 1
        nextpage = curpage + 1
        if nextpage > 3:
            return
        if not colcode:
            colcode = response.request.url[response.request.url.index("colcode=") + len("colcode=") :]
        nextApi = "http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp"
        payload_dict = {
            "subject": "",
            "pdate": "",
            "kindof": "",
            "unitname": "",
            "projectname": "",
            "projectcode": "",
            "colcode": colcode,
            "curpage": str(nextpage),
            "grade": "province",
            "region": "",
            "firstpage": "1",
        }

        yield scrapy.FormRequest(
            url=nextApi,
            formdata=payload_dict,
            callback=self.apiUrlParse,
            meta={"page": nextpage, "listName": listName, "colcode": colcode},dont_filter=True
        )

    def getContent(self, response):
        items_info = response.meta["items"]
        ## 发布时间
        contentSoup = BeautifulSoup(response.text, "lxml")
        mideas = contentSoup.select("div.info_box midea")
        author = pubdatetime = None
        for midea in mideas:
            text = midea.text
            if "发布时间" in text:
                pubdatetime = text[text.index("：") + len("：") :]
            elif "发布人" in text:
                author = text[text.index("：") + len("：") :]
        #'2023年6月29日11时17分'
        pubdate_time = None
        try:
            pubdate_time = self.dateFormatString(pubdatetime, "%Y年%m月%d日%H时%M分")
        except:
            pass
        if not pubdate_time:
            try:
                pubdate_time = self.dateFormatString(pubdatetime, "%Y年%m月%d日 %H时%M分%S秒")
            except:
                pass
        if not pubdate_time:
            try:
                pubdate_time = self.dateFormatString(pubdatetime, "%Y年%m月%d日")
            except:
                pass
        if not pubdate_time:
            print(response.request.url, "没有获取到正确的时间")
            return
        contentHtml = str(contentSoup.select("div.content")[0]).replace("'", "’")
        content = contentSoup.select("div.content")[0].text.strip()
        itmes = {
            "po_id": get_md5(response.request.url),
            "website_url": self.webUrl,
            "website_name": self.webName,
            "po_category": "政府采购",
            "po_info_type": items_info["listName"],
            "bid_url": response.request.url,
            "bo_name": items_info.get("title"),
            "po_source": author,
            "po_html_con": contentHtml,
            "po_content": content,
            "po_public_time": pubdate_time,
            "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            "po_province": "山东省",
        }
        itmes_po = GovernmentProcurementItem()
        itmes_po.update(itmes)
        # print(itmes)
        yield itmes_po
    def dateFormatString(self, timestamp, timeType):
        """
        自定义的时间格式转换
        时间用指定格式显示,比如 年-月-日 转 年/月/日
        """
        # dt = "2020-10-10 22:20:20"
        # 转为数组
        # "%Y-%m-%d %H:%M:%S"
        timeArray = time.strptime(timestamp, timeType)
        # 转为其它显示格式
        customTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # print(customTime)  # 2020/10/10 22:20:20
        return customTime