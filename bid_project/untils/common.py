# -*- coding: utf-8 -*-
# @Time : 2023/6/7 9:24
# @Author: mayj
import hashlib
from urllib.parse import urljoin


def get_md5(key: str):
    """生成MD5,统一id长度"""
    key += "&1234"
    md5_obj = hashlib.md5(key.encode("utf-8"))
    return md5_obj.hexdigest()


def urljoin_url(base_url, url):
    """拼接完整url"""
    if "http" not in url:
        url = urljoin(base_url, url)
    return url
