# -*- coding: utf-8 -*-
"""
@desc: 
@version: python3
@author: shenr
@time: 2023/7/13 
"""
import json

from untils.pysql import MysqlPipelinePublic

# from .pysql import MysqlPipelinePublic

# 查询出bo表


# x = [
#     "po_id",
#     "bid_url",
#     "po_md5_url",
#     "po_province",
#     "po_city",
#     "po_county",
#     "po_industry",
#     "po_zone",
#     "po_category",
#     "po_info_type",
#     "category",
#     "info_type",
#     "po_public_time",
#     "bo_name",
#     "po_source",
#     "po_html_con",
#     "po_content",
#     "po_json_data",
#     "description",
#     "modifier",
#     "dept_belong_id",
#     "is_delete",
#     "is_active",
#     "creator_id",
#     "is_crawl",
#     "website_name",
#     "website_url",
#     "bid_orgin_url",
#     "po_status",
#     "create_datetime",
#     "update_datetime",
#     "is_type",
# ]
#
#
mq = MysqlPipelinePublic()
# ccc = mq.select_sql("t_zx_po_crawl_info", x, {"'1'": "1"})
# print(len(ccc))
# errlist = []
# for each in ccc:
#     item = {}
#     item["bid_id"] = each.get("po_id")
#     item["update_datetime"] = each.get("update_datetime")
#     item["create_datetime"] = each.get("create_datetime")
#     item["bid_url"] = each.get("bid_url")
#     item["bid_md5_url"] = each.get("po_md5_url")
#     item["bid_province"] = each.get("po_province")
#     item["bid_city"] = each.get("po_city")
#     item["bid_county"] = each.get("po_county")
#     item["bid_industry"] = each.get("po_industry")
#     item["bid_zone"] = each.get("po_zone")
#     item["bid_category"] = each.get("po_category")
#     item["bid_info_type"] = each.get("po_info_type")
#     item["category"] = each.get("category")
#     item["info_type"] = each.get("info_type")
#     item["bid_source"] = each.get("po_source")
#     item["bid_name"] = str(each.get("bo_name")).replace("'", '"')
#     item["bid_public_time"] = each.get("po_public_time")
#     item["bid_html_con"] = str(each.get("po_html_con")).replace("'", '"')
#     item["bid_json_data"] = str(each.get("po_json_data")).replace("'", '"')
#     item["bid_content"] = str(each.get("po_content")).replace("'", '"')
#     item["description"] = each.get("description")
#     item["modifier"] = each.get("modifier")
#     item["dept_belong_id"] = each.get("dept_belong_id")
#     item["is_delete"] = each.get("is_delete")
#     item["is_active"] = each.get("is_active")
#     item["bid_status"] = each.get("po_status")
#     item["creator_id"] = each.get("creator_id")
#     item["is_crawl"] = each.get("is_crawl")
#     item["website_url"] = each.get("website_url")
#     item["bid_orgin_url"] = each.get("po_orgin_url")
#     item["website_name"] = each.get("website_name")
#     item["is_type"] = 2
#     try:
#         mq.insert_sql("t_zx_bid_info", item)
#     except:
#         print(item["bid_id"])
#         errlist.append(item["bid_id"])
# print("出错===", errlist)


