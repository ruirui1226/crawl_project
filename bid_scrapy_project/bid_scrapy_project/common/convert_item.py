# -*- coding: utf-8 -*-
# @Time : 2023/7/13 14:15
# @Author: mayj
"""
    转换item字段
"""
keys = {
    "po_id": "bid_id",
    "create_datetime": "create_datetime",
    "bid_url": "bid_url",
    "bid_md5_url": "bid_md5_url",
    "po_province": "bid_province",
    "po_city": "bid_city",
    "po_county": "bid_county",
    "po_zone": "bid_zone",
    "po_category": "bid_category",
    "po_info_type": "bid_info_type",
    "po_source": "bid_source",
    "bo_name": "bid_name",
    "po_public_time": "bid_public_time",
    "po_html_con": "bid_html_con",
    "po_content": "bid_content",
    "po_json_data": "bid_json_data",
    "po_industry": "bid_industry",
    "bid_orgin_url": "bid_orgin_url",
    "description": "description",
    "website_name": "website_name",
    "website_url": "website_url",
}


def convert_data(data):
    """统一item字段"""
    data.pop("list_parse")
    new_data = {"is_type": 1}
    if "bid_id" in str(data):
        new_data = dict(data)
        new_data["is_type"] = 1
        return new_data
    for field, data in data.items():
        new_data[keys[field]] = data
    new_data["is_type"] = 2
    return new_data
