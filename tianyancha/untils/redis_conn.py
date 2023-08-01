# -*- coding: utf-8 -*-
# @ Time      : 2023/4/20 14:47
# @ Author    : wym
# @ FileName  : redis_conn.py
# @ SoftWare  : PyCharm
from redis import Redis
from tianyancha.conf.env import *

conn = Redis(host=REDIS_HOST, encoding=REDIS_ENCODING, port=REDIS_PORT, db=REDIS_DB)

r = Redis(
    host=REDIS_HOST,
    encoding=REDIS_ENCODING,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True,
)