# ccc = mq.select_sql("t_zx_bid_info", ["id", "bid_html_con"], {"website_name": "国家电网新一代电子商务平台"})
# print(ccc)
# for each in ccc:
#     each_ = each
#     id_ = each_.get("id")
#     print("正在处理===", id_)
#     bid_html_con = each_.get("bid_html_con").replace("'", '"').replace("\n", "").replace("\t", "")
#     bid_html_con = eval(bid_html_con)
#     print(type(bid_html_con))
#
#     bid_html_con_ = str(bid_html_con.get("resultValue").get("notice")).replace("'", '"')
#     bid_content = str(bid_html_con.get("resultValue").get("notice")).replace("'", '"')
#     bid_json_data = str(bid_html_con).replace("'", '"')
#     mq.update_sql(
#         "t_zx_bid_info",
#         {"bid_html_con": bid_html_con_, "bid_json_data": bid_json_data, "bid_content": bid_content},
#         {"id": id_},
#     )
#
# xxx = {"successful": True, "resultValue": {"fileFlag": "1", "notice": {"PURPRJ_NOTICE_DET_ID": None, "CONTACT": "张强", "PURPRJ_STATUS": 130020008, "PURPRJ_NAME": "国网大数据中心2023年第三次服务公开招标采购", "TAX": None, "PRJ_INTRODUCE": None, "PRJ_STATUS": 1, "PURPRJ_ID": 2023062840757076, "CHG_NOTICE_CONT": " ", "PUR_TYPE": 130007002, "ORG_TYPE": 5, "PUBLISH_ORG_NAME": "国网大数据中心", "IS_SELF_EXEC": 1, "PAY_MODE_NAME": "线下支付", "OPENBID_ADDR": "招标人招投标交易平台信息系统", "BID_AGT": "北京华联电力工程监理有限公司", "IMPL_MODE": 130022002, "PUR_TYPE_NAME": "服务", "NOTICE_TYPE": 100063001, "ONLINE_BID_NOTICE_ID": 2023063090331283, "BID_AGT_ADDR": "北京市丰台区南四环西路188号11区2号楼", "PAY_MODE": 130045002, "E_MAIL": "zhangqiang@heesc.com", "BID_AGT_ADDR_ZIP_CODE": "100070", "PURPRJ_CODE": "902305", "NOTICE_TYPE_NAME": "招标公告", "BID_ORG": "国网大数据中心", "OPENBID_TIME": "2023-07-21 09:00:00", "BIDBOOK_BUY_END_TIME": "2023-07-10 16:00:00", "TEL": "010-52262020", "PUB_TIME": "2023-06-30", "BIDBOOK_SELL_BEGIN_TIME": "2023-06-30 14:20:00"}}, "resultHint": "", "errorPage": "", "type": ""}
# print(type(xxx))
# x = [
#     {
#         "id": 51490,
#         "bid_html_con": '{"successful": True, "resultValue": {"fileFlag": "1", "notice": {"PURPRJ_NOTICE_DET_ID": None, "CONTACT": "张强", "PURPRJ_STATUS": 130020008, "PURPRJ_NAME": "国网大数据中心2023年第三次服务公开招标采购", "TAX": None, "PRJ_INTRODUCE": None, "PRJ_STATUS": 1, "PURPRJ_ID": 2023062840757076, "CHG_NOTICE_CONT": " ", "PUR_TYPE": 130007002, "ORG_TYPE": 5, "PUBLISH_ORG_NAME": "国网大数据中心", "IS_SELF_EXEC": 1, "PAY_MODE_NAME": "线下支付", "OPENBID_ADDR": "招标人招投标交易平台信息系统", "BID_AGT": "北京华联电力工程监理有限公司", "IMPL_MODE": 130022002, "PUR_TYPE_NAME": "服务", "NOTICE_TYPE": 100063001, "ONLINE_BID_NOTICE_ID": 2023063090331283, "BID_AGT_ADDR": "北京市丰台区南四环西路188号11区2号楼", "PAY_MODE": 130045002, "E_MAIL": "zhangqiang@heesc.com", "BID_AGT_ADDR_ZIP_CODE": "100070", "PURPRJ_CODE": "902305", "NOTICE_TYPE_NAME": "招标公告", "BID_ORG": "国网大数据中心", "OPENBID_TIME": "2023-07-21 09:00:00", "BIDBOOK_BUY_END_TIME": "2023-07-10 16:00:00", "TEL": "010-52262020", "PUB_TIME": "2023-06-30", "BIDBOOK_SELL_BEGIN_TIME": "2023-06-30 14:20:00"}}, "resultHint": "", "errorPage": "", "type": ""}',
#     }
# ]


xxx = mq.select_sql("t_zx_bid_info", ['bid_id'], {"is_type": "%http%"})
print(xxx)

ccc = set()
for i in xxx:
    ccc.add(i["bid_id"])
print(ccc)


# mq.select_sql("t_zx_bid_info", ['create_datetime'], {"bid_id": })
