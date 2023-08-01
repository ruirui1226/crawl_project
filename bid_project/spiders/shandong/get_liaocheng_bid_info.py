# -*- coding: utf-8 -*-
# @Time : 2023/6/12 9:03
# @Author: mayj
# 聊城招投标
import datetime
import json
import re
import time

import requests
from lxml import etree
from loguru import logger
from untils.common import urljoin_url, get_md5
from untils.pysql import MysqlPipelinePublic
from untils.redis_conn import conn

BASE_URL = "http://ggzyjy.liaocheng.gov.cn/"
GET_CATEGORY_URL = "http://ggzyjy.liaocheng.gov.cn/lcggzy/jyxx/003001/trade_info.html"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}


def get_ino_type_urls():
    """获取二级标签url"""
    res = requests.get(GET_CATEGORY_URL, headers=headers)
    tree = etree.HTML(res.text)
    item_xpaths = tree.xpath('//ul[@class="tree"]/li')
    ino_type_datas = []
    for item_xpath in item_xpaths:
        category = item_xpath.xpath("./h3/a/@title")[0]
        category_url = item_xpath.xpath("./h3/a/@href")[0]
        if category == "建设工程":
            item_sub_xpaths = item_xpath.xpath("./div/ul/li")
            for into_sub_xpath in item_sub_xpaths:
                sub_category = into_sub_xpath.xpath("./h3/a/@title")[0]
                sub_category_url = into_sub_xpath.xpath("./h3/a/@href")[0]
                ino_type_datas.append(
                    {
                        "url": sub_category_url,
                        "category": category,
                        "sub_category": sub_category,
                    }
                )
        else:
            ino_type_datas.append(
                {
                    "url": category_url,
                    "category": category,
                }
            )
            # into_type_xpaths = into_sub_xpath.xpath('.//li[@class="tree-item"]')
            # for into_type_xpath in into_type_xpaths:
            #     into_type = into_type_xpath.xpath('./a/@title')[0]
            #     href = into_type_xpath.xpath('./a/@href')[0]
            #     into_type_new = f'{category_new}:{into_type}'
            #     ino_type_datas.append({
            #         'category': category,
            #         'into_type': into_type_new,
            #         'href': href,
            #     })
        # else:
        # into_type_xpaths = item_xpath.xpath('.//li[@class="tree-item"]')
        # for into_type_xpath in into_type_xpaths:
        #     into_type = into_type_xpath.xpath('./a/@title')[0]
        #     href = into_type_xpath.xpath('./a/@href')[0]
        #     ino_type_datas.append({
        #         'category':category,
        #         'into_type':into_type,
        #         'href':href,
        #     })
    return ino_type_datas


def get_liaocheng_bid_list(meta):
    """获取聊城招投标列表信息"""
    url = meta["url"]
    url = urljoin_url(BASE_URL, url)
    res = requests.get(url, headers=headers)
    if "pan-hd" not in res.text:
        logger.error(f"{url}:获取列表信息失败")
        return
    tree = etree.HTML(res.text)
    info_type_tree = tree.xpath('//div[@class="context-box"]/div')
    for i, info_type_xpath in enumerate(info_type_tree):
        if (i + 1) % 2 == 1:
            info_type = info_type_xpath.xpath("./span/text()")[0].strip()
            if meta.get("sub_category", ""):
                info_type = f'{meta["sub_category"]}:{info_type}'
            next_url = info_type_xpath.xpath("./a/@href")[0]
            category_id_str = re.search(r"jyxx(/.+/)trade", next_url).group(1)
        if (i + 1) % 2 == 0:
            trade_items = info_type_xpath.xpath('.//li[@class="trade-item"]')
            last_pub_time = ""
            for trade_item_xpath in trade_items:
                href = trade_item_xpath.xpath("./a/@href")[0]
                info_id = re.search(r"infoid=(.+?)&", href).group(1)
                det_url = urljoin_url(BASE_URL, href)
                if conn.sismember("bid_liaocheng:liaocheng_bid_det_info", get_md5(info_id)):
                    logger.debug("{}=======>数据已经采集，无需再次采集".format(det_url))
                    continue

                bid_name = trade_item_xpath.xpath("./a/@title")[0]
                pub_date = trade_item_xpath.xpath('./span[@class="date r"]/text()')[0].strip()
                last_pub_time = pub_date
                categorynum_str = re.search("categorynum=(\d+)", href).group(1)
                pub_date_str = pub_date.replace("-", "")
                new_category_str = (
                    category_id_str if categorynum_str in category_id_str else category_id_str + categorynum_str + "/"
                )
                req_det_url = (
                    f"http://ggzyjy.liaocheng.gov.cn/lcggzy/jyxx{new_category_str}/{pub_date_str}/{info_id}.html"
                )

                ret_data = {
                    "url": det_url,
                    "req_det_url": req_det_url,
                    "pub_date": pub_date,
                    "bid_name": bid_name,
                    "id": get_md5(info_id),
                    "category": meta["category"],
                    "type": info_type,
                }
                logger.debug(ret_data)
                conn.sadd("bid_liaocheng:liaocheng_bid_det_req_info", json.dumps(ret_data))
            data_now = datetime.datetime.now().strftime("%Y-%m-%d")
            if last_pub_time == data_now:
                new_next_url = urljoin_url(BASE_URL, next_url)
                next_meta = {
                    "category": meta["category"],
                    "info_type": info_type,
                    "url": new_next_url,
                }
                get_liaocheng_bid_next_list(next_meta)


