# -*- coding: utf-8 -*-
import hashlib

import pymysql
from loguru import logger
from pymysql import IntegrityError

# from bid_project.conf.env_demo import *


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
            database="hot_list_rankings",
            user="root",
            password="121314",
            host="10.67.78.131",
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
                # print(sql)
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


def get_md5(key: str):
    """生成MD5,统一id长度"""
    key += "&1234"
    md5_obj = hashlib.md5(key.encode("utf-8"))
    return md5_obj.hexdigest()