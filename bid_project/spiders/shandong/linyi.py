#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/6/7 9:49
@Author : zhangpf
@File : linyi.py
@Desc : 临沂市
@Software: PyCharm
"""
import math
import re
import time

from loguru import logger
from pyquery import PyQuery as pq
import requests
from bid_project.untils.common import get_md5
from bid_project.untils.pysql import MysqlPipelinePublic

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Referer": "http://ggzyjy.linyi.gov.cn/linyi/jyxx/jylist.html?categoryNum=012&pageIndex=4791",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}


def list_page():
    """列表页"""
    response = requests.get("http://ggzyjy.linyi.gov.cn/linyi/jyxx/jylist.html", headers=headers, verify=False).text
    total = re.findall("total: (.*?),", str(response), re.S)[0]
    totals = math.ceil(int(total) / 15)
    for i in range(2, totals + 1):
        response = requests.get(f"http://ggzyjy.linyi.gov.cn/linyi/jyxx/{i}.html", headers=headers, verify=False).text
        detail_list(response)
        break


def detail_list(response):
    """获取列表页中的每一个"""
    res_t = pq(response)
    for url in res_t('ul[class="news-items"] li a').items():
        detail_url = url.attr("href")
        details_page(detail_url)


def details_page(detail_url):
    """详情页"""
    logger.warning("当前url={}".format("http://ggzyjy.linyi.gov.cn" + detail_url))
    response = requests.get("http://ggzyjy.linyi.gov.cn" + detail_url, headers=headers, verify=False).text
    parse_page(response,detail_url)


def parse_page(response,detail_url):
    """解析详情页"""
    res_t = pq(response)
    bid_name = res_t('div[class="ewb-article"] h3').text()
    bid_html_con = str(res_t('div[class="ewb-article-info"]').outer_html()).replace("'",'"')
    bid_source = res_t('div[class="ewb-article-sources"] p').eq(3).text()
    bid_category = res_t('div[class="ewb-location"] a').eq(2).text()
    bid_info_type = res_t('span[id="viewGuid"]').text()
    pre = re.compile('>(.*?)<')
    bid_content = ''.join(pre.findall(str(bid_html_con)))
    information_time = res_t('div[class="ewb-article-sources"] p').eq(0).text().split("：")[-1].split("】")[0]
    item = {
        "bid_id": get_md5(str(detail_url).split("/")[-1].split(".")[0]),
        "bid_md5_url": get_md5("http://ggzyjy.linyi.gov.cn" + detail_url),
        "bid_city": "临沂市",
        "bid_county": "",
        "bid_url": "http://ggzyjy.linyi.gov.cn" + detail_url,
        "bid_category": bid_category,
        "bid_info_type": bid_info_type,
        "bid_source": bid_source,
        "bid_html_con": bid_html_con,
        "bid_content": bid_content,
        "bid_name": bid_name,
        "bid_public_time": information_time,
        "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
    }
    print(item)
    mq = MysqlPipelinePublic()
    mq.insert_sql("t_zx_bid_crawl_info", item)


if __name__ == "__main__":
    list_page()
