#!/usr/bin/conf python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/20 09:06
# @Author  : wym
# @File    : pysql.py
import time

import pymysql
from loguru import logger
from tianyancha.conf.env import *
from pymysql import IntegrityError


def get_company_230529_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl=3  order by id desc limit 279,2000"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023'"

    # sql ="select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023'"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_xh ='1'"
    sql = """
            select id, company_name, tyc_id from t_zx_company_tyc_all_infos where is_lz =1 or is_cyl =1 or is_crawl='zjtx_2023' order by id desc
                        """
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023' limit 1153,200000"
    # sql = "select  id,company_name,tyc_id from sheet2"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230420_name_detail():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = """
            select id, company_name, tyc_id, detailbusinessid, businessid from t_zx_tyc_administrative_licensing a
            where a.id not in (select info_id from t_zx_tyc_administrative_licensing_detail)
            """
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_istory_action_at_law_detail():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = """
            select id, company_name, tyc_id, lawsuitUrl from t_zx_history_action_at_law a
            where a.id not in (select info_id from t_zx_history_action_at_law_detail) limit 100
            """
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


class MysqlPipelinePublic(object):
    """
    mondo:
    insert_sql(t_zx_company_tyc_all_infos, {"company_name": "海尔集团公司", "tyc_id": 2315740})
    delete_sql(t_zx_company_tyc_all_infos, {"company_name": "海尔集团公司", "tyc_id": 2315740})
    update_sql(t_zx_company_tyc_all_infos, {"is_zjtx": "123456"}, {"company_name": "海尔集团公司", "tyc_id": 2315740})
    select_sql(t_zx_company_tyc_all_infos, [tyc_id, is_zjtx], {"company_name": "海尔集团公司", "tyc_id": 2315740})
    """

    def __init__(self):
        self.conn = pymysql.connect(
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
        )
        self.cursor = self.conn.cursor()

    def insert_sql(self, table_name, item):
        """
        写入
        :param table_name: 表名 str
        :param item: 条件 dict
            {"company_name": "海尔集团公司", "tyc_id": 2315740}
        """
        try:
            if isinstance(item, dict) and isinstance(table_name, str):
                str_fields = ", ".join([fields for fields, data in item.items()])
                str_data = "'" + "', '".join("%s" % data for fields, data in item.items()) + "'"
                sql = f"""insert into {table_name} ({str_fields}) values ({str_data}) """
                # print("=================================================================",sql)
                try:
                    self.conn.ping()
                except:
                    time.sleep(1)
                    print("*********sql重连**********")
                    self.conn = pymysql.connect(
                        database=DATABASE_NAME,
                        user=DATABASE_USER,
                        password=DATABASE_PASSWORD,
                        host=DATABASE_HOST,
                    )
                    self.cursor = self.conn.cursor()
                self.cursor.execute(sql)
                self.conn.commit()
            else:
                return "======sql传参错误, 请检查======"
        except IntegrityError as f:
            logger.warning(f"写入失败{f}")

    def delete_sql(self, table_name, where_data):
        """
        删除
        :param table_name: 表名 str
        :param where_data: 条件 list
            {"company_name": "海尔集团公司", "tyc_id": 2315740}
        """
        try:
            if isinstance(where_data, dict) and isinstance(table_name, str):
                str_where = "' and ".join([each + " = '" + str(where_data[each]) for each in where_data]) + "'"
                sql = f"""delete from {table_name} where {str_where} """
                self.cursor.execute(sql)
                self.conn.commit()
            else:
                return "======sql传参错误, 请检查======"
        except IntegrityError as f:
            logger.warning(f"删除失败{f}")

    def update_sql(self, table_name, set_data, where_data):
        """
        修改
        :param table_name: 表名 str
        :param set_data: 修改值 dict
        :param where_data: 条件 dict
            {"company_name": "海尔集团公司", "tyc_id": 2315740}
        :param
        """
        try:
            if isinstance(where_data, dict) and isinstance(table_name, str) and isinstance(set_data, dict):
                str_where = "' and ".join([each + " = '" + str(where_data[each]) for each in where_data]) + "'"
                str_set = "', ".join([each + " = '" + str(set_data[each]) for each in set_data]) + "'"
                sql = f"""update {table_name} set {str_set} where {str_where} """
                self.cursor.execute(sql)
                self.conn.commit()
            else:
                return "======sql传参错误, 请检查======"
        except IntegrityError as f:
            logger.warning(f"修改失败{f}")

    def select_sql(self, table_name, sel_data, where_data):
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
            return_data = []
            item = {}
            if isinstance(where_data, dict) and isinstance(sel_data, list) and isinstance(table_name, str):
                str_sel = ", ".join(sel_data)
                str_where = "' and ".join([each + " = '" + str(where_data[each]) for each in where_data]) + "'"
                sql = f"""select {str_sel} from {table_name} where {str_where} """
                print(sql)
                self.cursor.execute(sql)
                self.conn.commit()
                for i in self.cursor.fetchall():
                    item = dict(zip(sel_data, i))
                    return_data.append(item)
                return return_data
            else:
                return "======sql传参错误, 请检查======"
        except IntegrityError as f:
            logger.warning(f"查询失败{f}")

    def insert_all_sql(self, table_name, items):
        """
        批量写入
        :param table_name: 表名 str
        :param items: 条件 list
            [{"company_name": "海尔集团公司", "tyc_id": 2315740}, ...]
        """
        try:
            if isinstance(items, list) and isinstance(table_name, str):
                str_fields = ", ".join([fields for fields, data in items[0].items()])
                str_data = (
                    "'"
                    + "'), ('".join(["', '".join("%s" % data for fields, data in item.items()) for item in items])
                    + "'"
                )
                sql = f"""insert into {table_name} ({str_fields}) values ({str_data}) """
                self.cursor.execute(sql)
                self.conn.commit()
            else:
                return "======sql传参错误, 请检查======"
        except IntegrityError as f:
            logger.warning(f"写入失败{f}")

    def close(self):
        self.cursor.close()
        self.conn.close()
