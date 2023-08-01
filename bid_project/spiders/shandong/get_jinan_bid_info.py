# -*- coding: utf-8 -*-
# @Time : 2023/6/7 10:00
# @Author: mayj
# 济南招投标
import json
import re
import time

import requests
from lxml import etree
from loguru import logger

from untils.common import urljoin_url, get_md5
from untils.redis_conn import conn
from untils.pysql import MysqlPipelinePublic

URL = "http://jnggzy.jinan.gov.cn/jnggzyztb/front/newChangeHomePageList.do"
BASE_URL = "http://jnggzy.jinan.gov.cn/"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def get_jinan_bid_list(type: int, page=1, next=False):
    """获取济南公共资源列表信息"""
    if type == 7:
        data = {
            "area": "",
            "type": type,
            "pagenum": page,
            "subheading": "城乡绿化",
        }
    else:
        data = {
            "area": "",
            "type": type,
            "pagenum": page,
        }
    logger.debug("正在请求第{}页".format(page))
    resp = requests.post(URL, headers=headers, data=data)
    json_data = resp.json()
    if "<li>" not in str(json_data.get("params", {})):
        logger.error("获取列表信息失败")
        return False
    data_params = json_data.get("params", {})
    data_str = ""
    for data_v in data_params.values():
        if isinstance(data_v, int):
            continue
        data_str += data_v
    data_tree = etree.HTML(data_str)
    li_list = data_tree.xpath("//li")
    for li_xph in li_list:
        herf = li_xph.xpath("./a/@href")[0]
        id = re.search(r"=(\w+)", herf).group(1)
        if conn.sismember("bid_jinan:jinan_bid_det_info", get_md5(id)):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(herf))
            continue
        try:
            county = li_xph.xpath('./span[@class="bt-left dq"]/@title')[0]
        except:
            county = ""
        bid_name = li_xph.xpath("./a/@title")[0].strip()
        pub_date = li_xph.xpath("./span[last()]/text()")[0]
        det_url = urljoin_url(BASE_URL, herf)
        ret_data = {"url": det_url, "county": county, "pub_date": pub_date, "bid_name": bid_name, "id": id}
        logger.info(ret_data)
        conn.sadd("bid_jinan:jinan_bid_det_req_info", json.dumps(ret_data))
    if next and page + 1 <= 2:
        get_jinan_bid_list(type, page + 1, next)


def get_jinan_bid_det(meta_data):
    """获取济南公共资源详情信息"""
    logger.debug("正在获取详情内容：{}".format(meta_data["url"]))
    resp = requests.get(meta_data["url"], headers=headers)
    if 'class="list"' not in resp.text:
        logger.error("未获取到详情信息内容")
        return
    tree = etree.HTML(resp.text)
    id = re.search(r"=(\w+)", meta_data["url"]).group(1)
    try:
        info_type = tree.xpath('//div[@class="bread"]/span[3]/text()')[0]
        category = tree.xpath('//div[@class="bread"]/span[2]/text()')[0]
    except:
        category = tree.xpath("//title/text()")[0].strip("详情")
        info_type = ""
    category = category.replace(">", "").strip()
    info_type = info_type.replace(">", "").strip()
    info_type = info_type if len(info_type) >= 2 else ""
    bid_html_con = tree.xpath('//div[@class="list"]')[0]
    if "区" in meta_data["county"]:
        meta_data["county"] = meta_data["county"].replace("市本级", "")
    bid_data = {
        "bid_id": get_md5(id),
        "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        "bid_url": meta_data["url"],
        "bid_city": "济南市",
        "bid_county": meta_data["county"],
        "bid_category": category,
        "bid_info_type": info_type,
        "bid_source": "济南公共资源交易中心",
        # 'bid_name':tree.xpath('//div[@class="list"]/h1/text()')[0],
        "bid_name": meta_data["bid_name"],
        "bid_public_time": meta_data["pub_date"],
        "bid_html_con": etree.tostring(bid_html_con, encoding="utf-8").decode("utf-8").replace("'", "’"),
        "bid_content": tree.xpath('string(//div[@class="list"])').replace("'", "’"),
    }
    return bid_data


def main():
    # 获取列表信息
    type_number_list = [0, 1, 2, 3, 4, 5, 6, 7]
    mql = MysqlPipelinePublic()
    for type_number in type_number_list:
        get_jinan_bid_list(type_number, next=True)

    # 获取详情信息
    meta_list = conn.smembers("bid_jinan:jinan_bid_det_req_info")
    for meta_str in meta_list:
        meta = json.loads(meta_str)
        if conn.sismember("bid_jinan:jinan_bid_det_info", meta["id"]):
            conn.srem("bid_jinan:jinan_bid_det_req_info", meta_str)
            logger.debug("{}=======>数据已经采集，无需再次采集".format(meta["id"]))
            continue
        time.sleep(1)
        data = get_jinan_bid_det(meta)
        if data:
            logger.debug(data["bid_name"])
            mql.insert_sql("t_zx_bid_crawl_info", data)
            # mql.insert_sql("t_zx_bid_crawl_info_myj", data)
            conn.sadd("bid_jinan:jinan_bid_det_info", data["bid_id"])
            conn.srem("bid_jinan:jinan_bid_det_req_info", meta_str)
    mql.close()


if __name__ == "__main__":
    main()
