# -*- coding: utf-8 -*-
"""
@desc: 山东省公共资源交易平台
@version: python3
@author: shenr
@time: 2023/6/9 
"""
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
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "If-Modified-Since": "Fri, 09 Jun 2023 04:52:11 GMT",
    "If-None-Match": 'W/"6482affb-631a"',
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}
cookies = {
    "Hm_lvt_3147c565b4637bb1f8c07a562a3c6cb7": "1681116668,1681204204,1681205868,1681866853",
    "wondersLog_sdywtb_sdk": "%7B%22persistedTime%22%3A1681116667827%2C%22updatedTime%22%3A1681866989133%2C%22sessionStartTime%22%3A1681866851645%2C%22sessionReferrer%22%3A%22%22%2C%22deviceId%22%3A%225aa8e1b5940af678c35ba43675924860-6431%22%2C%22LASTEVENT%22%3A%7B%22eventId%22%3A%22wondersLog_pv%22%2C%22time%22%3A1681866989132%7D%2C%22sessionUuid%22%3A2468230032295940%2C%22costTime%22%3A%7B%7D%7D",
    "zh_choose_428": "s",
}


def get_list(page_num, page_all, url):
    """ """
    response = requests.get(url.format(page_num))  # , headers=headers, cookies=cookies, verify=False)
    res = pq(response.text)
    doc = res
    re_data = re.findall("&lt;recordset&gt;(.*?)&lt;/recordset&gt;", str(doc), re.S)
    url_list = re.findall(';a href="(.*?)" target', str(re_data), re.S)
    for detail_url in url_list:
        detail = get_detial(detail_url)
        infoid = re.findall(".*/(.*?).html", str(detail_url), re.S)[0]
        if detail.get("bid_info_type") == "采购公告":
            item = {}
            item["po_id"] = get_md5(infoid)
            item["po_city"] = "山东省公共资源交易中心"
            item["po_county"] = detail.get("region")
            item["bid_url"] = detail_url
            item["po_category"] = detail.get("bid_category")
            item["po_info_type"] = detail.get("bid_info_type")
            item["po_source"] = detail.get("bid_source")
            item["po_html_con"] = str(detail.get("bid_html_con")).replace("'", '"')
            item["po_content"] = str(detail.get("bid_content")).replace("'", '"')
            item["bo_name"] = detail.get("name")
            item["website_name"] = "山东省公共资源交易中心"
            item["website_url"] = "http://ggzyjyzx.shandong.gov.cn/"
            item["po_public_time"] = detail.get("bid_public_time")
            item["bid_orgin_url"] = "http://ggzyjyzx.shandong.gov.cn/col/col209868/index.html"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            logging.info(item)
            mq = MysqlPipelinePublic()
            mq.insert_sql("t_zx_po_crawl_info", item)
        else:
            item = {}
            item["bid_id"] = get_md5(infoid)
            item["bid_md5_url"] = ""
            item["bid_city"] = "山东省公共资源交易中心"
            item["bid_county"] = detail.get("region")
            item["bid_url"] = detail_url
            item["bid_category"] = detail.get("bid_category")
            item["bid_info_type"] = detail.get("bid_info_type")
            item["bid_source"] = detail.get("bid_source")
            item["bid_html_con"] = str(detail.get("bid_html_con")).replace("'", '"')
            item["bid_content"] = str(detail.get("bid_content")).replace("'", '"')
            item["bid_name"] = detail.get("name")
            item["website_name"] = "山东省公共资源交易中心"
            item["website_url"] = "http://ggzyjyzx.shandong.gov.cn/"
            item["bid_public_time"] = detail.get("bid_public_time")
            item["bid_orgin_url"] = "http://ggzyjyzx.shandong.gov.cn/col/col209868/index.html"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            logging.info(item)
            mq = MysqlPipelinePublic()
            mq.insert_sql("t_zx_bid_crawl_info", item)
        # break
    if page_num == 1:
        num_all = int(re.findall("totalRecord:(.*?),", str(doc), re.S)[0])
        page_all = int(num_all / 18)
    # if page_num < page_all + 1:
    #     page_num += 1
    #     get_list(page_num, page_all, url)


def get_detial(detail_url):
    response = requests.get(detail_url)  # , headers=headers, cookies=cookies, verify=False)
    res = pq(response.text)
    name = res('meta[name="article-title"]').text()
    content = res('div[class="article"]').text()
    html_content = res('div[class="article"]')
    bid_category = res('div[class="dqwz"] tr td a').eq(2).text()
    bid_info_type = res('div[class="dqwz"] tr td a').eq(3).text()
    bid_public_time = res('div[class="article-xinxi"] p').eq(0).text().replace("发布时间：", "")
    bid_source = res('div[class="article-xinxi"] p').eq(1).text()
    return {
        "name": name,
        "bid_content": content,
        "bid_public_time": bid_public_time,
        "bid_html_con": html_content,
        "bid_category": bid_category,
        "bid_info_type": bid_info_type,
        "bid_source": bid_source,
    }


if __name__ == "__main__":
    page_num = 1
    page_all = 1
    url_list = [
        "http://ggzyjyzx.shandong.gov.cn/col/col209868/index.html?uid=474655&pageNum={}",
        "http://ggzyjyzx.shandong.gov.cn/col/col209869/index.html?uid=474655&pageNum={}",
        "http://ggzyjyzx.shandong.gov.cn/col/col209870/index.html?uid=474655&pageNum={}",
    ]
    for url_ in url_list:
        get_list(page_num, page_all, url_)
        # break
