# -*- coding: utf-8 -*-
# @Time : 2023/6/8 14:19
# @Author: mayj
# 青岛招投标
import json
import re
import time

import requests
from lxml import etree
from loguru import logger

from untils.common import urljoin_url, get_md5
from untils.redis_conn import conn
from untils.pysql import MysqlPipelinePublic

# URL = "http://jnggzy.jinan.gov.cn/jnggzyztb/front/newChangeHomePageList.do"
BASE_URL = "https://ggzy.qingdao.gov.cn"
GET_TYPE_URL = "https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/0-0-4"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    # 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
}


def get_ino_type_urls():
    """获取二级标签链接"""
    res = requests.get(GET_TYPE_URL, headers=headers)
    tree = etree.HTML(res.text)
    expmenu_list = tree.xpath('//div[@class="expmenu"]/div')
    data = []
    for i, expmenu_xph in enumerate(expmenu_list):
        try:
            vtitle = expmenu_xph.xpath(f'../div[{i+1}][@class="vtitle"]/text()')[0]
            data_dict = {
                "category": vtitle,
            }
            if vtitle:
                vcons = expmenu_xph.xpath(f'../div[{i+2}][@class="vcon"]/ul/li')
                for vcon in vcons:
                    vcon_name = vcon.xpath("./a/text()")[0]
                    vcon_href = vcon.xpath("./a/@href")[0]
                    data_dict["type"] = vcon_name
                    data_dict["href"] = vcon_href

                    # data_dict[vtitle][vcon_name] = vcon_href
                    data.append(data_dict)

        except:
            pass
    return data


def get_qingdao_bid_list(meta):
    """获取青岛市公共资源列表信息"""
    url = urljoin_url(BASE_URL, meta["href"])
    logger.debug("正在请求{}数据".format(url))
    resp = requests.get(url, headers=headers)
    if "list_info" not in resp.text:
        logger.error("获取列表信息失败")
        return False

    data_tree = etree.HTML(resp.text)
    li_list = data_tree.xpath('//div[@class="info_con"]//tr')
    for li_xph in li_list:
        try:
            herf = li_xph.xpath("./td[1]/a/@href")[0]
        except:
            logger.debug(f'{meta["href"]}没有数据')
            continue
        det_url = urljoin_url(BASE_URL, herf)
        if conn.sismember("bid_qingdao:qingdao_bid_det_info", get_md5(det_url)):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(det_url))
            continue
        try:
            county = li_xph.xpath("./td[1]/a/text()")[0]
            county = re.search(r"[(.+?)]", county).group(1)
        except Exception as e:
            county = ""
        bid_name = li_xph.xpath("./td[1]/a/@title")[0].strip()
        pub_date = li_xph.xpath("./td[2]/text()")[0]
        ret_data = {
            "url": det_url,
            "county": county,
            "pub_date": pub_date,
            "bid_name": bid_name,
            "id": get_md5(det_url),
            "category": meta["category"],
            "type": meta["type"],
        }
        conn.sadd("bid_qingdao:qingdao_bid_det_req_info", json.dumps(ret_data))

    # if next and page+1 <=2:
    #     get_qingdao_bid_list(type, page+1, next)


def get_qingdao_bid_det(meta_data):
    """获取青岛公共资源详情信息"""
    logger.debug("正在获取详情内容：{}".format(meta_data["url"]))
    resp = requests.get(meta_data["url"], headers=headers)
    if "ewb_location" not in resp.text:
        logger.error("未获取到详情信息内容")
        return
    tree = etree.HTML(resp.text)
    try:
        bid_html_con = tree.xpath('//div[@class="box_bg"]')[0]
        content = tree.xpath('string(//div[@class="box_bg"])').replace("'", "’")
    except:
        bid_html_con = tree.xpath('.//div[@class="ewb-main"]')[0]
        content = tree.xpath('string(//div[@class="ewb-main"])').replace("'", "’")
    bid_data = {
        "bid_id": get_md5(meta_data["url"]),
        "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        "bid_url": meta_data["url"],
        "bid_city": "青岛市",
        "bid_county": meta_data["county"],
        "bid_category": meta_data["category"],
        "bid_info_type": meta_data["type"],
        "bid_source": "青岛公共资源交易平台",
        # 'bid_name':tree.xpath('//div[@class="list"]/h1/text()')[0],
        "bid_name": meta_data["bid_name"],
        "bid_public_time": meta_data["pub_date"],
        "bid_html_con": etree.tostring(bid_html_con, encoding="utf-8").decode("utf-8").replace("'", "’"),
        "bid_content": content,
    }
    return bid_data


def main():
    # 获取列表信息
    all_list = get_ino_type_urls()
    mql = MysqlPipelinePublic()
    for start_dict in all_list:
        get_qingdao_bid_list(start_dict)

    # 获取详情信息
    meta_list = conn.smembers("bid_qingdao:qingdao_bid_det_req_info")
    for meta_str in meta_list:
        meta = json.loads(meta_str)
        if conn.sismember("bid_qingdao:qingdao_bid_det_info", meta["id"]):
            conn.srem("bid_qingdao:qingdao_bid_det_req_info", meta_str)
            logger.debug("{}=======>数据已经采集，无需再次采集".format(meta["url"]))
            continue
        time.sleep(1)
        data = get_qingdao_bid_det(meta)
        if data:
            logger.debug(data["bid_name"])
            mql.insert_sql("t_zx_bid_crawl_info", data)
            # mql.insert_sql("t_zx_bid_crawl_info_myj", data)
            conn.sadd("bid_qingdao:qingdao_bid_det_info", data["bid_id"])
            conn.srem("bid_qingdao:qingdao_bid_det_req_info", meta_str)
    mql.close()


if __name__ == "__main__":
    main()
