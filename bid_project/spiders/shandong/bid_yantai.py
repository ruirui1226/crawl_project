#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: 招投标-山东省-烟台市
@version: python3
@author: shenr
@time: 2023/06/09
"""


import json
import logging
import re
import time

import requests
from pyquery import PyQuery as pq

from bid_project.untils.common import get_md5
from bid_project.untils.pysql import MysqlPipelinePublic

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Referer": "http://ggzyjy.yantai.gov.cn/jyxxgc/index.jhtml",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}
cookies = {
    "_gscu_31623267": "861010745g3vav21",
    "clientlanguage": "zh_CN",
    "_gscbrs_31623267": "1",
    "_gscs_31623267": "86279097icb2x521|pv:17",
}
current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
pub_time = ""


def get_list(url, pagenum):
    res = requests.get(url=url.format(pagenum), headers=headers, cookies=cookies, verify=False)
    res_t = pq(res.text)
    results = res_t('ul[class="article-list2"]')
    mq = MysqlPipelinePublic()
    for each in results('li[class="jygk-li"]').items():
        detail_url = each("div a").attr("href")
        bid_id = re.findall(".*/(.*?).jhtml", str(detail_url), re.S)[0]
        detail = get_detail(detail_url)
        pub_time = each("div p").text()[:10] if each("div p").text() and re.search(r'\d', each("div p").text()) else each("div").eq(1).text()
        if detail.get("bid_category") == "政府采购":
            item = {}
            item["po_id"] = get_md5(bid_id)
            item["po_city"] = "烟台市"
            item["po_county"] = each("div span").eq(0).text().replace("[", "").replace("]", "").replace(" ", "")
            item["bid_url"] = detail_url
            item["po_category"] = detail.get("bid_category")
            item["po_info_type"] = detail.get("bid_info_type")
            item["po_source"] = detail.get("bid_source") or each('div[class="article-list3-t2"] div').eq(0).text()
            item["po_html_con"] = str(detail.get("bid_html_con")).replace("'", '"')
            item["po_content"] = str(detail.get("bid_content")).replace("'", '"')
            item["bo_name"] = each("div a").attr("title")
            item["po_public_time"] = each("div p").text()[:10] if each("div p").text() and re.search(r'\d', each("div p").text()) else each("div").eq(1).text()
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            logging.info(item)
            try:
                mq.insert_sql("t_zx_po_crawl_info", item)
            except:
                logging.info("chucuo")
        else:
            item = {}
            item["bid_id"] = get_md5(bid_id)
            item["bid_md5_url"] = ""
            item["bid_city"] = "烟台市"
            item["bid_county"] = each("div span").eq(0).text().replace("[", "").replace("]", "").replace(" ", "")
            item["bid_url"] = detail_url
            item["bid_category"] = detail.get("bid_category")
            item["bid_info_type"] = detail.get("bid_info_type")
            item["bid_source"] = detail.get("bid_source") or each('div[class="article-list3-t2"] div').eq(0).text()
            item["bid_html_con"] = str(detail.get("bid_html_con")).replace("'", '"')
            item["bid_content"] = str(detail.get("bid_content")).replace("'", '"')
            item["bid_name"] = each("div a").attr("title")
            item["bid_public_time"] = each("div p").text()[:10] if each("div p").text() and re.search(r'\d', each("div p").text()) else each("div").eq(1).text()
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            logging.info(item)
            try:
                mq.insert_sql("t_zx_bid_crawl_info", item)
            except:
                logging.info("chucuo1111")
    total = re.findall("count: (.*?),", str(res_t), re.S)[0]
    # if int(total)/10 + 1 > pagenum:
    # if pub_time == current_time:
    #     pagenum += 1
    #     get_list(url.format(pagenum), pagenum)
    # else:
    #     logging.info("=============当天已爬取完毕=============")


def get_detail(url):
    res = requests.get(url=url, headers=headers, cookies=cookies, verify=False)
    res_t = pq(res.text)
    # 来源
    bid_source = res_t('div[class="content-title2"] span').eq(2).text()
    # 层级
    bid_category = res_t('div[class="sitemap"] a').eq(2).text()
    bid_info_type = res_t('div[class="sitemap"] a').eq(3).text()
    # 详情
    content = res_t('div[class="content-warp"]').text()
    html_content = res_t('div[class="content-warp"]').outerHtml()
    return {
        "bid_source": bid_source,
        "bid_content": content,
        "bid_html_con": html_content,
        "bid_category": bid_category,
        "bid_info_type": bid_info_type,
    }


if __name__ == "__main__":
    url_list = [
        "http://ggzyjy.yantai.gov.cn/jyxxgc/index_{}.jhtml",
        "http://ggzyjy.yantai.gov.cn/jyxxzc/index_{}.jhtml",
        "http://ggzyjy.yantai.gov.cn/jyxxgt/index_{}.jhtml",
        "http://ggzyjy.yantai.gov.cn/jyxxcq/index_{}.jhtml",
    ]
    for url_ in url_list:
        pagenum = 1
        get_list(url_, pagenum)
        # break
