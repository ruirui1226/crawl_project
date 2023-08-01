# -*- coding: utf-8 -*-

"""
@desc: 巨潮资讯-app-年报
@version: python3
@author: shenr
@time: 2023/04/24
"""

import datetime
import json
import sys
import time
import psycopg2
import scrapy
from loguru import logger
# from JsonStorage import create_json
from ..items import JuchaoAppAnnualItem

# logger = logging.getLogger(__name__)


def get_week():
    con = None
    try:
        con = psycopg2.connect(
            database="list_company_annual_report",
            user="postgres",
            password="hsd#H&hdj6sd",
            host="10.67.78.125",
        )
        cur = con.cursor()
        cur.execute("""SELECT * FROM week_data where zt = '0' order by start_time limit 1""")
        code = cur.fetchall()
        print(code)
        return code

    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
        sys.exit(1)

    finally:
        if con:
            con.close()


def upd_week(www):
    con = None
    try:
        con = psycopg2.connect(
            database="list_company_annual_report",
            user="postgres",
            password="hsd#H&hdj6sd",
            host="10.67.78.125",
        )
        cur = con.cursor()
        cur.execute(
            f"""
                update week_data
                set zt = '1'
                where start_time = '{www}'
        """
        )
        con.commit()

    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
        sys.exit(1)

    finally:
        if con:
            con.close()


class Spider(scrapy.Spider):
    name = "juchao_annual_data"
    allowed_domains = ["https://www-s.cninfo.com.cn/new/fulltextSearch/fullApp?pageNum=1&pageSize=30&tabName=fulltext&sDate=2021-04-24&eDate=2023-04-24&sortName=pubdate&sortType=desc&isHLtitle=true&column=szse&category=category_ndbg_szsh"]
    start_urls = "https://www-s.cninfo.com.cn/new/fulltextSearch/fullApp?pageNum=1&pageSize=30&tabName=fulltext&sDate=2021-04-25&eDate=2023-04-25&sortName=pubdate&sortType=desc&isHLtitle=true&column=szse&category=category_ndbg_szsh"
    # page = 1
    week = get_week()

    headers = {
        "Cookie": "JSESSIONID=A3C41652093BD0A2F5D43A4683BF6258; routeId=.uc2; insert_cookie=45380249",
        "User-Agent": "okhttp/3.12.12"
    }
    data = {
        "pageNum": "100",
        "pageSize": "30",
        "tabName": "fulltext",
        "sDate": "2022-04-25",
        "eDate": "2023-04-25",
        "sortName": "pubdate",
        "sortType": "desc",
        "isHLtitle": "false",
        "column": "szse",
        "category": "category_ndbg_szsh"
        }

    def start_requests(self):
        for www in self.week:
            time.sleep(1)
            page = 1
            yield scrapy.Request(
                url=f"https://www-s.cninfo.com.cn/new/fulltextSearch/fullApp?pageNum={page}&pageSize=30&tabName=fulltext&sDate={www[0]}&eDate={www[1]}&sortName=pubdate&sortType=desc&isHLtitle=true&column=szse&category=category_ndbg_szsh",
                callback=self.parse_1,
                dont_filter=True,
                meta={"www": www,
                      "page": page}
            )

    def parse_1(self, response, **kwargs):
        time.sleep(0.5)
        www = response.meta.get("www")
        page = response.meta.get("page")
        doc_ = json.loads(response.text)
        # print("状态==========", response)
        doc = doc_.get("announcements")
        if not doc:
        # if self.page == 10:
            upd_week(www[0])
            logger.info("================爬取结束================")
        else:
            logger.info(f"当前爬取======={www},第{page}页========")
            for each in doc:
                item = JuchaoAppAnnualItem()
                item["spider_name"] = "juchao_annual_data"
                item["id"] = each.get("id")
                item["seccode"] = each.get("secCode")
                item["secname"] = each.get("secName")
                item["orgid"] = each.get("orgId")
                item["announcementid"] = each.get("announcementId")
                item["announcementtitle"] = each.get("announcementTitle")
                item["announcementtime"] = each.get("announcementTime")
                item["adjuncturl"] = each.get("adjunctUrl")
                item["adjunctsize"] = each.get("adjunctSize")
                item["adjuncttype"] = each.get("adjunctType")
                item["storagetime"] = each.get("storageTime")
                item["columnid"] = each.get("columnId")
                item["pagecolumn"] = each.get("pageColumn")
                item["announcementtype"] = each.get("announcementType")
                item["associateannouncement"] = each.get("associateAnnouncement")
                item["important"] = each.get("important")
                item["batchnum"] = each.get("batchNum")
                item["announcementcontent"] = each.get("announcementContent")
                item["orgname"] = each.get("orgName")
                item["tilesecname"] = each.get("tileSecName")
                item["shorttitle"] = each.get("shortTitle")
                item["announcementtypename"] = each.get("announcementTypeName")
                item["secnamelist"] = each.get("secNameList")
                item["pdf_url"] = "http://static.cninfo.com.cn/" + item["adjuncturl"]
                item["creat_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                logger.info(f"{item}")
                yield item
            # 本地存储json数据
            # json_data = doc_
            # name = str(www[0]) + "_" + str(page)
            # create_json(json_data, name, self.name)
            page += 1
            # self.data["pageNum"] = str(int(self.data["pageNum"]) + page)
            yield scrapy.Request(
                url=f"https://www-s.cninfo.com.cn/new/fulltextSearch/fullApp?pageNum={page}&pageSize=30&tabName=fulltext&sDate={www[0]}&eDate={www[1]}&sortName=pubdate&sortType=desc&isHLtitle=true&column=szse&category=category_ndbg_szsh",
                callback=self.parse_1,
                meta={"www": www,
                      "page": page},
                dont_filter=True,
            )

"https://www-s.cninfo.com.cn/new/fulltextSearch/fullApp?pageNum=1&pageSize=100&tabName=fulltext&sDate=2022-04-25&eDate=2022-05-01&sortName=pubdate&sortType=desc&isHLtitle=true&column=szse&category=category_ndbg_szsh"