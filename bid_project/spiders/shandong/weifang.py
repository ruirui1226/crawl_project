#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/6/9 14:12
@Author : zhangpf
@File : weifang.py
@Desc : 潍坊市
@Software: PyCharm
"""
import re
import time

import requests
from loguru import logger
from pyquery import PyQuery as pq

from untils.common import get_md5
from untils.pysql import MysqlPipelinePublic

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "ASP.NET_SessionId=12blwgtnrd3ekonokttjbuf5",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}


def level_list():
    response = requests.get("http://ggzy.weifang.gov.cn/wfggzy/xmxx/", headers=headers, verify=False).text
    res = pq(response)
    for url in res('div[class="column-bd"] li a').items():
        url = url.attr("href")
        response = requests.get("http://ggzy.weifang.gov.cn" + url, headers=headers, verify=False).text
        res = pq(response)
        for url in res('div[class="s-block"] h4 a').items():
            url = url.attr("href")
            categorynum = str(url).split("/")[-1]
            list_page(categorynum)
            break
        break


def list_page(categorynum):
    response = requests.get(
        f"http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_jh.aspx?address=&type=&categorynum={categorynum}",
        headers=headers,
        verify=False,
    ).text
    res = pq(response)
    total = res('td[class="huifont"]').text().split("/")[-1]
    for i in range(1, int(total) + 1):
        response = requests.get(
            f"http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_jh.aspx?address=&type=&categorynum={categorynum}&Paging={i}",
            headers=headers,
            verify=False,
        ).text
        res = pq(response)

        for details_url in res('span[class="info-name"] a').items():
            detail_url = details_url.attr("href")
            detail_page(detail_url)


def detail_page(detail_url):
    response = requests.get(
        "http://ggzy.weifang.gov.cn" + detail_url,
        headers=headers,
        verify=False,
    ).text
    logger.warning("当前url={}".format("http://ggzy.weifang.gov.cn" + detail_url))
    res = pq(response)
    bid_name = res('h3[class="bigtitle"]').text()
    bid_html_con = str(res('div[class="substance"]').outer_html()).replace("'", '"')
    pre = re.compile(">(.*?)<")
    bid_content = "".join(pre.findall(str(bid_html_con)))
    bid_county = res('div[class="location"] span').text()
    # bid_source = res('p[class="sub-cp"]').text()
    bid_category = res('div[class="location"] a').eq(4).text()
    bid_info_type = res('div[class="location"] a').eq(3).text()
    information_time = str(res('p[class="sub-cp"]').text()).split("：")[2].split(" ")[0]

    item = {
        "bid_id": get_md5(str(detail_url).split("/")[-1].split(".")[0]),
        "bid_md5_url": get_md5("http://ggzy.weifang.gov.cn" + detail_url),
        "bid_city": "潍坊市",
        "bid_county": bid_county,
        "bid_url": "http://ggzy.weifang.gov.cn" + detail_url,
        "bid_category": bid_category,
        "bid_info_type": bid_info_type,
        "bid_source": "",
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
    level_list()
