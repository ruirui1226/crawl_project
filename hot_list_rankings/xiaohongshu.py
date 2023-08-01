#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/7/7 16:08
@Author : zhangpf
@File : xiaohongshu.py
@Desc : 小红书
@Software: PyCharm
"""
import time
import requests
from loguru import logger
from pyquery import PyQuery as pq
from hot_list_rankings.pysql import MysqlPipelinePublic, get_md5

headers = {
    "authority": "tophub.today",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "referer": "https://tophub.today/n/DpQvNABoNE",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

response = requests.get("https://tophub.today/n/L4MdA5ldxD", headers=headers)
res = pq(response.text)
today_data = res('div[class="jc-c"]').eq(0)
data_list = today_data("table tbody tr").items()
for data in data_list:
    ranking = data('td[align="center"]').text()
    title = data('td[class="al"] a').text()
    lianjie = data('td[class="al"] a').attr("href")
    redu = data("td").eq(2).text()
    item = {
        "ranking": ranking.replace(".", ""),
        "title": title,
        "link": "https://tophub.today" + lianjie,
        "link2": "",
        "heat": redu,
        "md5_title": get_md5("小红书" + title),
        "platform": "小红书",
        "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        "time": time.strftime("%Y-%m-%d", time.localtime(int(time.time()))),
    }
    mq = MysqlPipelinePublic()
    mq.insert_sql("t_zx_popularity_ranking", item)
    logger.warning("当前数据={}".format(item))
