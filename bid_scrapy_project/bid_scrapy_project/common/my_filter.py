# -*- coding: utf-8 -*-
# @Time : 2023/7/13 11:09
# @Author: mayj
"""
    自定义filter方法
"""
import redis
from scrapy.utils.project import get_project_settings
from scrapy.utils.request import request_fingerprint

settings = get_project_settings()


class Request_Fingerprint(object):
    """把url初始化成req对象"""

    def __init__(self, url):
        self.method = "GET"
        self.url = url
        self.body = b""


class Redis_Fingerprint(object):
    def __init__(self):
        self.server = redis.Redis(
            host=settings["REDIS_HOST"],
            port=settings["REDIS_PORT"],
            db=settings["REDIS_PARAMS"]["db"],
            password=settings["REDIS_PARAMS"]["password"],
        )

    def run(self, key, url):
        req_url = Request_Fingerprint(url=url)
        fp = request_fingerprint(req_url)
        # 存在返回True，不存在返回False
        return self.server.sadd(f"{key}:dupefilter", fp) == 0
