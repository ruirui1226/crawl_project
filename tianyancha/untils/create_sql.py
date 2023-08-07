#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: 快速建表
@version: python3
@author: shenr
@time: 2023/5/22 
"""
import pymysql
from conf.env import *
from pymysql import IntegrityError
from loguru import logger


class CREATE(object):
    """
    自动建表
    """

    def __init__(self):
        """
        建表之前首先确定目标库
        """
        self.conn = pymysql.connect(
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
        )
        self.cursor = self.conn.cursor()

    def show_sql(self, name_dic):
        """
        判断当前表是否存在
        :param name_dic: {"t_zx_company_main_staff_info": "主要人员"}
        """
        sql_show = f"""show tables like '{list(name_dic.keys())[0]}'"""
        return self.cursor.execute(sql_show)

    def create_sql(self, name_dic, field_dic):
        """
        建表
        :param name_dic: {"t_zx_company_main_staff_info": "主要人员"}
        :param field_dic: {"info_id": "int", "company_name": "varchar(255)", "toco": "varchar(255)", "create_time": "datetime"}
        """
        try:
            if isinstance(name_dic, dict) and isinstance(field_dic, dict):
                if self.show_sql(name_dic):
                    return "======当前表已存在，请勿重复创建======"
                str_ = (
                    ",\n                    ".join([k + "    " + field_dic.get(k) + "    null" for k in field_dic])
                    + ","
                )
                sql_in = (
                    f"""
                    create table {list(name_dic.keys())[0]}
                    (
                    id    int auto_increment comment '主键id'
                    primary key,
                    """
                    + str_
                    + f"""
                    constraint id
                        unique (id)
                    )
                    comment '{list(name_dic.values())[0]}';
                            """
                )
                self.cursor.execute(sql_in)
                # print("=====", sql_in)
                self.conn.commit()
                if self.show_sql(name_dic):
                    return "======创建成功======"
            else:
                return "======sql传参错误, 请检查======"

        except IntegrityError as f:
            logger.warning("======创建失败======")

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    # "mondo"
    name_dic = {"t_xz_tyc_final_beneficiary11": "最终受益人"}
    field_dic = {
        "info_id": "int",
        "servicetype": "varchar(255)",
        "total": "varchar(255)",
        "chainlist": "text",
        "servicecount": "varchar(255)",
        "name": "varchar(255)",
        "u_id": "varchar(255)",
        "type": "varchar(255)",
        "holderid": "varchar(255)",
        "percent": "varchar(255)",
        "cid": "varchar(255)",
        "company_name": "varchar(255)",
        "tyc_id": "varchar(255)",
        "create_time": "varchar(50)",
    }
    aaa = CREATE()
    x = aaa.create_sql(name_dic, field_dic)
    print(x)
