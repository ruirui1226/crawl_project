# -*- coding: utf-8 -*-
# @Time : 2023/6/8 18:04
# @Author: mayj
# 淄博招投标


import json
import time

import requests
from lxml import etree
from loguru import logger

from untils.redis_conn import conn
from untils.common import urljoin_url, get_md5
from untils.pysql import MysqlPipelinePublic

URL = "http://ggzyjy.zibo.gov.cn:8082/EpointWebBuilder_zbggzy/rest/frontAppCustomAction/getPageInfoListNew?params=%7B%22siteGuid%22%3A%227eb5f7f1-9041-43ad-8e13-8fcb82ea831a%22%2C%22categoryNum%22%3A%22002%22%2C%22kw%22%3A%22%22%2C%22startDate%22%3A%22%22%2C%22endDate%22%3A%22%22%2C%22jystauts%22%3A%22%22%2C%22areacode%22%3A%22%22%2C%22pageIndex%22%3A{}%2C%22pageSize%22%3A14%7D"
BASE_URL = "http://ggzyjy.zibo.gov.cn:8082/gonggongziyuan-content.html?"
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37",
}


category_num_dict = {
    "002001001": "建设工程:招标公告",
    "002001002": "建设工程:变更公告",
    "002001003": "建设工程:中标候选人公示",
    "002001004": "建设工程:中标结果公示",
    "002001005": "建设工程:异常公告",
    "002001006": "建设工程:合同公示及变更",
    "002001007": "建设工程:招标项目计划",
    "002001009": "建设工程:提问回复",
    "002002001": "政府采购:需求（意向）公示",
    "002002002": "政府采购:采购公告",
    "002002003": "政府采购:更正公告",
    "002002004": "政府采购:中标（成交）公告",
    "002002005": "政府采购:终止公告",
    "002002006": "政府采购:合同公告",
    "002002007": "政府采购:验收公告",
    "002011001": "自然资源:土地矿产",
    "002011001001": "土地矿产:出让公告",
    "002011001002": "土地矿产:结果公示",
    "002011001003": "土地矿产:变更公告",
    "002011001004": "土地矿产:终止公告",
    "002011001005": "土地矿产:中止公告",
    "002011002": "自然资源:集体用地",
    "002011002001": "集体用地:出让公告",
    "002011002002": "集体用地:结果公示",
    "002011002003": "集体用地:变更公告",
    "002011002004": "集体用地:终止公告",
    "002004001": "产权交易:出让公告",
    "002004002": "产权交易:结果公示",
    "002004003": "产权交易:变更公告",
    "002004004": "产权交易:终止公告",
    "002009001": "国企采购:需求（意向）公示",
    "002009002": "国企采购:采购公告",
    "002009003": "国企采购:更正公告",
    "002009004": "国企采购:中标（成交）公告",
    "002009005": "国企采购:终止公告",
    "002009006": "国企采购:合同公告",
    "002009007": "国企采购:验收公告",
    "002007001": "药械采购:需求（意向）公示",
    "002007002": "药械采购:采购公告",
    "002007003": "药械采购:更正公告",
    "002007004": "药械采购:中标（成交）公告",
    "002007005": "药械采购:终止公告",
    "002007006": "药械采购:合同公告",
    "002007007": "药械采购:验收公告",
    "002008001": "其他交易:需求（意向）公示",
    "002008002": "其他交易:采购公告",
    "002008003": "其他交易:更正公告",
    "002008004": "其他交易:中标（成交）公告",
    "002008005": "其他交易:终止公告",
    "002008006": "其他交易:合同公告",
    "002008007": "其他交易:验收公告",
}


def get_zibo_bid_list(page=0, next=False):
    """获取淄博公共资源列表信息"""

    logger.debug("正在请求第{}页".format(page))
    resp = requests.post(URL.format(page), headers=headers)

    json_data = resp.json()
    if json_data.get("status", {}).get("text", "") != "操作成功":
        logger.error("获取列表信息失败")
        return False
    datas = json_data.get("custom").get("infodata")

    for data_dict in datas:
        herf = data_dict.get("infourl")
        id = data_dict.get("infoid")
        if conn.sismember("bid_zibo:zibo_bid_det_info", get_md5(id)):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(herf))
            continue
        county = data_dict.get("areacode")

        bid_name = data_dict.get("realtitle")
        pub_date = data_dict.get("infodate")
        det_url = urljoin_url(BASE_URL, herf)
        relationguid = data_dict.get("relationguid")
        categorynum = data_dict.get("categorynum")
        try:
            category_str = category_num_dict.get(str(categorynum))
            category, info_type = category_str.split(":")
        except:
            category = ""
            info_type = ""

        url = f"http://ggzyjy.zibo.gov.cn:8082/gonggongziyuan-content.html?infoid={id}&relationguid={relationguid}&categorynum={categorynum}"
        ret_data = {
            "det_url": det_url,
            "county": county,
            "pub_date": pub_date,
            "bid_name": bid_name,
            "id": id,
            "url": url,
            "category": category,
            "info_type": info_type,
        }
        logger.info(json.dumps(ret_data))
        conn.sadd("bid_zibo:zibo_bid_det_req_info", json.dumps(ret_data))
    if next and page + 1 <= 4:
        get_zibo_bid_list(page + 1, next)


def get_zibo_bid_det(meta):
    """获取淄博公共资源详情信息"""
    res = requests.get(meta["det_url"])

    if "viewGuid" in res.text:
        tree = etree.HTML(res.text)
        bid_data = {
            "bid_id": get_md5(meta["id"]),
            "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            "bid_url": meta["url"],
            "bid_city": "淄博市",
            "bid_county": meta["county"],
            "bid_category": meta["category"],
            "bid_info_type": meta["info_type"],
            "bid_source": "淄博公共资源交易网",
            "bid_name": meta["bid_name"],
            "bid_public_time": meta["pub_date"],
            "bid_html_con": res.text.replace("'", "’"),
            "bid_content": tree.xpath("string(.)").replace("'", "’"),
        }
        return bid_data
    logger.error(f'未获取到详情数据：{meta["det_url"]}')


def main():
    # 获取列表信息
    get_zibo_bid_list(next=True)

    # 获取详情信息
    meta_list = conn.smembers("bid_zibo:zibo_bid_det_req_info")
    mql = MysqlPipelinePublic()
    for meta_str in meta_list:
        meta = json.loads(meta_str)
        if conn.sismember("bid_zibo:zibo_bid_det_info", meta["id"]):
            conn.srem("bid_zibo:zibo_bid_det_req_info", meta_str)
            logger.debug("{}=======>数据已经采集，无需再次采集".format(meta["url"]))
            continue
        time.sleep(1)
        data = get_zibo_bid_det(meta)
        if data:
            logger.debug(data["bid_name"])
            mql.insert_sql("t_zx_bid_crawl_info", data)
            # mql.insert_sql("t_zx_bid_crawl_info_myj", data)
            conn.sadd("bid_zibo:zibo_bid_det_info", data["bid_id"])
            conn.srem("bid_zibo:zibo_bid_det_req_info", meta_str)
    mql.close()


if __name__ == "__main__":
    main()