def get_liaocheng_bid_next_list(meta):
    """获取列表页更多信息"""
    url = meta["url"]
    url = urljoin_url(BASE_URL, url)
    res = requests.get(url, headers=headers)
    if "pan-hd" not in res.text:
        logger.error(f"{url}:获取列表更多信息失败")
        return
    tree = etree.HTML(res.text)
    item_tree = tree.xpath('//div[@class="context-bd"]//li[@class="trade-item"]')
    for item_xpath in item_tree:
        href = item_xpath.xpath("./a/@href")[0]
        info_id = re.search(r"infoid=(.+?)&", href).group(1)
        det_url = urljoin_url(BASE_URL, href)
        if conn.sismember("bid_liaocheng:liaocheng_bid_det_info", get_md5(info_id)):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(det_url))
            continue

        bid_name = item_xpath.xpath("./a/@title")[0]
        pub_date = item_xpath.xpath('./span[@class="date r"]/text()')[0].strip()
        categorynum_str = re.search("categorynum=(\d+)", href).group(1)
        pub_date_str = pub_date.replace("-", "")
        category_id_str = re.search(r"jyxx(/.+/)trade", meta["url"]).group(1)
        new_category_str = (
            category_id_str if categorynum_str in category_id_str else category_id_str + categorynum_str + "/"
        )
        req_det_url = f"http://ggzyjy.liaocheng.gov.cn/lcggzy/jyxx{new_category_str}/{pub_date_str}/{info_id}.html"

        ret_data = {
            "url": det_url,
            "req_det_url": req_det_url,
            "pub_date": pub_date,
            "bid_name": bid_name,
            "id": get_md5(info_id),
            "category": meta["category"],
            "type": meta["info_type"],
        }
        logger.debug(ret_data)
        conn.sadd("bid_liaocheng:liaocheng_bid_det_req_info", json.dumps(ret_data))


def get_liaocheng_bid_det(meta_data):
    """获取聊城招投标详情信息"""
    logger.debug("正在获取详情内容：{}".format(meta_data["url"]))
    resp = requests.get(meta_data["req_det_url"], headers=headers)
    if str(resp.status_code) == "404":
        logger.warning("详情数据不存在：{}".format(meta_data["req_det_url"]))
        return "404"
    if "<!-- main -->" not in resp.text:
        logger.error("未获取到详情信息内容")
        return ""

    bid_html_con = re.search(r"<!-- main -->(.+)<!-- 页面脚本 -->", resp.text, re.S).group(1).strip().replace("'", "’")
    bid_html_con_tree = etree.HTML(bid_html_con)
    content = bid_html_con_tree.xpath("string(.)").replace("'", "’")

    bid_data = {
        "bid_id": meta_data["id"],
        "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        "bid_url": meta_data["url"],
        "bid_city": "聊城市",
        # "bid_county": meta_data["county"],
        "bid_category": meta_data["category"],
        "bid_info_type": meta_data["type"],
        "bid_source": "聊城市公共资源交易中心",
        "bid_name": meta_data["bid_name"],
        "bid_public_time": meta_data["pub_date"],
        "bid_html_con": bid_html_con,
        "bid_content": content,
    }
    return bid_data


def main():
    # 获取列表信息
    info_type_metas = get_ino_type_urls()
    for info_type_meta in info_type_metas:
        get_liaocheng_bid_list(info_type_meta)

    mql = MysqlPipelinePublic()
    # 获取详情信息
    meta_list = conn.smembers("bid_liaocheng:liaocheng_bid_det_req_info")
    for meta_str in meta_list:
        meta = json.loads(meta_str)
        if conn.sismember("bid_liaocheng:liaocheng_bid_det_info", meta["id"]):
            conn.srem("bid_liaocheng:liaocheng_bid_det_req_info", meta_str)
            logger.debug("{}=======>数据已经采集，无需再次采集".format(meta["url"]))
            continue

        time.sleep(1)
        data = get_liaocheng_bid_det(meta)
        if isinstance(data, str):
            if data == "404":
                conn.sadd("bid_liaocheng:liaocheng_bid_det_info", meta["id"])
                conn.srem("bid_liaocheng:liaocheng_bid_det_req_info", meta_str)
                continue
        if data:
            logger.debug(data["bid_name"])
            mql.insert_sql("t_zx_bid_crawl_info", data)
            # mql.insert_sql("t_zx_bid_crawl_info_myj", data)
            conn.sadd("bid_liaocheng:liaocheng_bid_det_info", meta["id"])
            conn.srem("bid_liaocheng:liaocheng_bid_det_req_info", meta_str)
    mql.close()


if __name__ == "__main__":
    main()
