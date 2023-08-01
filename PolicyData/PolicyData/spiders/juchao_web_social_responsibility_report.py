# -*- coding: utf-8 -*-

"""
@desc: 巨潮资讯-web-社会责任报告
@version: python3
@author: shenr
@time: 2023/04/27
"""
import datetime
import json
import time
import sys
import psycopg2
import scrapy

from loguru import logger

from ..items import JuchaoWebSocialResponsibilityData


# logger = logging.getLogger(__name__)


def getCode():
    # 将con初始化为None 如果无法创建与数据库的连接(例如磁盘已满) 则不会定义连接变量 将导致 finally 子句中的错误
    con = None
    try:
        con = psycopg2.connect(
            database="list_company_annual_report",
            user="postgres",
            password="postgres",
            host="10.67.78.125",
        )
        cur = con.cursor()
        cur.execute(
            """
        select code, zwjc from public.t_zx_list_company_name_info a
        where a.code not in (select seccode from public.juchao_web_social_responsibility_report) 
        and a.category = 'A股' order by a.code limit 10
        """
        )
        code = cur.fetchall()
        print(code)
        return code

    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
        sys.exit(1)

    finally:
        if con:
            con.close()


def table_data(table):
    """
    :param table: 原网页数据
    :return: item
    """
    item = JuchaoWebSocialResponsibilityData()
    item["spider_name"] = "juchao_web_social_responsibility_report"
    item["id"] = table.get("id")
    item["seccode"] = table.get("secCode")
    item["secname"] = table.get("secName")
    item["orgid"] = table.get("orgId")
    item["announcementid"] = table.get("announcementId")
    item["announcementtitle"] = table.get("announcementTitle")
    item["announcementtime"] = table.get("announcementTime")
    item["adjuncturl"] = table.get("adjunctUrl")
    item["adjunctsize"] = table.get("adjunctSize")
    item["adjuncttype"] = table.get("adjunctType")
    item["storagetime"] = table.get("storageTime")
    item["columnid"] = table.get("columnId")
    item["pagecolumn"] = table.get("pageColumn")
    item["announcementtype"] = table.get("announcementType")
    item["associateannouncement"] = table.get("associateAnnouncement")
    item["important"] = table.get("important")
    item["batchnum"] = table.get("batchNum")
    item["announcementcontent"] = table.get("announcementContent")
    item["orgname"] = table.get("orgName")
    item["tilesecname"] = table.get("tileSecName")
    item["shorttitle"] = table.get("shortTitle")
    item["announcementtypename"] = table.get("announcementTypeName")
    item["secnamelist"] = table.get("secNameList")
    item["pdf_url"] = (
        "http://static.cninfo.com.cn/" + table.get("adjunctUrl") if table.get("adjunctUrl") else table.get("pdf_url")
    )
    item["creat_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return item


class Spider(scrapy.Spider):
    name = "juchao_web_social_responsibility_report"
    allowed_domains = [
        "http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=000001+%E7%A4%BE%E4%BC%9A%E8%B4%A3%E4%BB%BB%E6%8A%A5%E5%91%8A&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum=2&type="
    ]
    start_urls = "http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=000001+%E7%A4%BE%E4%BC%9A%E8%B4%A3%E4%BB%BB%E6%8A%A5%E5%91%8A&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum=2&type="
    # page = 1
    code_list = getCode()

    def start_requests(self):
        # print(f"当前爬取==={self.page}===")
        for code in self.code_list:
            time.sleep(1)
            page = 1
            yield scrapy.Request(
                url=f"http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey={code[0]}+%E7%A4%BE%E4%BC%9A%E8%B4%A3%E4%BB%BB%E6%8A%A5%E5%91%8A&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum=1&type=",
                callback=self.parse_1,
                dont_filter=True,
                meta={"seccode": code[0], "secname": code[1], "page": page},
            )

    def parse_1(self, response, **kwargs):
        time.sleep(3)
        seccode = response.meta.get("seccode")
        secname = response.meta.get("secname")
        page = response.meta.get("page")
        doc_ = json.loads(response.text)
        logger.info(f"text******{response.text}******")
        logger.info(f"状态*******{response}******")
        doc = doc_.get("announcements")
        totalrecordnum = doc_.get("totalRecordNum")

        if response.status != 200:
            table = {}
            table["spider_name"] = "juchao_web_social_responsibility_report"
            table["id"] = "未访问成功"
            table["secCode"] = seccode
            table["secName"] = secname
            table["pdf_url"] = seccode
            item = table_data(table)
            # yield item
        else:
            if str(totalrecordnum) == "0":
                logger.info(seccode)
                table = {}
                table["spider_name"] = "juchao_web_social_responsibility_report"
                table["id"] = "无数据"
                table["secCode"] = seccode
                table["secName"] = secname
                table["pdf_url"] = seccode
                item = table_data(table)
                # yield item
                logger.info("================爬取结束================")
            else:
                logger.info(f"当前爬取========={seccode},第{page}页========")
                for each in doc:
                    item = table_data(each)
                    logger.info(item)
                    # yield item
                if totalrecordnum/10 > page:
                    page += 1
                    yield scrapy.Request(
                        url=f"http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey={seccode}+%E7%A4%BE%E4%BC%9A%E8%B4%A3%E4%BB%BB%E6%8A%A5%E5%91%8A&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum={page}&type=",
                        callback=self.parse_1,
                        meta={"seccode": seccode, "secname": secname, "page": page},
                        dont_filter=True,
                    )
