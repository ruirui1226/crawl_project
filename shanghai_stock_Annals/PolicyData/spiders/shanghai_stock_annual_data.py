# -*- coding: utf-8 -*-
"""
@desc: 上交所-年报
@version: python3
@author: shenr
@time: 2023/04/19
"""
import datetime
import json
import logging
import re
import datetime
import sys

import pymysql
from pymysql import IntegrityError
from redis import Redis
import scrapy

from shanghai_stock_Annals.PolicyData.items import ShanghaiStorkExchangeItem
from shanghai_stock_Annals.PolicyData.settings import *

logger = logging.getLogger(__name__)

conn = Redis(host="10.67.78.131", port=6379, password="qwer1234", db=1, encoding="utf-8")


def get_time():
    time_now = datetime.datetime.now().strftime("%Y-%m-%d")
    time_yest = datetime.date.today() + datetime.timedelta(-1)

    # return "2023-04-26", "2023-05-19"
    return time_yest, time_now


def get_week():
    con = None
    try:
        con = pymysql.connect(
            database="list_company_annual_report",
            user="root",
            port=3306,
            password="hsd#H&hdj6sd",
            host="10.67.78.125",
        )
        cur = con.cursor()
        cur.execute("""SELECT * FROM week_data where shanghai_zt = '0' order by start_time limit 1""")
        code = cur.fetchall()
        print("pppppppp", code)
        return code[0]
        # return ('2023-02-15', '2023-02-21', '1', '0')

    except IntegrityError as e:
        print(f"Error {e}")
        sys.exit(1)

    finally:
        if con:
            con.close()


def upd_week(www):
    con = None
    try:
        con = pymysql.connect(
            database="list_company_annual_report",
            user="root",
            password="hsd#H&hdj6sd",
            port=3306,
            host="10.67.78.125",
        )
        cur = con.cursor()
        cur.execute(
            f"""
                update week_data
                set shanghai_zt = '1'
                where start_time = '{www}'
        """
        )
        con.commit()

    except IntegrityError as e:
        print(f"Error {e}")
        sys.exit(1)


