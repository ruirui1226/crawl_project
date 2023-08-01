#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: 招投标-山东省-东营市
@version: python3
@author: shenr
@time: 2023/06/07
"""


import re
import time
import logging
import requests
from pyquery import PyQuery as pq

from bid_project.untils.common import get_md5
from bid_project.untils.pysql import MysqlPipelinePublic


url_get = "http://ggzy.dongying.gov.cn/jyxx/about.html"


def get_list(pagenum):
    logging.info(f"===========当前爬取{pagenum}页===========")
    if pagenum == 1:
        url_ = url_get
    else:
        url_ = f"http://ggzy.dongying.gov.cn/jyxx/{pagenum}.html"
    res = requests.get(url=url_, verify=False)
    res_t = pq(res.text)
    results = res_t('div[id="static"]')

    for each in results('ul[class="ewb-look-items"] li').items():
        detail_url = "http://ggzy.dongying.gov.cn/" + each("h2 a").attr("href")
        bid_public_time = each("div div").eq(1).text()
        infoid = re.findall(".*/(.*?).html", str(detail_url), re.S)[0]
        # 详情页
        detail = get_detail(detail_url)
        if detail.get("bid_category") == "政府采购":
            item = {}
            item["po_id"] = get_md5(infoid)
            item["po_city"] = "东营市"
            item["po_county"] = detail.get("region")
            item["bid_url"] = detail_url
            item["po_category"] = detail.get("bid_category")
            item["po_info_type"] = detail.get("bid_info_type")
            item["po_source"] = detail.get("bid_source")
            item["po_html_con"] = str(detail.get("bid_html_con")).replace("'", '"')
            item["po_content"] = str(detail.get("bid_content")).replace("'", '"')
            item["bo_name"] = each("h2 a").attr("title")
            item["po_public_time"] = bid_public_time
            item["website_name"] = "东营市公共资源交易中心"
            item["website_url"] = "http://ggzy.dongying.gov.cn/jyxx/about.html"
            item["bid_orgin_url"] = "http://ggzy.dongying.gov.cn/jyxx/about.html"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            logging.info(item)
            mq = MysqlPipelinePublic()
            mq.insert_sql("t_zx_po_crawl_info", item)
        else:
            item = {}
            item["bid_id"] = get_md5(infoid)
            item["bid_md5_url"] = ""
            item["bid_city"] = "东营市"
            item["bid_county"] = detail.get("region")
            item["bid_url"] = detail_url
            item["bid_category"] = detail.get("bid_category")
            item["bid_info_type"] = detail.get("bid_info_type")
            item["bid_source"] = detail.get("bid_source")
            item["bid_html_con"] = str(detail.get("bid_html_con")).replace("'", '"')
            item["bid_content"] = str(detail.get("bid_content")).replace("'", '"')
            item["bid_name"] = each("h2 a").attr("title")
            item["bid_public_time"] = bid_public_time
            item["website_name"] = "东营市公共资源交易中心"
            item["website_url"] = "http://ggzy.dongying.gov.cn/jyxx/about.html"
            item["bid_orgin_url"] = "http://ggzy.dongying.gov.cn/jyxx/about.html"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            logging.info(item)
            # 写入数据
            mq = MysqlPipelinePublic()
            mq.insert_sql("t_zx_bid_crawl_info", item)
            # break
    # 下一页
    total = re.findall('total: (.*?),', str(res_t), re.S)[0]
    if int(total)/10 + 1 > pagenum:
        pagenum += 1
        get_list(pagenum)


def get_detail(url):
    res = requests.get(url=url)
    res_t = pq(res.text)
    # 区县
    region = res_t('span[class="go-tt"] font').eq(0).text()
    # 层级
    bid_category = res_t('div[class="ewb-route"] p a').eq(2).text()
    bid_info_type = res_t('span[id="viewGuid"]').text()
    # 详情
    content = res_t('div[class="cm-wpr"]').text()
    html_content = res_t('div[class="cm-wpr"]').outerHtml()
    return {
        "region": re.findall("·(.*?)]", str(region), re.S)[0] if re.findall("·(.*?)]", str(region), re.S) else "",
        "bid_content": content,
        "bid_html_con": html_content,
        "bid_category": bid_category,
        "bid_info_type": bid_info_type,
    }


if __name__ == "__main__":
    pagenum = 1
    get_list(pagenum)
