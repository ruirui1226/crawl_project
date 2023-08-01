#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/5/29 17:05
@Author : xushaowei
@File : tyc_distribute_task.py
@Desc :
@Software:PyCharm
"""
import pymysql
from pymysql import IntegrityError
from loguru import logger
from conf.env import *
from untils.redis_conn import r


def task_distribution(table_name, sel_data, where_data, redis_key):
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    data_list = []
    """
    查询
    :param table_name: 表名 str
    :param sel_data: 查询值 list
            [tyc_id, is_zjtx]
    :param where_data: 条件 dict
        {"company_name": "海尔集团公司", "tyc_id": 2315740}
    :param
    """
    try:
        if isinstance(where_data, dict) and isinstance(sel_data, list) and isinstance(table_name, str):
            str_sel = ", ".join(sel_data)
            str_where = "' and ".join([each + " = '" + str(where_data[each]) for each in where_data]) + "'"
            sql = f"""select {str_sel} from {table_name} where {str_where} """
            cursor.execute(sql)
            conn.commit()
            data_list = cursor.fetchall()
        else:
            return "======sql传参错误, 请检查======"
    except IntegrityError as f:
        logger.warning("查询失败")

    for data in data_list:
        r.sadd(redis_key, str(data))
