#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/6/9 9:52
@Author : zhangpf
@File : heze.py
@Desc : 菏泽市
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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}


def list_page():
    response = requests.get('http://ggzy.heze.gov.cn/jyxx/about.html', headers=headers, verify=False).text
    res_t = pq(response)
    for url in res_t('ul[class="ewb-info-items"] li a').items():
        detail_url = url.attr("href")
        details_page(detail_url)
    # total = re.findall("total: (.*?),", str(response), re.S)[0]
    total = res_t('span[id="index"]').text().split("/")[1]
    print(total)
    # totals = math.ceil(int(total) / 15)
    for i in range(2, int(total) + 1):
        response = requests.get(f'http://ggzy.heze.gov.cn/jyxx/{i}.html', headers=headers, verify=False).text
        res_t = pq(response)
        for url in res_t('ul[class="ewb-info-items"] li a').items():
            detail_url = url.attr("href")
            details_page(detail_url)
        break


def details_page(detail_url):
    logger.warning("当前url={}".format("http://ggzy.heze.gov.cn" + detail_url))
    response = requests.get("http://ggzy.heze.gov.cn" + detail_url, headers=headers, verify=False).text
    parse_page(response,detail_url)

def parse_page(response,detail_url):
    res_t = pq(response)
    bid_name = res_t('div[class="article-info"] h1').text()
    # print(bid_name)
    bid_html_con = str(res_t('div[class="con"]').outer_html()).replace("'",'"')
    # print(bid_html_con)
    # bid_source = res_t('div[class="ewb-article-sources"] p').eq(3).text()
    bid_category = res_t('p[class="ewb-location-content"] a').eq(2).text()
    # print(bid_category)
    bid_info_type = res_t('p[class="ewb-location-content"] span').text()
    # print(bid_info_type)
    pre = re.compile('>(.*?)<')
    bid_content = ''.join(pre.findall(str(bid_html_con)))
    # print(bid_content)
    information_time = res_t('p[class="infotime"]').text()
    # print(information_time)
    item = {
        "bid_id": get_md5(str(detail_url).split("/")[-1].split(".")[0]),
        "bid_md5_url": get_md5("http://ggzy.heze.gov.cn" + detail_url),
        "bid_city": "菏泽市",
        "bid_county": "",
        "bid_url": "http://ggzy.heze.gov.cn" + detail_url,
        "bid_category": bid_category,
        "bid_info_type": bid_info_type,
        # "bid_source": bid_source,
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


