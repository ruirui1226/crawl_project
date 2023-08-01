#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/12 09:00:00
# @Author  : xm
# @File    : sd_gov_ccgp.py
# @Description : 中国山东政府采购网

import time

import requests
from bs4 import BeautifulSoup

from untils.common import get_md5
from untils.pysql import MysqlPipelinePublic
from untils.redis_conn import r


class get_cg_InfoSpider:
    def __init__(self):
        self.url = "http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?grade=province&colcode=0301"
        self.webUrl = "http://www.ccgp-shandong.gov.cn/"
        self.webName = "中国山东政府采购网"
        self.url_f = "http://www.ccgp-shandong.gov.cn/sdgp2017/site/"
        self.s = requests.Session()
        self.tableName = "t_zx_po_crawl_info"
        self.REDISNAME = "shandongcgwqc"

    def info2sql(self, infos):
        if infos:
            contentId = get_md5(infos["bid_url"])
            ##redis 去重
            if r.hsetnx(self.REDISNAME, contentId, "") == 0:
                return
            ##存储到sql
            mql = MysqlPipelinePublic()
            mql.insert_sql(self.tableName, infos)
            mql.close()

    def dealInfo(self, response, listHref, listName):
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
            ##获取详情页信息
            contentRes = self.s.get(content_url)
            ## 发布时间
            contentSoup = BeautifulSoup(contentRes.text, "lxml")
            mideas = contentSoup.select("div.info_box midea")
            author = pubdatetime = None
            for midea in mideas:
                text = midea.text
                if "发布时间" in text:
                    pubdatetime = text[text.index("：") + len("：") :]
                elif "发布人" in text:
                    author = text[text.index("：") + len("：") :]
            contentHtml = str(contentSoup.select("div.content")[0]).replace("'", "’")
            contents = contentSoup.select("div.content *::text").extract()
            content = "".join(x.strip() for x in contents)
            itmes = {
                "website_url": self.webUrl,
                "website_name": self.webName,
                "po_category": listName,
                "bid_url": content_url,
                "bo_name": detail_title,
                "po_source": author,
                "po_html_con": contentHtml,
                "po_content": content,
                "po_public_time": pubdatetime,
                "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            self.info2sql(itmes)

    def main(self):
        list_res = self.s.get(self.url)
        listSoup = BeautifulSoup(list_res.text, "lxml")
        ass = listSoup.select("body > ul > li > a")
        if not ass:
            ass = listSoup.select("div.n_left  li> a")
        for a in ass:
            listHref = a.attrs["href"]
            listName = a.text
            if "grade=province=2500" in listHref:
                self.dealInfo(list_res, listHref, listName)
            else:
                listHref = self.url_f + listHref
                ##访问子列表
                contentListRes = self.s.get(listHref)
                self.dealInfo(contentListRes, listHref, listName)


if __name__ == "__main__":
    get_cg_InfoSpider().main()