def ret_data(item, rows):
    URL = "http://www.sse.com.cn" + rows["URL"]
    item["spider_name"] = "shanghai_stock_exchange_annual_report"
    item["bulletin_type_desc"] = rows.get("BULLETIN_TYPE_DESC", "")
    item["bulletin_year"] = rows.get("BULLETIN_YEAR", "")
    item["is_holder_disclose"] = rows.get("IS_HOLDER_DISCLOSE", "")
    item["org_bulletin_id"] = rows.get("ORG_BULLETIN_ID", "")
    item["org_file_type"] = rows.get("ORG_FILE_TYPE", "")
    item["security_code"] = rows.get("SECURITY_CODE", "")
    item["security_name"] = rows.get("SECURITY_NAME", "")
    item["ssedate"] = rows.get("SSEDATE", "")
    item["title"] = rows.get("TITLE", "")
    item["pdf_url"] = URL
    item["creat_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return item


class QingdaoDataSpider(scrapy.Spider):
    name = "shanghai_stock_exchange_annual_report"
    allowed_domains = ["http://www.sse.com.cn/disclosure/listedinfo/announcement/"]
    time_ = get_week()
    # start_urls = f"http://query.sse.com.cn/security/stock/queryCompanyBulletinNew.do?jsonCallBack=jsonpCallback25327794&isPagination=true&pageHelp.pageSize=25&pageHelp.cacheSize=1&START_DATE={time_[0]}&END_DATE={time_[1]}&SECURITY_CODE=&TITLE=&BULLETIN_TYPE=0101&stockType=&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.endPage=1&_=1684462399567"
    start_urls = "http://query.sse.com.cn/security/stock/queryCompanyBulletinNew.do?jsonCallBack=jsonpCallback13700697&isPagination=true&pageHelp.pageSize=25&pageHelp.cacheSize=1&START_DATE={}&END_DATE={}&SECURITY_CODE=&TITLE=&BULLETIN_TYPE=0101&stockType=&pageHelp.pageNo={}&pageHelp.beginPage={}&pageHelp.endPage={}&_=1685585792482"

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        # 'Cookie': 'ba17301551dcbaf9_gdp_user_key=; gdp_user_id=gioenc-74g7e382,e9d9,5616,9da3,1gbed3g90a35; ba17301551dcbaf9_gdp_session_id_6ca48cf8-d3ec-4962-a04f-fab212f03348=true; ba17301551dcbaf9_gdp_session_id_3209ced0-bd84-4768-824c-095bb6a13bbd=true; ba17301551dcbaf9_gdp_session_id_97c1c403-729a-4289-9c68-3f2a5a2fc340=true; ba17301551dcbaf9_gdp_session_id_4c2ae7d5-2c9b-44d2-9c2c-80df8884e1d6=true; ba17301551dcbaf9_gdp_session_id_2c6f94b5-5a0f-4fb3-ab63-5a350d3526c6=true; ba17301551dcbaf9_gdp_session_id_9e197abc-1150-4bf8-a8f0-d549bba371ae=true; ba17301551dcbaf9_gdp_session_id_35b993ac-7fc0-4035-a153-6f2f65c337d0=true; ba17301551dcbaf9_gdp_session_id_7c53c919-d7ee-4923-b084-48dc1eaecd4b=true; ba17301551dcbaf9_gdp_session_id_26d455bb-f344-41c5-a53a-2b6d131c0867=true; ba17301551dcbaf9_gdp_session_id_fc6d0532-d332-4cbe-9408-b25248b5d925=true; ba17301551dcbaf9_gdp_session_id_cf2cccfa-723a-47e9-bc78-b3b28dde583e=true; JSESSIONID=A56F9D2BC118473A0956623967948C78; ba17301551dcbaf9_gdp_session_id=10aee09e-ccc2-4b21-a7d1-2b8be309bdf9; ba17301551dcbaf9_gdp_session_id_10aee09e-ccc2-4b21-a7d1-2b8be309bdf9=true; ba17301551dcbaf9_gdp_sequence_ids={"globalKey":404,"VISIT":11,"PAGE":36,"VIEW_CLICK":276,"CUSTOM":79,"VIEW_CHANGE":7}',
        "Referer": "http://www.sse.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }

    data = {
        "jsonCallBack": "jsonpCallback1365070",
        "isPagination": "true",
        "pageHelp.pageSize": "25",
        "pageHelp.cacheSize": "1",
        "START_DATE": "2023-01-20",
        "END_DATE": "2023-04-20",
        "SECURITY_CODE": "",
        "TITLE": "",
        "BULLETIN_TYPE": "0101",
        "stockType": "",
        "pageHelp.pageNo": "1",
        "pageHelp.beginPage": "1",
        "pageHelp.endPage": "1",
        "_": "1681960376532",
    }

    def get_redis_val(self, redis_key):
        """
        获取缓存数据
        :param redis_key:
        :return:
        """
        data_value = conn.get(str(redis_key))
        if not data_value:
            return {"next_page": 1, "page_count": 1, "all_data": []}
        data_value = json.loads(data_value)
        return {
            "next_page": int(data_value["next_page"]) + 1,
            "pagecount": int(data_value["page_count"]),
            "all_data": data_value["all_data"],
        }

    def set_redis_val(self, redis_key, next_page, page_count, new_data):
        """
        设置缓存数据
        :param redis_key:
        :param next_page:
        :param new_data:
        :return:
        """
        old_val = self.get_redis_val(str(redis_key))
        all_data = old_val["all_data"]
        all_data = all_data + new_data
        data_value = {"next_page": int(next_page), "page_count": page_count, "all_data": all_data}
        conn.set(str(redis_key), json.dumps(data_value))
        conn.expire(str(redis_key), 60 * 60)

    def start_requests(self):
        cache_val = self.get_redis_val(self.time_[0])
        # print("redis======", cache_val)
        next_page = cache_val.get("next_page")
        page_count = cache_val.get("page_count")
        yield scrapy.FormRequest(
            url=self.start_urls.format(self.time_[0], self.time_[1], next_page, next_page, next_page),
            headers=self.headers,
            # body=json.dumps(self.data),
            callback=self.parse_1,
            meta={"next_page": next_page, "page_count": page_count},
            dont_filter=True,
            method="POST",
        )

    def parse_1(self, response, **kwargs):
        meta = response.meta
        next_page = meta["next_page"]
        page_count = meta["page_count"]
        print("45646546456", page_count)
        print(f"=========当前爬取第{next_page}页==========")
        doc = response.text
        re_data = re.findall("\(\{(.*?)\}\)", str(doc), re.S)[0]
        print(response.url)
        re_data = "{" + re_data + "}"
        load_data = json.loads(re_data)
        pageHelp = load_data.get("pageHelp")

        if page_count:
            if next_page - 1 == page_count:
                cache_val = self.get_redis_val(self.time_[0])
                all_data = cache_val["all_data"]
                for each in all_data:
                    item_y = ShanghaiStorkExchangeItem()
                    item_y["spider_name"] = "shanghai_stock_exchange_annual_report"
                    item_y["bulletin_type_desc"] = each.get("bulletin_type_desc", "")
                    item_y["bulletin_year"] = each.get("bulletin_year", "")
                    item_y["is_holder_disclose"] = each.get("is_holder_disclose", "")
                    item_y["org_bulletin_id"] = each.get("org_bulletin_id", "")
                    item_y["org_file_type"] = each.get("org_file_type", "")
                    item_y["security_code"] = each.get("security_code", "")
                    item_y["security_name"] = each.get("security_name", "")
                    item_y["ssedate"] = each.get("ssedate", "")
                    item_y["title"] = each.get("title", "")
                    item_y["pdf_url"] = each.get("pdf_url")
                    item_y["creat_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print("========", item_y)
                    yield item_y
                upd_week(self.time_[0])
                print("==================爬取结束=====================")
            else:
                pagecount = pageHelp.get("pageCount")
                page_count = int(pagecount)
                print("总页数+++++", page_count)
                data = pageHelp.get("data")
                items = []
                for each in data:
                    for rows in each:
                        item_r = {}
                        item = ret_data(item_r, rows)
                        items.append(item)
                self.set_redis_val(self.time_[0], next_page, page_count, items)

                next_page += 1
                yield scrapy.FormRequest(
                    # url=f"http://query.sse.com.cn/security/stock/queryCompanyBulletinNew.do?jsonCallBack=jsonpCallback13700697&isPagination=true&pageHelp.pageSize=25&pageHelp.cacheSize=1&START_DATE={self.time_[0]}&END_DATE={self.time_[1]}&SECURITY_CODE=&TITLE=&BULLETIN_TYPE=0101&stockType=&pageHelp.pageNo={next_page}&pageHelp.beginPage={next_page}&pageHelp.endPage={next_page}&_=1685585792488",
                    url=f"http://query.sse.com.cn/security/stock/queryCompanyBulletinNew.do?jsonCallBack=jsonpCallback88734151&isPagination=true&pageHelp.pageSize=25&pageHelp.cacheSize=1&START_DATE={self.time_[0]}&END_DATE={self.time_[1]}&SECURITY_CODE=&TITLE=&BULLETIN_TYPE=0101&stockType=&pageHelp.pageNo={next_page}&pageHelp.beginPage={next_page}&pageHelp.endPage={next_page}&_=1685585792488",
                    headers=self.headers,
                    # body=json.dumps(self.data),
                    callback=self.parse_1,
                    meta={"next_page": next_page, "page_count": page_count},
                    dont_filter=True,
                    method="POST",
                )
        else:
            upd_week(self.time_[0])
