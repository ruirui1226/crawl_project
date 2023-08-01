# -*- coding: utf-8 -*-
"""
@desc: 巨潮-财务数据
@version: python3
@author: shenr
@time: 2023/04/26
"""
import base64
import datetime
import json
import sys
import time

import psycopg2
from loguru import logger
import scrapy
from ..items import JuchaoWebCaiwuData


def getcode():
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
            where a.code not in (select code from public.juchao_web_caiwu_data) 
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
    item = JuchaoWebCaiwuData()
    item["spider_name"] = "juchao_web_caiwu_data"
    item["enddate"] = table.get("ENDDATE")
    item["f004n"] = table.get("F004N")
    item["f008n"] = table.get("F008N")
    item["f010n"] = table.get("F010N")
    item["f011n"] = table.get("F011N")
    item["f016n"] = table.get("F016N")
    item["f017n"] = table.get("F017N")
    item["f022n"] = table.get("F022N")
    item["f023n"] = table.get("F023N")
    item["f025n"] = table.get("F025N")
    item["f026n"] = table.get("F026N")
    item["f029n"] = table.get("F029N")
    item["f041n"] = table.get("F041N")
    item["f042n"] = table.get("F042N")
    item["f043n"] = table.get("F043N")
    item["f052n"] = table.get("F052N")
    item["f053n"] = table.get("F053N")
    item["f054n"] = table.get("F054N")
    item["f056n"] = table.get("F056N")
    item["f058n"] = table.get("F058N")
    item["f067n"] = table.get("F067N")
    item["f078n"] = table.get("F078N")
    item["code"] = table.get("code")
    item["company"] = table.get("company")
    item["creat_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item["unique_id"] = item["company"] + "_" + item["enddate"]
    return item


class QingdaoDataSpider(scrapy.Spider):
    name = "juchao_web_caiwu_data"
    allowed_domains = ["http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1140?scode=000005&sign=1&rtype=2"]
    start_urls = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1140?scode=000001&sign=1&rtype=1"

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        # 'Content-Length': '0',
        # 'Cookie': 'Hm_lvt_489bd07e99fbfc5f12cbb4145adb0a9b=1682303781,1682305527,1682411173,1682474017; Hm_lpvt_489bd07e99fbfc5f12cbb4145adb0a9b=1682479846; JSESSIONID=2E0E4303A2A0100B2E059775255227EB',
        "Origin": "http://webapi.cninfo.com.cn",
        "Referer": "http://webapi.cninfo.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "mcode": base64.b64encode(str(int(time.time())).encode()),
    }

    sql_data = getcode()

    def start_requests(self):
        for each in self.sql_data:
            type_ = 1
            yield scrapy.FormRequest(
                url=f"http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1140?scode={each[0]}&sign=1&rtype=1",
                # url=self.start_urls,
                callback=self.parse_1,
                headers=self.headers,
                dont_filter=True,
                meta={"code": each[0], "company": each[1], "type_": type_},
                method="POST",
            )

    def parse_1(self, response, **kwargs):
        meta = response.meta
        code = meta.get("code")
        company = meta.get("company")
        type_ = meta.get("type_")
        logger.info(f"=========当前爬取{company}的第{type_}页==========")
        doc = json.loads(response.text)
        records = doc.get("records")
        if not records:
            if str(doc.get("resultcode")) != "200":
                records = [{"ENDDATE": "未访问成功", "code": code, "company": company}]
            else:
                records = [{"ENDDATE": "无数据", "code": code, "company": company}]
        for table in records:
            table["code"] = code
            table["company"] = company
            item = table_data(table)
            print(item)
            # yield item

        type_ += 1
        if type_ == 5:
            logger.info("============爬取结束============")
        else:
            yield scrapy.FormRequest(
                url=f"https://webapi.cninfo.com.cn/api/sysapi/p_sysapi1140?scode={code}&sign=1&rtype={type_}",
                callback=self.parse_1,
                headers=self.headers,
                dont_filter=True,
                meta={
                    "code": code,
                    "company": company,
                    "type_": type_,
                },
                method="POST",
            )
