#!/usr/bin/conf python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/20 09:06
# @Author  : wym
# @File    : pysql.py
import time
from sqlalchemy import create_engine
import pymysql
from loguru import logger
from tianyancha.conf.env import *
from pymysql import IntegrityError


def get_engine():
    return create_engine("mysql+pymysql://root:zxicet@10.67.78.14:DATABASE_PORT/industrial_chain_project?charset=utf8")
    # return pymysql.connect(host=DATABASE_HOST,port=DATABASE_PORT,user=DATABASE_USER,password=DATABASE_PASSWORD,db=DATABASE_NAME)


def get_company_name1():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "select * from t_zx_company_tyc_all_infos_copy1 LIMIT 200,100 ;"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_news_list():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "select id,company_name,tyc_id,uri from t_zx_company_newslist_info;"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_news_list_2():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "select id,company_name,tyc_id,uri from t_zx_company_newslist_info order by id Desc;"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def update_news_detail_info(item):
    try:
        conn = pymysql.connect(
            host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
        )
        cursor = conn.cursor()
        # 第2步：你做的操作
        sql = "select id,company_name,tyc_id,uri from t_zx_company_newslist_info ;"
        cursor.execute(sql)  # 所做的查询操作
        # conn.commit()  # 数据操作的二次确认
        data_list = cursor.fetchall()
        return data_list
    except Exception as e:
        print(e)


def get_company_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    # sql = " select id, company_name, tyc_id from t_zx_company_tyc_all_infos limit 2000"
    sql = " select id, company_name, tyc_id from t_zx_company_tyc_all_infos where is_lz = '1'"
#     sql = """SELECT id, company_name, tyc_id FROM t_zx_company_tyc_all_infos AS A
# WHERE is_cyl = '1' AND A.id NOT IN (SELECT B.info_id FROM t_zx_company_judicial_bankruptcy_info AS B GROUP BY info_id)"""
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_name_base():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = " select * from t_zx_company_list_info_base"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_byd_company_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = " select * from t_zx_byd_company_list_info "
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230201_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = " select   id , company_name, tyc_id from  t_zx_tyc_company_lack_info_230320_copy1 order by id desc "
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230310_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "  select   id , company_name, tyc_id from  t_zx_tyc_company_lack_info_230320_copy1 order by id desc"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


#
def get_company_230321_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    # sql = """  select   id , company_name, tyc_id from  t_zx_company_byd_info_list_0327 where is_byd =0 and company_name like "%汽车%" or company_name like "%电池%" or company_name like "%比亚迪%" """
    sql = """select   id , company_name, tyc_id from  t_zx_company_byd_info_list_0327 limit 10725,60"""
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


# def get_company_230321_name():
#
#     conn = pymysql.connect(
#         host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
#     )
#     cursor = conn.cursor()
#     # 第2步：你做的操作
#     # sql = """  select   id , company_name, tyc_id from  t_zx_company_byd_info_list_0327 where is_byd =0 and company_name like "%汽车%" or company_name like "%电池%" or company_name like "%比亚迪%" """
#     sql = """select   id , company_name, tyc_id from  t_zx_company_byd_info_list_0321 where is_zzjzds = 0"""
#     cursor.execute(sql)  # 所做的查询操作
#     # conn.commit()  # 数据操作的二次确认
#     data_list = cursor.fetchall()
#     return data_list


def get_company_230328_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    # sql = "select id , company_name, tyc_id  from t_zx_dmjb_company_list_info_0328 order by id desc limit 2"
    # sql ="""select id , company_name, tyc_id  from t_zx_dmjb_company_list_info_0328  where tyc_id = '2314116535'"""

    # sql =" "
    sql = """select distinct  id,company_name, tyc_id  from t_zx_list_company_lack_info_0412 limit 139,1000"""

    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_lack_company_0411_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    # sql = "select id , company_name, tyc_id  from t_zx_dmjb_company_list_info_0328 order by id desc limit 2"
    # sql ="""select id , company_name, tyc_id  from t_zx_dmjb_company_list_info_0328  where tyc_id = '2314116535'"""

    # sql =" "
    sql = """select id , zwjc, code,category  from t_zx_lack_list_company_list_info order by id desc """

    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230411_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    # sql = "select id , company_name, tyc_id  from t_zx_dmjb_company_list_info_0328 order by id desc limit 2"
    # sql ="""select id , company_name, tyc_id  from t_zx_dmjb_company_list_info_0328  where tyc_id = '2314116535'"""

    # sql =" "
    sql = """select id , company_name, tyc_id  from t_zx_tyc_lack_company_search_info_0412 where enterprise_name =1"""

    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230328_2_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "select id , company_name, tyc_id  from t_zx_dmjb_company_list_info_0328 order by id desc limit 500 "
    # sql ="""select id , company_name, tyc_id  from t_zx_dmjb_company_list_info_0328 limit 700,10000"""

    # sql =" "
    # sql ="""select id , company_name, tyc_id  from t_zx_lchxlg_company_list_info_0328 """

    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230328_list_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "select id , company_name, tyc_id  from t_zx_list_company_info_0328"

    # sql =" "
    # sql ="""select id , company_name, tyc_id  from t_zx_lchxlg_company_list_info_0328 """

    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230328_1_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "select id , company_name, tyc_id  from t_zx_lchxlg_company_list_info_0328 where tyc_id =2320651117"

    # sql ="""select id , company_name, tyc_id  from t_zx_lchxlg_company_list_info_0328 """

    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230329_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "select * from t_zx_company_tyc_all_infos where tyc_id =2320651117"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230329_2_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "select  id,supplierList_name,supplier_gid from t_zx_company_bid_info_0329 "
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230420_name():
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
            select id, co_name, co_id from company_name_0727_new a
            # where a.id in (select info_id from t_zx_company_holder_info)
            """
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023' limit 1153,200000"
    # sql = "select  id,company_name,tyc_id from sheet2"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


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


def get_qualification_certificate_id():
    """资质证书Id"""
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl=3  order by id desc limit 279,2000"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023'"

    # sql ="select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023'"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_xh ='1'"
    sql = "select  id,company_name,tyc_id,businessId from t_zx_qualification_certificate limit 10"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023' limit 1153,200000"
    # sql = "select  id,company_name,tyc_id from sheet2"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_court_announcement_details_id():
    """历史法院公告详情id"""
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl=3  order by id desc limit 279,2000"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023'"

    # sql ="select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023'"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_xh ='1'"
    sql = "select  id,company_name,tyc_id,uuid from t_zx_history_court_announcement limit 20"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023' limit 1153,200000"
    # sql = "select  id,company_name,tyc_id from sheet2"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_person_subject_to_enforcement_id():
    """历史被执行人id"""
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl=3  order by id desc limit 279,2000"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023'"

    # sql ="select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023'"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_xh ='1'"
    sql = "select  id,company_name,tyc_id,businessId from t_zx_history_person_subject_to_enforcement limit 20"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023' limit 1153,200000"
    # sql = "select  id,company_name,tyc_id from sheet2"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_publicity_of_land_plots_detailes_id():
    """地块公示Id"""
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl=3  order by id desc limit 279,2000"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023'"

    # sql ="select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023'"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_xh ='1'"
    sql = "select  id,company_name,tyc_id,businessId from t_zx_publicity_of_land_plots limit 10"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023' limit 1153,200000"
    # sql = "select  id,company_name,tyc_id from sheet2"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230506_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl=3  order by id desc limit 279,2000"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023'"

    # sql ="select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023'"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_xh ='1'"
    sql = "select  id,company_name,tyc_id from t_zx_company_trademark_info where is_crawl ='yy_jzds' limit 1"
    # sql = "select  id,company_name,tyc_id from t_zx_company_tyc_all_infos where is_crawl ='zjtx_2023' limit 1153,200000"
    # sql = "select  id,company_name,tyc_id from sheet2"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


#
# def get_company_230321_name():
#
#     conn = pymysql.connect(
#         host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
#     )
#     cursor = conn.cursor()
#     # 第2步：你做的操作
#     sql = """  select   id , company_name, tyc_id from  t_zx_company_byd_info_list_0321 where is_zzjzds= 0"""
#
#     cursor.execute(sql)  # 所做的查询操作
#     # conn.commit()  # 数据操作的二次确认
#     data_list = cursor.fetchall()
#     return data_list


def get_company_230324_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "  select   id , company_name, tyc_id from  t_zx_company_byd_info_list_0321"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230322_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "  select   id , company_name, tyc_id from  t_zx_company_byd_info_list_0321 limit 2489,3000"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230322_qichezhizaoye_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "  select   id , company_name, tyc_id from  t_zx_tyc_qichezhizaoye_search_info_2_0321  limit 3750,10000"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_230322_qichezhizaoye_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "  select   id , supplier_name, supplier_graphId from  t_zx_company_supply_info_0322"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_company_qylhh_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = " select * from t_zx_qylhh_company_list_info"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_zjtx_company_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = " select * from t_zx_company_list_info where is_sd =0 "
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_zjtx_company_name_2():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = " select * from t_zx_company_list_info where is_sd =0 order by id desc "
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_all_company_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "select * from t_zx_company_tyc_all_infos where tyc_id =2320651117"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_ss_company_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )

    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "select * from t_zx_company_all_infos  where tyc_id='2334319161'"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def get_staff_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "select * from t_zx_company_main_staff_info_copy1;"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def delete_to_mysql_main_staff(staff_table_id, info_id, staff_name):
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    sql = "delete from  t_zx_company_main_staff_info_copy1 where id ='%s'" % staff_table_id
    cursor.execute(sql)
    logger.warning("%s数据已经删除" % staff_name)
    conn.commit()
    conn.close()


def get_company_wechat_name():
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    # 第2步：你做的操作
    sql = "select * from t_zx_company_infos_copy1 order by id DESC ;"
    cursor.execute(sql)  # 所做的查询操作
    # conn.commit()  # 数据操作的二次确认
    data_list = cursor.fetchall()
    return data_list


def delete_to_mysql_wechat_main(info_id, company_name):
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    sql = "delete from t_zx_company_list_info_1 where id ='%s'" % info_id
    cursor.execute(sql)
    logger.warning("%s数据已经删除" % company_name)
    conn.commit()
    conn.close()


def delete_to_news_info(info_id, company_name):
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    sql = "delete from t_zx_company_list_info_copy1 where id ='%s'" % info_id
    cursor.execute(sql)
    logger.warning("%s数据已经删除" % company_name)
    conn.commit()
    conn.close()


def delete_to_certificate_info(info_id, company_name):
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    sql = "delete from t_zx_company_list_info_base where id ='%s'" % info_id
    cursor.execute(sql)
    logger.warning("%s数据已经删除" % company_name)
    conn.commit()
    conn.close()


# def delete_to_mysql_main(info_id, company_name):
#     conn = pymysql.connect(
#         host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
#     )
#     sql = "delete from  t_zx_company_infos_copy2 where id ='%s'" % info_id
#     cursor.execute(sql)
#     logger.warning("%s数据已经删除" % company_name)
#     conn.commit()
#     conn.close()


def delete_news_list(news_id, company_name):
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    sql = "delete from t_zx_company_newslist_info where id ='%s'" % news_id
    cursor.execute(sql)
    logger.warning("%s数据已经删除" % company_name)
    conn.commit()
    conn.close()


def delete_to_Patent_info_main(info_id, company_name):
    conn = pymysql.connect(
        host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME
    )
    cursor = conn.cursor()
    sql = "delete from t_zx_company_list_info where id ='%s'" % info_id
    cursor.execute(sql)
    logger.warning("%s数据已经删除" % company_name)
    conn.commit()
    conn.close()


def get_company_pdf_info():
    # 第2步：你做的操作
    sql = "select  id, security_code, security_name,title,pdf_url from shanghai_stock_exchange"
    self.cursor.execute(sql)  # 所做的查询操作
    pdf_data_list = self.cursor.fetchall()
    return pdf_data_list


class MysqlPipeline(object):
    # try:

    def __init__(self):
        self.conn = pymysql.connect(
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
        )
        self.cursor = self.conn.cursor()

    # def process_item(self, item):
    #     insert_sql = "INSERT   IGNORE  INTO t_ts_bid_crawl_info (bid_url,bid_category,bid_city,bid_name,bid_public_time,bid_source,bid_info_type,is_active,is_delete)VALUES (%(bid_url)s, %(bid_category)s, %(bid_city)s, %(bid_name)s, %(bid_public_time)s, %(bid_source)s, %(bid_info_type)s,%(is_active)s, %(is_delete)s)"
    #     logger.debug("当前item数据为%s------------->" % item)
    #     self.cursor.execute(insert_sql, item)
    #     self.conn.commit()

    """
                        "info_id": info_id,
                        "company_name": company_name,
                        "toco": staff_info["toco"],
                        "typeSore": staff_info["typeSore"],
                        "name": staff_info["name"],
                        "staff_id": staff_info["id"],
                        "type": staff_info["type"],
                        "create_time":time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.time())))

        """

    def insert_into_main_staff_info(self, item):
        insert_sql = " INSERT INTO t_zx_company_main_staff_info(info_id,company_name,toco,typeSore,name,staff_id,type,create_time )VALUES (%(info_id)s,%(company_name)s,%(toco)s,%(typeSore)s,%(name)s,%(staff_id)s,%(type)s,%(create_time)s)"
        logger.debug("当前item数据为%s------------->" % item)
        self.cursor.execute(insert_sql, item)
        self.conn.commit()

    def get_company_pdf_info(self):
        # 第2步：你做的操作
        sql = (
            "select  id, security_code, security_name,title,pdf_url from shanghai_stock_exchange where pdf_file is null"
        )
        self.cursor.execute(sql)  # 所做的查询操作
        data_list = self.cursor.fetchall()
        return data_list

    def get_company_pdf_info_2(self):
        # 第2步：你做的操作
        sql = "select  id, seccode, secname,title,download_page from shenzhen_stock_exchange where pdf_file is null"
        self.cursor.execute(sql)  # 所做的查询操作
        data_list = self.cursor.fetchall()
        return data_list

    def get_company_jzds_info(self):
        # 第2步：你做的操作
        sql = "select  id, gid,competeOpponentName from t_zx_tyc_jingzhengduishou"
        self.cursor.execute(sql)  # 所做的查询操作
        data_list = self.cursor.fetchall()
        return data_list

    def get_company_search_info(self):
        # 第2步：你做的操作
        sql = "select  id, company_name,tyc_id from t_zx_tyc_zjtx_company_search_info"
        self.cursor.execute(sql)  # 所做的查询操作
        data_list = self.cursor.fetchall()
        return data_list

    def get_company_search_info_2(self):
        # 第2步：你做的操作
        sql = "select  id, company_name,tyc_id from t_zx_zjtx_company_info_2023"
        self.cursor.execute(sql)  # 所做的查询操作
        data_list = self.cursor.fetchall()
        return data_list

    def insert_into_all_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_tyc_all_infos(tyc_id,info_id, historyNames, serviceType, regStatus, estiblishTimeTitleName, emailList, headUrl, phoneList, baiduAuthURLWWW, type, equityUrl, toco, ownId, property3, companyShowBizTypeName, approvedTime, logo, industry2017, bussiness_id, orgNumber, isClaimed, sourceFlag, correctCompanyId, longitude, entityType, companyBizOrgType, realCid, businessScope, taxNumber, portray, haveReport, tags, isBranch, companyId, phoneNumber, serviceCount, taxQualification, categoryScore, isHightTech, name, percentileScore, isMicroEnt, baseInfo, flag, regCapital, staffNumRange, latitude, industry, legalTitleName, regTitleName, updateTimes, legalPersonName, regNumber, creditCode, weibo, fromTime, socialStaffNum, companyOrgType, alias, baiduAuthURLWAP, email, actualCapital, estiblishTime, companyType, regInstitute, companyBizType, regLocation, websiteList, safetype, legalPersonId, updatetime, base, company_name, create_time)VALUES (%(tyc_id)s,%(info_id)s, %(historyNames)s, %(serviceType)s, %(regStatus)s, %(estiblishTimeTitleName)s, %(emailList)s, %(headUrl)s, %(phoneList)s, %(baiduAuthURLWWW)s, %(type)s, %(equityUrl)s, %(toco)s, %(ownId)s, %(property3)s, %(companyShowBizTypeName)s, %(approvedTime)s, %(logo)s, %(industry2017)s, %(bussiness_id)s, %(orgNumber)s, %(isClaimed)s, %(sourceFlag)s, %(correctCompanyId)s, %(longitude)s, %(entityType)s, %(companyBizOrgType)s, %(realCid)s, %(businessScope)s, %(taxNumber)s, %(portray)s, %(haveReport)s, %(tags)s, %(isBranch)s, %(companyId)s, %(phoneNumber)s, %(serviceCount)s, %(taxQualification)s, %(categoryScore)s, %(isHightTech)s, %(name)s, %(percentileScore)s, %(isMicroEnt)s, %(baseInfo)s, %(flag)s, %(regCapital)s, %(staffNumRange)s, %(latitude)s, %(industry)s, %(legalTitleName)s, %(regTitleName)s, %(updateTimes)s, %(legalPersonName)s, %(regNumber)s, %(creditCode)s, %(weibo)s, %(fromTime)s, %(socialStaffNum)s, %(companyOrgType)s, %(alias)s, %(baiduAuthURLWAP)s, %(email)s, %(actualCapital)s, %(estiblishTime)s, %(companyType)s, %(regInstitute)s, %(companyBizType)s, %(regLocation)s, %(websiteList)s, %(safetype)s, %(legalPersonId)s, %(updatetime)s, %(base)s, %(company_name)s, %(create_time)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_holder_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_holder_info_0321(tyc_id,info_id,company_name,toco,amomon,paymet,time,percent,name,holder_id,type,create_time,tagList,total)VALUES (%(tyc_id)s,%(info_id)s,%(company_name)s,%(toco)s,%(amomon)s,%(paymet)s,%(time)s,%(percent)s,%(name)s,%(holder_id)s,%(type)s,%(create_time)s,%(tagList)s,%(total)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except:
            pass

    """
                    "info_id": info_id,
                "publicNum":wechat_info.get("publicNum",""),
                "codeImg":wechat_info.get("codeImg",""),
                "recommend":wechat_info.get("recommend",""),
                "title":wechat_info.get("title",""),
                "titleImgURL":wechat_info.get("titleImgURL",""),
                "titleImgOriginalURL":wechat_info.get("titleImgOriginalURL",""),             
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),


        """

    def insert_into_holder_info_info(self, item):
        # try:
        insert_sql = " INSERT INTO t_zx_company_holder_info(tyc_id,	info_id,	company_name,	create_time,	tagList,	toco,	amount,	name,	capital,	capitalActl,	logo,	holder_id,	type,	shareHolderType,	percent,	hcgid,	finalBenefitShares,	position,	jigouName,	jigouLogo,	jigouId,	productId,	productName,	productLogo,	existHoldingPath,	existBenefitDetail,	serviceType,	serviceCount)VALUES (%(tyc_id)s,	%(info_id)s,	%(company_name)s,	%(create_time)s,	%(tagList)s,	%(toco)s,	%(amount)s,	%(name)s,	%(capital)s,	%(capitalActl)s,	%(logo)s,	%(holder_id)s,	%(type)s,	%(shareHolderType)s,	%(percent)s,	%(hcgid)s,	%(finalBenefitShares)s,	%(position)s,	%(jigouName)s,	%(jigouLogo)s,	%(jigouId)s,	%(productId)s,	%(productName)s,	%(productLogo)s,	%(existHoldingPath)s,	%(existBenefitDetail)s,	%(serviceType)s,	%(serviceCount)s)"
        logger.debug("当前item数据为%s------------->" % item)

        self.cursor.execute(insert_sql, item)
        self.conn.commit()

    # except:
    #     pass

    def insert_into_main_holder_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_main_holder_info(tyc_id,	info_id,	company_name,	create_time,serviceType,	tenTotal,	proportion,	publishDate,	compareChange,	shareType,	holdingChange,	toco,	sorting,	holdingNum,	logo,	details,	main_id,	mtenTotal,	holdingNumWithUnit,	actual,	tenPercent,	holdingChangeWithUnit,	cType,	costEstimation,	tagList,	serviceCount,	shareUnit,	name,	mtenPercent,	graphId,	alias,	companyType)VALUES (%(tyc_id)s,	%(info_id)s,	%(company_name)s,	%(create_time)s,	%(serviceType)s,	%(tenTotal)s,	%(proportion)s,	%(publishDate)s,	%(compareChange)s,	%(shareType)s,	%(holdingChange)s,	%(toco)s,	%(sorting)s,	%(holdingNum)s,	%(logo)s,	%(details)s,	%(main_id)s,	%(mtenTotal)s,	%(holdingNumWithUnit)s,	%(actual)s,	%(tenPercent)s,	%(holdingChangeWithUnit)s,	%(cType)s,	%(costEstimation)s,	%(tagList)s,	%(serviceCount)s,	%(shareUnit)s,	%(name)s,	%(mtenPercent)s,	%(graphId)s,	%(alias)s,	%(companyType)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except:
            pass

    def insert_into_wechat_public_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_wechat_public_info(info_id,company_name,publicNum,codeImg,recommend,title,titleImgURL,titleImgOriginalURL,create_time)VALUES (%(info_id)s,%(company_name)s,%(publicNum)s,%(codeImg)s,%(recommend)s,%(title)s,%(titleImgURL)s,%(titleImgOriginalURL)s,%(create_time)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except:
            pass

    """
                "info_id": info_id,
                "ico":weibi_info.get("ico",""),
                "name":weibi_info.get("name",""),
                "href":weibi_info.get("href",""),
                "info":weibi_info.get("info",""),
                "tags": " ".join([tags for tags in weibi_info.get("tags","")]),
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),

        """

    def insert_into_Weibo_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_weibo_info(info_id,company_name,ico,name,href,info,create_time,tags)VALUES (%(info_id)s,%(company_name)s,%(ico)s,%(name)s,%(href)s,%(info)s,%(create_time)s,%(tags)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except:
            pass

    """

                "info_id": info_id,
                "company_name": company_name,
                "regNo":trademark_info["regNo"],
                "tmPic":trademark_info["tmPic"],
                "appDate": trademark_info["appDate"],
                "tmClass": trademark_info["tmClass"],
                "intClsV2": trademark_info["intClsV2"],
                "intCls": trademark_info["intCls"],
                "applicantCn": trademark_info["applicantCn"],
                "tmName":trademark_info["tmName"],
                "eventTime": trademark_info["eventTime"],
                "trademark_id": trademark_info["id"],
                "category": trademark_info["category"],
                "status": status,

                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),



        """

    def insert_into_Trademark_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_trademark_info(info_id,company_name,regNo,tmPic,appDate,tmClass,intClsV2,intCls,applicantCn,tmName,eventTime,trademark_id,category,status,create_time,tyc_id)VALUES (%(info_id)s,%(company_name)s,%(regNo)s,%(tmPic)s,%(appDate)s,%(tmClass)s,%(intClsV2)s,%(intCls)s,%(applicantCn)s,%(tmName)s,%(eventTime)s,%(trademark_id)s,%(category)s,%(status)s,%(create_time)s,%(tyc_id)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    """
                "info_id": info_id,
                "regtime": copyreg_info["regtime"],
                "publishtime": copyreg_info["publishtime"],
                "businessId": copyreg_info["businessId"],
                "simplename": copyreg_info["simplename"],
                "authorNationality": copyreg_info["authorNationality"],
                "regnum": copyreg_info["regnum"],
                "copyreg_id": copyreg_info["copyreg_id"],
                "fullname": copyreg_info["fullname"],
                "version": copyreg_info["version"],
                "catnum": copyreg_info["catnum"],
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            软件著作权

        """

    def insert_into_historySeniorExecutive_info(self, item):
        """历史高管"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_history_senior_executive(id,info_id,t_id,time,relation,type,name,toco,logo,company_name,tyc_id,create_time,unique_id)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(t_id)s,%(time)s,%(relation)s,%(type)s,%(name)s,%(toco)s,%(logo)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(unique_id)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_investments_abroad_info(self, item):
        """历史对外投资"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_history_investments_abroad(id,info_id,regStatus,amount,estiblishTime,regCapital,jigouId,jigouName,jigouLogo,type,percent,legalPersonName,legalPersonId,name,alias,logo,t_id,personType,graphId,company_name,tyc_id,create_time,unique_id)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(regStatus)s,%(amount)s,%(estiblishTime)s,%(regCapital)s,%(jigouId)s,%(jigouName)s,%(jigouLogo)s,%(type)s,%(percent)s,%(legalPersonName)s,%(legalPersonId)s,%(name)s,%(alias)s,%(logo)s,%(t_id)s,%(personType)s,%(graphId)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(unique_id)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_notice_of_court_session_info(self, item):
        """历史开庭公告"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_history_notice_of_court_session(id,info_id,area,plaintiff,litigant,businessId,court,caseNo,caseReason,contractors,litigant2,courtroom,defendant,identityList,eventTime,explainMessage,t_id,judge,startDate,company_name,tyc_id,create_time,unique_id)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(area)s,%(plaintiff)s,%(litigant)s,%(businessId)s,%(court)s,%(caseNo)s,%(caseReason)s,%(contractors)s,%(litigant2)s,%(courtroom)s,%(defendant)s,%(identityList)s,%(eventTime)s,%(explainMessage)s,%(t_id)s,%(judge)s,%(startDate)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(unique_id)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_court_announcement_info(self, item):
        """历史法院公告"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_history_court_announcement(id, info_id,announce_id,party2StrApp,party1,reason,bltnno,party2,businessId,judgephone,party1StrApp,caseno,identityList,uuid,bltntypename,content,courtcode,province,mobilephone,publishpage,party2Str,publishdate,t_id,party1Str,company_name,tyc_id,create_time,unique_id)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(announce_id)s,%(party2StrApp)s,%(party1)s,%(reason)s,%(bltnno)s,%(party2)s,%(businessId)s,%(judgephone)s,%(party1StrApp)s,%(caseno)s,%(identityList)s,%(uuid)s,%(bltntypename)s,%(content)s,%(courtcode)s,%(province)s,%(mobilephone)s,%(publishpage)s,%(party2Str)s,%(publishdate)s,%(t_id)s,%(party1Str)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(unique_id)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_court_announcement_details_info(self, item):
        """历史法院公告详情"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_history_court_announcement_details(id,info_id,caseCodeList,caseReason,caseTitle,caseType,courtList,hasCaseExplanation,t_id,isCaseClosed,sameSerialCaseCount,trialProcedure,trialProcedureDetail,trialTime,uuid,labels,caseIdentityList,company_name,tyc_id,create_time)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(caseCodeList)s,%(caseReason)s,%(caseTitle)s,%(caseType)s,%(courtList)s,%(hasCaseExplanation)s,%(t_id)s,%(isCaseClosed)s,%(sameSerialCaseCount)s,%(trialProcedure)s,%(trialProcedureDetail)s,%(trialTime)s,%(uuid)s,%(labels)s,%(caseIdentityList)s,%(company_name)s,%(tyc_id)s,%(create_time)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_person_subject_to_enforcement_details_info(self, item):
        """历史被执行人详情"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_history_person_subject_to_enforcement_details(id,info_id,caseCodeList,caseReason,caseTitle,caseType,courtList,hasCaseExplanation,t_id,isCaseClosed,sameSerialCaseCount,trialProcedure,trialProcedureDetail,trialTime,uuid,labels,caseIdentityList,company_name,tyc_id,create_time)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(caseCodeList)s,%(caseReason)s,%(caseTitle)s,%(caseType)s,%(courtList)s,%(hasCaseExplanation)s,%(t_id)s,%(isCaseClosed)s,%(sameSerialCaseCount)s,%(trialProcedure)s,%(trialProcedureDetail)s,%(trialTime)s,%(uuid)s,%(labels)s,%(caseIdentityList)s,%(company_name)s,%(tyc_id)s,%(create_time)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_person_subject_to_enforcement_info(self, item):
        """历史被执行人"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_history_person_subject_to_enforcement(id,info_id,caseCode,partyCardNum,pname,businessId,execCourtName,caseCreateTime,explainMessage,execMoneyUnit,t_id,execMoney,cid,company_name,tyc_id,create_time,unique_id)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(caseCode)s,%(partyCardNum)s,%(pname)s,%(businessId)s,%(execCourtName)s,%(caseCreateTime)s,%(explainMessage)s,%(execMoneyUnit)s,%(t_id)s,%(execMoney)s,%(cid)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(unique_id)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_shareholder_info(self, item):
        """历史股东"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_history_shareholder(id,info_id,tagList,toco,amount,logo,alias,capital,name,startTime,t_id,endTime,type,company_name,tyc_id,create_time,unique_id)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(tagList)s,%(toco)s,%(amount)s,%(logo)s,%(alias)s,%(capital)s,%(name)s,%(startTime)s,%(t_id)s,%(endTime)s,%(type)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(unique_id)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_Intellectual_property_pledged_info(self, item):
        """历史知识产权出质"""
        try:
            insert_sql = """ INSERT INTO t_zx_history_intellectual_property_pledged(info_id,pledgeId,iprCertificateNum,iprName,iprType,pledgorName,pledgeeName,pledgeRegPeriod,state,publicityDate,businessId,pledgorType,pledgeeType,t_id,pledgorCid,pledgeeCid,explainId,explainMessage,explainState,detailList,company_name,tyc_id,create_time,url)
                VALUES 
                (%(info_id)s,%(pledgeId)s,%(iprCertificateNum)s,%(iprName)s,%(iprType)s,%(pledgorName)s,%(pledgeeName)s,%(pledgeRegPeriod)s,%(state)s,%(publicityDate)s,%(businessId)s,%(pledgorType)s,%(pledgeeType)s,%(t_id)s,%(pledgorCid)s,%(pledgeeCid)s,%(explainId)s,%(explainMessage)s,%(explainState)s,%(detailList)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(url)s)"""
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_historical_final_case_info(self, item):
        """历史终本案件"""
        try:
            insert_sql = """ INSERT INTO t_zx_historical_final_case(info_id,zname,execCourtName,caseFinalTime,caseCreateTime,caseCode,execMoney,noExecMoney,execMoneyUnit,noExecMoneyUnit,businessId,company_name,tyc_id,create_time,url,unique_id)
                VALUES 
                (%(info_id)s,%(zname)s,%(execCourtName)s,%(caseFinalTime)s,%(caseCreateTime)s,%(caseCode)s,%(execMoney)s,%(noExecMoney)s,%(execMoneyUnit)s,%(noExecMoneyUnit)s,%(businessId)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(url)s,%(unique_id)s)"""
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_enterprise_market_value_info(self, item):
        """企业市值"""
        try:
            insert_sql = """ INSERT INTO t_zx_enterprise_market_value(info_id,stockcode,stockname,timeshow,fvaluep,tvalue,flowvalue,tvaluep,topenprice,tamount,trange,thighprice,tamounttotal,tchange,tlowprice,pprice,tmaxprice,tminprice,hexm_curPrice,hexm_float_price,hexm_float_rate,stop,stockStatus,marketType,stockType,code_type,graphId,plate_weight_num,onlineIssueDate,listingDate,flag,listingStatus,listingType,company_name,tyc_id,create_time,unique_id)
                VALUES 
                (%(info_id)s,%(stockcode)s,%(stockname)s,%(timeshow)s,%(fvaluep)s,%(tvalue)s,%(flowvalue)s,%(tvaluep)s,%(topenprice)s,%(tamount)s,%(trange)s,%(thighprice)s,%(tamounttotal)s,%(tchange)s,%(tlowprice)s,%(pprice)s,%(tmaxprice)s,%(tminprice)s,%(hexm_curPrice)s,%(hexm_float_price)s,%(hexm_float_rate)s,%(stop)s,%(stockStatus)s,%(marketType)s,%(stockType)s,%(code_type)s,%(graphId)s,%(plate_weight_num)s,%(onlineIssueDate)s,%(listingDate)s,%(flag)s,%(listingStatus)s,%(listingType)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(unique_id)s)"""
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_administrative_penalty_info(self, item):
        """历史行政处罚"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_history_administrative_penalty(info_id,sourceId,detailBusinessId,gid,showTypeName,detailShowType,punishContent,similarId,punishDate,punishReason,punishNumber,haveChange,altInfo,t_id,originalId,similarBusinessId,similarCount,punishDepartment,company_name,tyc_id,create_time,Unique_id)"
                "VALUES "
                "(%(info_id)s,%(sourceId)s,%(detailBusinessId)s,%(gid)s,%(showTypeName)s,%(detailShowType)s,%(punishContent)s,%(similarId)s,%(punishDate)s,%(punishReason)s,%(punishNumber)s,%(haveChange)s,%(altInfo)s,%(t_id)s,%(originalId)s,%(similarBusinessId)s,%(similarCount)s,%(punishDepartment)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(Unique_id)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_history_Legal_representative_info(self, item):
        """历史法定代表人"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_history_legal_representative(id,info_id,t_id,time,relation,type,name,toco,logo,company_name,tyc_id,create_time,unique_id)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(t_id)s,%(time)s,%(relation)s,%(type)s,%(name)s,%(toco)s,%(logo)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(unique_id)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_HistoryActionAtLaw_info(self, item):
        """历史法律诉讼"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_history_action_at_law"
                "(id,info_id,hasCaseExplanation,submittime,casereason,amount,plaintiffList,docid,lawsuitUrl,businessId,title,court,uuid,caseno,url,amountUnit,doctype,judgetime,amountPaperWork,judgment,eventTime,casetype,explainMessage,t_id,defendantList,company_name,tyc_id,create_time,unique_id)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(hasCaseExplanation)s,%(submittime)s,%(casereason)s,%(amount)s,%(plaintiffList)s,%(docid)s,%(lawsuitUrl)s,%(businessId)s,%(title)s,%(court)s,%(uuid)s,%(caseno)s,%(url)s,%(amountUnit)s,%(doctype)s,%(judgetime)s,%(amountPaperWork)s,%(judgment)s,%(eventTime)s,%(casetype)s,%(explainMessage)s,%(t_id)s,%(defendantList)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(unique_id)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_HistoryActionAtLaw_info_detail(self, item):
        """历史法律诉讼"""
        try:
            insert_sql = """
                INSERT INTO t_zx_history_action_at_law_detail(info_id,company_name,tyc_id,court,title,caseno,uuid,url,doctype,lawfirmlist,judgetime,companylist,planintextlist,lawlist,casetype,sourcename,monitorstatus,create_time)
                VALUES(%(info_id)s,%(company_name)s,%(tyc_id)s,%(court)s,%(title)s,%(caseno)s,%(uuid)s,%(url)s,%(doctype)s,%(lawfirmlist)s,%(judgetime)s,%(companylist)s,%(planintextlist)s,%(lawlist)s,%(casetype)s,%(sourcename)s,%(monitorstatus)s,%(create_time)s)
                """
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_breach_of_the_person_subjected_to_execution_info(self, item):
        """历史失信被执行人"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_history_shixinbeizhixingren(info_id,businessentity,areaname,courtname,businessId,unperformPart,staff,type,cpwsUrl,performedPart,iname,disrupttypename,casecode,cardnum,performance,regdate,publishdate,gistunit,duty,explainMessage,gistid,cid,company_name,tyc_id,create_time,t_id,unique_id)"
                "VALUES "
                "(%(info_id)s,%(businessentity)s,%(areaname)s,%(courtname)s,%(businessId)s,%(unperformPart)s,%(staff)s,%(type)s,%(cpwsUrl)s,%(performedPart)s,%(iname)s,%(disrupttypename)s,%(casecode)s,%(cardnum)s,%(performance)s,%(regdate)s,%(publishdate)s,%(gistunit)s,%(duty)s,%(explainMessage)s,%(gistid)s,%(cid)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(t_id)s,%(unique_id)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_CopyrightOfWorks_info(self, item):
        """作品著作权"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_copyright_of_works(id,info_id,type,finishTime,createTime,regnum,fullname,authorNationality,publishtime,regtime,company_name,tyc_id,create_time)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(type)s,%(finishTime)s,%(createTime)s,%(regnum)s,%(fullname)s,%(authorNationality)s,%(publishtime)s,%(regtime)s,%(company_name)s,%(tyc_id)s,%(create_time)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_OnTheList_info(self, item):
        """上榜榜单"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_on_the_list(id,info_id,releaseDate,businessId,inTheListName,pid,source,dataJson,sourceUrl,issueYear,rankingType,name,ranking,detailUrl,t_id,company_name,tyc_id,create_time,gid,unique_id)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(releaseDate)s,%(businessId)s,%(inTheListName)s,%(pid)s,%(source)s,%(dataJson)s,%(sourceUrl)s,%(issueYear)s,%(rankingType)s,%(name)s,%(ranking)s,%(detailUrl)s,%(t_id)s,%(company_name)s,%(tyc_id)s,%(create_time)s,%(gid)s,%(unique_id)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_PublicityOfLandPlots_info(self, item):
        """地块公示"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_publicity_of_land_plots(id,info_id,landAreaUnit,publicationOrganize,landUsefulness,landArea,businessId,administrativeDistrict,landLocation,publicationDate,company_name,tyc_id,create_time)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(landAreaUnit)s,%(publicationOrganize)s,%(landUsefulness)s,%(landArea)s,%(businessId)s,%(administrativeDistrict)s,%(landLocation)s,%(publicationDate)s,%(company_name)s,%(tyc_id)s,%(create_time)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_qualificationCertificate_info(self, item):
        """资质证书"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_qualification_certificate(id,info_id,certNo,endDate,businessId,certificateName,t_id,productNameMaster,startDate,company_name,tyc_id,create_time)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(certNo)s,%(endDate)s,%(businessId)s,%(certificateName)s,%(t_id)s,%(productNameMaster)s,%(startDate)s,%(company_name)s,%(tyc_id)s,%(create_time)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_qualificationCertificate_details_info(self, item):
        """资质证书详情"""
        try:
            insert_sql = (
                " INSERT INTO t_zx_qualification_certificate_details(id,info_id,detail,company_name,tyc_id,create_time)"
                "VALUES "
                "(%(id)s,%(info_id)s,%(detail)s,%(company_name)s,%(tyc_id)s,%(create_time)s)"
            )
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_publicity_of_land_plots_details_info(self, item):
        """地块公示详情"""
        try:
            insert_sql = """ INSERT INTO t_zx_publicity_of_land_plots_details(id,info_id,publicationOrganize,feedbackMethod,postalCode,landArea,contactPerson,remark,landLocation,landAreaAll,electronicMail,landAreaUnit,contactOrganize,landUsefulness,landNum,contactNumber,publicAnnouncementPeriod,organizeLocation,projectName,publicationDate,landuserClean,landuserCleanApp,company_name,tyc_id,create_time)
                VALUES 
                (%(id)s,%(info_id)s,%(publicationOrganize)s,%(feedbackMethod)s,%(postalCode)s,%(landArea)s,%(contactPerson)s,%(remark)s,%(landLocation)s,%(landAreaAll)s,%(electronicMail)s,%(landAreaUnit)s,%(contactOrganize)s,%(landUsefulness)s,%(landNum)s,%(contactNumber)s,%(publicAnnouncementPeriod)s,%(organizeLocation)s,%(projectName)s,%(publicationDate)s,%(landuserClean)s,%(landuserCleanApp)s,%(company_name)s,%(tyc_id)s,%(create_time)s)"""
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_copyReg_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_copyreg_info(tyc_id,info_id,regtime,publishtime,businessId,simplename,authorNationality,regnum,copyreg_id,fullname,version,catnum,company_name,create_time)VALUES (%(tyc_id)s,%(info_id)s,%(regtime)s,%(publishtime)s,%(businessId)s,%(simplename)s,%(authorNationality)s,%(regnum)s,%(copyreg_id)s,%(fullname)s,%(version)s,%(catnum)s,%(company_name)s,%(create_time)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_copyrightworks_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_copyrightworks_info(tyc_id,info_id,regtime,publishtime,businessId,finishTime,authorNationality,regnum,createTime,fullname,company_name,create_time,type)VALUES (%(tyc_id)s,%(info_id)s,%(regtime)s,%(publishtime)s,%(businessId)s,%(finishTime)s,%(authorNationality)s,%(regnum)s,%(createTime)s,%(fullname)s,%(company_name)s,%(create_time)s,%(type)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_publicmsg_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_publicmsg_info(firstImg, title, relevantList, imgsList, orgGidsList, website, eventLabels, abstracts, docid, emotionLabels, rtm, imgsCount, uri, tags_json, labels, comGidsList, hGidsList, info_id, company_name, tyc_id, url, create_time)VALUES (%(firstImg)s,	%(title)s,	%(relevantList)s,	%(imgsList)s,	%(orgGidsList)s,	%(website)s,	%(eventLabels)s,	%(abstracts)s,	%(docid)s,	%(emotionLabels)s,	%(rtm)s,	%(imgsCount)s,	%(uri)s,	%(tags_json)s,	%(labels)s,	%(comGidsList)s,	%(hGidsList)s,	%(info_id)s,	%(company_name)s,	%(tyc_id)s,	%(url)s,	%(create_time)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_Icp_info(self, item):
        """

         "info_id": info_id,
         "webSite":icp_info ["webSite"][0],
         "ym":icp_info["ym"],
         "companyType": icp_info["companyType"],
        "liscense": icp_info["liscense"],
         "companyName": icp_info["companyName"],
         "examineDate":icp_info["examineDate"],
         "businessId": icp_info["businessId"],
         "company_name": company_name,
         "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),


        """
        try:
            insert_sql = " INSERT INTO t_zx_company_icp_info(info_id,webSite,ym,companyType,liscense,companyName,examineDate,businessId,company_name,create_time)VALUES (%(info_id)s,%(webSite)s,%(ym)s,%(companyType)s,%(liscense)s,%(companyName)s,%(examineDate)s,%(businessId)s,%(company_name)s,%(create_time)s)"
            # logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except:
            pass

    def insert_into_Patent_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_patent_info_0321(info_id,	businessId,	title,	patentNum,	uuid,	pubnumber,	applicationTime,	cat,	eventTime,	inventor,	patent_id,	address,	agency,	abstracts,	applicantName,	pubDate,	applicationPublishTime,	appnumber,	patentType,	imgUrl,	mainCatNum,	createTime,	lprs,	patentName,	applicationPublishNum,	allCatNum,lawStatus,	company_name,	create_time)VALUES (%(info_id)s,	%(businessId)s,	%(title)s,	%(patentNum)s,	%(uuid)s,	%(pubnumber)s,	%(applicationTime)s,	%(cat)s,	%(eventTime)s,	%(inventor)s,	%(patent_id)s,	%(address)s,	%(agency)s,	%(abstracts)s,	%(applicantName)s,	%(pubDate)s,	%(applicationPublishTime)s,	%(appnumber)s,	%(patentType)s,	%(imgUrl)s,	%(mainCatNum)s,	%(createTime)s,	%(lprs)s,	%(patentName)s,	%(applicationPublishNum)s,	%(allCatNum)s,%(lawStatus)s,	%(company_name)s,	%(create_time)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except Exception as e:
            logger.warning(e)

    def insert_into_Patent_bc_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_patent_info(tyc_id,info_id,	businessId,	title,	patentNum,	uuid,	pubnumber,	applicationTime,	cat,	eventTime,	inventor,	patent_id,	address,	agency,	abstracts,	applicantName,	pubDate,	applicationPublishTime,	appnumber,	patentType,	imgUrl,	mainCatNum,	createTime,	lprs,	patentName,	applicationPublishNum,	allCatNum,lawStatus,	company_name,	create_time)VALUES (%(tyc_id)s,%(info_id)s,	%(businessId)s,	%(title)s,	%(patentNum)s,	%(uuid)s,	%(pubnumber)s,	%(applicationTime)s,	%(cat)s,	%(eventTime)s,	%(inventor)s,	%(patent_id)s,	%(address)s,	%(agency)s,	%(abstracts)s,	%(applicantName)s,	%(pubDate)s,	%(applicationPublishTime)s,	%(appnumber)s,	%(patentType)s,	%(imgUrl)s,	%(mainCatNum)s,	%(createTime)s,	%(lprs)s,	%(patentName)s,	%(applicationPublishNum)s,	%(allCatNum)s,%(lawStatus)s,	%(company_name)s,	%(create_time)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except Exception as e:
            logger.warning(e)

    def insert_into_Human_info(self, item):
        """ "

        "info_id": info_id,
           "serviceType": human_info.get("serviceType",""),
           "total": human_info.get("total",""),
           # "chainList": [],
           "serviceCount": human_info.get("serviceCount",""),
           "isLegal":human_info.get("isLegal",""),
           "name": human_info.get("name",""),
           "logo": human_info.get("logo",""),
           "id": human_info.get("id",""),
           "type": human_info.get("type",""),
           "holderId": human_info.get("holderId",""),
           "cid": human_info.get("cid",""),
           "company_name": company_name,
           "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),


        """
        try:
            insert_sql = " INSERT INTO t_zx_company_humanholding_info(info_id,	serviceType,	total,	serviceCount,	isLegal,	name,logo,human_id，type,holderId,cid,	company_name,	create_time)VALUES (%(info_id)s,	%(serviceType)s,	%(total)s,	%(serviceCount)s,	%(isLegal)s,	%(name)s,%(logo,%(human_id)s，%(type)s,%(holderId)s,%(cid)s,	%(company_name)s,	%(create_time)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except:
            pass

    # 对外投资

    def insert_into_invest_info(self, item):
        """
            "jigouId": invest_info.get("jigouId", ""),
                "jigouLogo": invest_info.get("jigouLogo", ""),
                "jigouName": invest_info.get("jigouName", ""),
                "legalLogo": invest_info.get("legalLogo", ""),
                "serviceCount": invest_info.get("serviceCount", ""),
                "legalPersonTitle": invest_info.get("legalPersonTitle", ""),

        jigouId,jigouLogo,jigouName,legalLogo,serviceCount,legalPersonTitle
        :param item:
        :return:
        """

        try:
            insert_sql = " INSERT INTO t_zx_company_invest_info(tyc_id,info_id,	regStatus,	regCapital,	source,	pencertileScore,	type,	percent,	productName,	legalPersonName,	orgType,	toco,	creditCode,	alias,	logo,	invest_id,	personType,	amount,	estiblishTime,	productId,	productLogo,	amountSuffix,	business_scope,	legalPersonId,	name,	time,	category,	graphId,	base,	total,	company_name,	create_time,jigouId,jigouLogo,jigouName,legalLogo,serviceCount,legalPersonTitle)VALUES (%(tyc_id)s,%(info_id)s,	%(regStatus)s,	%(regCapital)s,	%(source)s,	%(pencertileScore)s,	%(type)s,	%(percent)s,	%(productName)s,	%(legalPersonName)s,	%(orgType)s,	%(toco)s,	%(creditCode)s,	%(alias)s,	%(logo)s,	%(invest_id)s,	%(personType)s,	%(amount)s,	%(estiblishTime)s,	%(productId)s,	%(productLogo)s,	%(amountSuffix)s,	%(business_scope)s,	%(legalPersonId)s,	%(name)s,	%(time)s,	%(category)s,	%(graphId)s,	%(base)s,	%(total)s,	%(company_name)s,	%(create_time)s,%(jigouId)s,%(jigouLogo)s,%(jigouName)s,%(legalLogo)s,%(serviceCount)s,%(legalPersonTitle)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except Exception as e:
            logger.warning(e)

    # 开庭公告
    def insert_into_announcement_info(self, item):
        # "info_id": info_id,
        # "area": announcement_info.get("area", ""),
        # "plaintiff": " ".join([plaintiff.get("name", "") for plaintiff in announcement_info["plaintiff"]]),
        # "litigant": announcement_info.get("litigant", ""),
        # "businessId": announcement_info.get("businessId", ""),
        # "court": announcement_info.get("court", ""),
        # "caseNo": announcement_info.get("caseNo", ""),
        # "caseReason": announcement_info.get("caseReason", ""),
        # "contractors": announcement_info.get("contractors", ""),
        # "courtroom": announcement_info.get("courtroom", ""),
        # "defendant": " ".join([defendant.get("name", "") for defendant in announcement_info["defendant"]]),
        # "eventTime": announcement_info.get("eventTime", ""),
        # "announcement_id": announcement_info.get("id", ""),
        # "judge": announcement_info.get("judge", ""),
        # "startDate": announcement_info.get("startDate", ""),
        # "total": res_json["data"]["count"],
        # "company_name": company_name,
        # "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),

        # try:

        insert_sql = " INSERT INTO t_zx_company_announcement_info(info_id, tyc_id,	area,	plaintiff,	litigant,	businessId,	court,	caseNo,	caseReason,	contractors, courtroom,	defendant,	eventTime,announcement_id,	judge,	startDate,	total,	company_name)VALUES (%(info_id)s, %(tyc_id)s, %(area)s,	%(plaintiff)s,	%(litigant)s,	%(businessId)s,	%(court)s,	%(caseNo)s,	%(caseReason)s,	%(contractors)s,	%(courtroom)s,	%(defendant)s,	%(eventTime)s,%(announcement_id)s,	%(judge)s,	%(startDate)s,%(total)s,	%(company_name)s)"

        self.cursor.execute(insert_sql, item)
        self.conn.commit()
        # except Exception as e:
        #     logger.warning(e)

    def insert_into_bid_info(self, item):
        # try:
        """
            "supplierList_name":supplierList_name,
        "supplier_gid":supplier_gid,
        "purchaserList_name":purchaserList_name,
        "purchaser_gid":purchaser_gid,

        """

        insert_sql = " INSERT INTO t_zx_company_bid_info(url,supplierList_name,supplier_gid,purchaserList_name,purchaser_gid,tyc_id,area,	bidAmountPaperWork,	publishTime,	infoCategory,	bidAmountCompany,	bidUrl,	businessId,	abs,	link,	bidAmount,	title,	bid_type,	uuid,	proxy,	bid_id,	purchaser_gids,	supplierList,	purchaserList,	info_id,	company_name,	create_time)VALUES (%(url)s,%(supplierList_name)s,%(supplier_gid)s,%(purchaserList_name)s,%(purchaser_gid)s,%(tyc_id)s,%(area)s,	%(bidAmountPaperWork)s,	%(publishTime)s,	%(infoCategory)s,	%(bidAmountCompany)s,	%(bidUrl)s,	%(businessId)s,	%(abs)s,	%(link)s,	%(bidAmount)s,	%(title)s,	%(bid_type)s,	%(uuid)s,	%(proxy)s,	%(bid_id)s,	%(purchaser_gids)s,	%(supplierList)s,	%(purchaserList)s,	%(info_id)s,	%(company_name)s,	%(create_time)s)"

        self.cursor.execute(insert_sql, item)
        self.conn.commit()

    #
    # except Exception as e:
    #     logger.warning(e)

    def insert_into_change_info(self, item):
        insert_sql = " INSERT INTO t_zx_company_change_info(info_id,changeTime,havePsersion,contentAfter,createTime,contentBefore,changeItem,total,company_name,	create_time)VALUES (%(info_id)s,%(changeTime)s,%(havePsersion)s,%(contentAfter)s,%(createTime)s,%(contentBefore)s,%(changeItem)s,%(total)s,	%(company_name)s,	%(create_time)s)"

        self.cursor.execute(insert_sql, item)
        self.conn.commit()

    def insert_into_Bussiness_ss_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_ss_bussiness_base_info(info_id, historyNames, serviceType, regStatus, estiblishTimeTitleName, emailList, headUrl, phoneList, baiduAuthURLWWW, type, equityUrl, toco, ownId, property3, companyShowBizTypeName, approvedTime, logo, industry2017, bussiness_id, orgNumber, isClaimed, sourceFlag, correctCompanyId, longitude, entityType, companyBizOrgType, realCid, businessScope, taxNumber, portray, haveReport, tags, isBranch, companyId, phoneNumber, serviceCount, taxQualification, categoryScore, isHightTech, name, percentileScore, isMicroEnt, baseInfo, flag, regCapital, staffNumRange, latitude, industry, legalTitleName, regTitleName, updateTimes, legalPersonName, regNumber, creditCode, weibo, fromTime, socialStaffNum, companyOrgType, alias, baiduAuthURLWAP, email, actualCapital, estiblishTime, companyType, regInstitute, companyBizType, regLocation, websiteList, safetype, legalPersonId, updatetime, base, company_name, create_time)VALUES (%(info_id)s, %(historyNames)s, %(serviceType)s, %(regStatus)s, %(estiblishTimeTitleName)s, %(emailList)s, %(headUrl)s, %(phoneList)s, %(baiduAuthURLWWW)s, %(type)s, %(equityUrl)s, %(toco)s, %(ownId)s, %(property3)s, %(companyShowBizTypeName)s, %(approvedTime)s, %(logo)s, %(industry2017)s, %(bussiness_id)s, %(orgNumber)s, %(isClaimed)s, %(sourceFlag)s, %(correctCompanyId)s, %(longitude)s, %(entityType)s, %(companyBizOrgType)s, %(realCid)s, %(businessScope)s, %(taxNumber)s, %(portray)s, %(haveReport)s, %(tags)s, %(isBranch)s, %(companyId)s, %(phoneNumber)s, %(serviceCount)s, %(taxQualification)s, %(categoryScore)s, %(isHightTech)s, %(name)s, %(percentileScore)s, %(isMicroEnt)s, %(baseInfo)s, %(flag)s, %(regCapital)s, %(staffNumRange)s, %(latitude)s, %(industry)s, %(legalTitleName)s, %(regTitleName)s, %(updateTimes)s, %(legalPersonName)s, %(regNumber)s, %(creditCode)s, %(weibo)s, %(fromTime)s, %(socialStaffNum)s, %(companyOrgType)s, %(alias)s, %(baiduAuthURLWAP)s, %(email)s, %(actualCapital)s, %(estiblishTime)s, %(companyType)s, %(regInstitute)s, %(companyBizType)s, %(regLocation)s, %(websiteList)s, %(safetype)s, %(legalPersonId)s, %(updatetime)s, %(base)s, %(company_name)s, %(create_time)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except Exception as e:
            logger.debug(e)

    def insert_into_Branch_ss_info(self, item):
        # try:

        insert_sql = " INSERT INTO t_zx_company_ss_branch_info_0306(info_id, legalPersonId, regStatus, estiblishTime, name, alias, branch_id, pencertileScore, personType, category, type, base, legalPersonName, company_name, create_time)VALUES(%(info_id)s, %(legalPersonId)s, %(regStatus)s, %(estiblishTime)s, %(name)s, %(alias)s, %(branch_id)s, %(pencertileScore)s, %(personType)s, %(category)s, %(type)s, %(base)s, %(legalPersonName)s, %(company_name)s, %(create_time)s)"

        self.cursor.execute(insert_sql, item)
        self.conn.commit()
        # except Exception as e:
        #     logger.debug(e)

    def insert_into_Bussiness_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_bussiness_base_info(tyc_id,info_id, historyNames, serviceType, regStatus, estiblishTimeTitleName, emailList, headUrl, phoneList, baiduAuthURLWWW, type, equityUrl, toco, ownId, property3, companyShowBizTypeName, approvedTime, logo, industry2017, bussiness_id, orgNumber, isClaimed, sourceFlag, correctCompanyId, longitude, entityType, companyBizOrgType, realCid, businessScope, taxNumber, portray, haveReport, tags, isBranch, companyId, phoneNumber, serviceCount, taxQualification, categoryScore, isHightTech, name, percentileScore, isMicroEnt, baseInfo, flag, regCapital, staffNumRange, latitude, industry, legalTitleName, regTitleName, updateTimes, legalPersonName, regNumber, creditCode, weibo, fromTime, socialStaffNum, companyOrgType, alias, baiduAuthURLWAP, email, actualCapital, estiblishTime, companyType, regInstitute, companyBizType, regLocation, websiteList, safetype, legalPersonId, updatetime, base, company_name, create_time)VALUES (%(tyc_id)s,%(info_id)s, %(historyNames)s, %(serviceType)s, %(regStatus)s, %(estiblishTimeTitleName)s, %(emailList)s, %(headUrl)s, %(phoneList)s, %(baiduAuthURLWWW)s, %(type)s, %(equityUrl)s, %(toco)s, %(ownId)s, %(property3)s, %(companyShowBizTypeName)s, %(approvedTime)s, %(logo)s, %(industry2017)s, %(bussiness_id)s, %(orgNumber)s, %(isClaimed)s, %(sourceFlag)s, %(correctCompanyId)s, %(longitude)s, %(entityType)s, %(companyBizOrgType)s, %(realCid)s, %(businessScope)s, %(taxNumber)s, %(portray)s, %(haveReport)s, %(tags)s, %(isBranch)s, %(companyId)s, %(phoneNumber)s, %(serviceCount)s, %(taxQualification)s, %(categoryScore)s, %(isHightTech)s, %(name)s, %(percentileScore)s, %(isMicroEnt)s, %(baseInfo)s, %(flag)s, %(regCapital)s, %(staffNumRange)s, %(latitude)s, %(industry)s, %(legalTitleName)s, %(regTitleName)s, %(updateTimes)s, %(legalPersonName)s, %(regNumber)s, %(creditCode)s, %(weibo)s, %(fromTime)s, %(socialStaffNum)s, %(companyOrgType)s, %(alias)s, %(baiduAuthURLWAP)s, %(email)s, %(actualCapital)s, %(estiblishTime)s, %(companyType)s, %(regInstitute)s, %(companyBizType)s, %(regLocation)s, %(websiteList)s, %(safetype)s, %(legalPersonId)s, %(updatetime)s, %(base)s, %(company_name)s, %(create_time)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_Bussiness_qichezhizaoye_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_bussiness_base_info_0322(tyc_id,info_id, historyNames, serviceType, regStatus, estiblishTimeTitleName, emailList, headUrl, phoneList, baiduAuthURLWWW, type, equityUrl, toco, ownId, property3, companyShowBizTypeName, approvedTime, logo, industry2017, bussiness_id, orgNumber, isClaimed, sourceFlag, correctCompanyId, longitude, entityType, companyBizOrgType, realCid, businessScope, taxNumber, portray, haveReport, tags, isBranch, companyId, phoneNumber, serviceCount, taxQualification, categoryScore, isHightTech, name, percentileScore, isMicroEnt, baseInfo, flag, regCapital, staffNumRange, latitude, industry, legalTitleName, regTitleName, updateTimes, legalPersonName, regNumber, creditCode, weibo, fromTime, socialStaffNum, companyOrgType, alias, baiduAuthURLWAP, email, actualCapital, estiblishTime, companyType, regInstitute, companyBizType, regLocation, websiteList, safetype, legalPersonId, updatetime, base, company_name, create_time)VALUES (%(tyc_id)s,%(info_id)s, %(historyNames)s, %(serviceType)s, %(regStatus)s, %(estiblishTimeTitleName)s, %(emailList)s, %(headUrl)s, %(phoneList)s, %(baiduAuthURLWWW)s, %(type)s, %(equityUrl)s, %(toco)s, %(ownId)s, %(property3)s, %(companyShowBizTypeName)s, %(approvedTime)s, %(logo)s, %(industry2017)s, %(bussiness_id)s, %(orgNumber)s, %(isClaimed)s, %(sourceFlag)s, %(correctCompanyId)s, %(longitude)s, %(entityType)s, %(companyBizOrgType)s, %(realCid)s, %(businessScope)s, %(taxNumber)s, %(portray)s, %(haveReport)s, %(tags)s, %(isBranch)s, %(companyId)s, %(phoneNumber)s, %(serviceCount)s, %(taxQualification)s, %(categoryScore)s, %(isHightTech)s, %(name)s, %(percentileScore)s, %(isMicroEnt)s, %(baseInfo)s, %(flag)s, %(regCapital)s, %(staffNumRange)s, %(latitude)s, %(industry)s, %(legalTitleName)s, %(regTitleName)s, %(updateTimes)s, %(legalPersonName)s, %(regNumber)s, %(creditCode)s, %(weibo)s, %(fromTime)s, %(socialStaffNum)s, %(companyOrgType)s, %(alias)s, %(baiduAuthURLWAP)s, %(email)s, %(actualCapital)s, %(estiblishTime)s, %(companyType)s, %(regInstitute)s, %(companyBizType)s, %(regLocation)s, %(websiteList)s, %(safetype)s, %(legalPersonId)s, %(updatetime)s, %(base)s, %(company_name)s, %(create_time)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_Branch_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_branch_info(tyc_id,info_id, legalPersonId, regStatus, estiblishTime, name, alias, branch_id, pencertileScore, personType, category, type, base, legalPersonName, company_name, create_time)VALUES(%(tyc_id)s,%(info_id)s, %(legalPersonId)s, %(regStatus)s, %(estiblishTime)s, %(name)s, %(alias)s, %(branch_id)s, %(pencertileScore)s, %(personType)s, %(category)s, %(type)s, %(base)s, %(legalPersonName)s, %(company_name)s, %(create_time)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_qylhh_Bussiness_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_qylhh_bussiness_base_info(tyc_id,info_id, historyNames, serviceType, regStatus, estiblishTimeTitleName, emailList, headUrl, phoneList, baiduAuthURLWWW, type, equityUrl, toco, ownId, property3, companyShowBizTypeName, approvedTime, logo, industry2017, bussiness_id, orgNumber, isClaimed, sourceFlag, correctCompanyId, longitude, entityType, companyBizOrgType, realCid, businessScope, taxNumber, portray, haveReport, tags, isBranch, companyId, phoneNumber, serviceCount, taxQualification, categoryScore, isHightTech, name, percentileScore, isMicroEnt, baseInfo, flag, regCapital, staffNumRange, latitude, industry, legalTitleName, regTitleName, updateTimes, legalPersonName, regNumber, creditCode, weibo, fromTime, socialStaffNum, companyOrgType, alias, baiduAuthURLWAP, email, actualCapital, estiblishTime, companyType, regInstitute, companyBizType, regLocation, websiteList, safetype, legalPersonId, updatetime, base, company_name, create_time)VALUES (%(tyc_id)s,%(info_id)s, %(historyNames)s, %(serviceType)s, %(regStatus)s, %(estiblishTimeTitleName)s, %(emailList)s, %(headUrl)s, %(phoneList)s, %(baiduAuthURLWWW)s, %(type)s, %(equityUrl)s, %(toco)s, %(ownId)s, %(property3)s, %(companyShowBizTypeName)s, %(approvedTime)s, %(logo)s, %(industry2017)s, %(bussiness_id)s, %(orgNumber)s, %(isClaimed)s, %(sourceFlag)s, %(correctCompanyId)s, %(longitude)s, %(entityType)s, %(companyBizOrgType)s, %(realCid)s, %(businessScope)s, %(taxNumber)s, %(portray)s, %(haveReport)s, %(tags)s, %(isBranch)s, %(companyId)s, %(phoneNumber)s, %(serviceCount)s, %(taxQualification)s, %(categoryScore)s, %(isHightTech)s, %(name)s, %(percentileScore)s, %(isMicroEnt)s, %(baseInfo)s, %(flag)s, %(regCapital)s, %(staffNumRange)s, %(latitude)s, %(industry)s, %(legalTitleName)s, %(regTitleName)s, %(updateTimes)s, %(legalPersonName)s, %(regNumber)s, %(creditCode)s, %(weibo)s, %(fromTime)s, %(socialStaffNum)s, %(companyOrgType)s, %(alias)s, %(baiduAuthURLWAP)s, %(email)s, %(actualCapital)s, %(estiblishTime)s, %(companyType)s, %(regInstitute)s, %(companyBizType)s, %(regLocation)s, %(websiteList)s, %(safetype)s, %(legalPersonId)s, %(updatetime)s, %(base)s, %(company_name)s, %(create_time)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_qylhh_Branch_info(self, item):
        """
        "info_id": info_id,
        "legalPersonId":branchList_info.get("legalPersonId",""),
        "regStatus": branchList_info.get("regStatus",""),
        "estiblishTime": branchList_info.get("estiblishTime",""),
        "name": branchList_info.get("name",""),
        "alias":branchList_info.get("alias",""),
        "branch_id": branchList_info.get("id",""),
        "pencertileScore": branchList_info.get("pencertileScore",""),
        "personType":branchList_info.get("personType",""),
        "category": branchList_info.get("category",""),
        "type":branchList_info.get("type",""),
        "base":branchList_info.get("base",""),
        "legalPersonName":branchList_info.get("legalPersonName",""),
        "company_name": company_name,
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S



        """

        try:
            insert_sql = " INSERT INTO t_zx_company_qylhh_branch_info(tyc_id,info_id, legalPersonId, regStatus, estiblishTime, name, alias, branch_id, pencertileScore, personType, category, type, base, legalPersonName, company_name, create_time)VALUES(%(tyc_id)s,%(info_id)s, %(legalPersonId)s, %(regStatus)s, %(estiblishTime)s, %(name)s, %(alias)s, %(branch_id)s, %(pencertileScore)s, %(personType)s, %(category)s, %(type)s, %(base)s, %(legalPersonName)s, %(company_name)s, %(create_time)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_lawsuitscr_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_lawsuitscr_info_2(info_id,	submittime,	plaintiffsAppV2,	casereason,	defendants,	defendantsAppV2,	docid,	lawsuitUrl,	plaintiffsApp,	businessId,	title,	court,	uuid,	caseno,	url,	doctype,	judgetime,	eventTime,	casetype,	defendantsApp,	lawsuitscr_id,	plaintiffs,	total,	company_name,lawsuitData,	create_time)VALUES(%(info_id)s,	%(submittime)s,	%(plaintiffsAppV2)s,	%(casereason)s,	%(defendants)s,	%(defendantsAppV2)s,	%(docid)s,	%(lawsuitUrl)s,	%(plaintiffsApp)s,	%(businessId)s,	%(title)s,	%(court)s,	%(uuid)s,	%(caseno)s,	%(url)s,	%(doctype)s,	%(judgetime)s,	%(eventTime)s,	%(casetype)s,	%(defendantsApp)s,	%(lawsuitscr_id)s,	%(plaintiffs)s,	%(total)s,	%(company_name)s,%(lawsuitData)s,	%(create_time)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except Exception as e:
            logger.debug(e)

    def insert_into_CourtRegister_info(self, item):
        # try:

        insert_sql = " INSERT INTO t_zx_company_courtregister_info(info_id, plaintiffList, litigantGids, litigant, filingDate, caseStatus, businessId, source, content, caseType, sourceUrl, property2, property1, isDeleted, defendant, juge, startTime, department, area, plaintiff, assistant, updateTime, court, caseNo, caseReason, closeDate, third, createTime, cid, total, company_name, create_time)VALUES(%(info_id)s, %(plaintiffList)s, %(litigantGids)s, %(litigant)s, %(filingDate)s, %(caseStatus)s, %(businessId)s, %(source)s, %(content)s, %(caseType)s, %(sourceUrl)s, %(property2)s, %(property1)s, %(isDeleted)s, %(defendant)s, %(juge)s, %(startTime)s, %(department)s, %(area)s, %(plaintiff)s, %(assistant)s, %(updateTime)s, %(court)s, %(caseNo)s, %(caseReason)s, %(closeDate)s, %(third)s, %(createTime)s, %(cid)s, %(total)s, %(company_name)s, %(create_time)s)"

        self.cursor.execute(insert_sql, item)
        self.conn.commit()
        # except Exception as e:
        #     logger.debug(e)

    def insert_into_findHistoryRongzi_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_findhistoryrongzi_info(info_id, rongzi_id, date, pubTime, newsTitle, round, money, moneyNumber, tzrIds, investorName, investorGid, organizationName, value, valueNumber, share, shareNumber, newsUrl, investId, sourceWeb, createTime, updateTime, isDeleted, companyName, graphId, companyId, orderDate, rongziMap, sharesCode,sharesType, tzrIdsType, company_name, create_time,tyc_id)VALUES(%(info_id)s, %(rongzi_id)s, %(date)s, %(pubTime)s, %(newsTitle)s, %(round)s, %(money)s, %(moneyNumber)s, %(tzrIds)s, %(investorName)s, %(investorGid)s, %(organizationName)s, %(value)s, %(valueNumber)s, %(share)s, %(shareNumber)s, %(newsUrl)s, %(investId)s, %(sourceWeb)s, %(createTime)s, %(updateTime)s, %(isDeleted)s, %(companyName)s, %(graphId)s, %(companyId)s, %(orderDate)s, %(rongziMap)s,%(sharesCode)s,%(sharesType)s, %(tzrIdsType)s, %(company_name)s, %(create_time)s,%(tyc_id)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_findJingping_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_findJingping_info(tyc_id,info_id, jingpin_id, productId, product, jingpinProductId, jingpinProduct, sourceWeb, createTime, updateTime, isDeleted, companyName, graphId, companyId, icon, iconOssPath, yewu, setupDate, date, round, value, hangye, location, jingpinBrandId, portray, portrayStr, logo, alias, company_name, create_time)VALUES(%(tyc_id)s,%(info_id)s, %(jingpin_id)s, %(productId)s, %(product)s, %(jingpinProductId)s, %(jingpinProduct)s, %(sourceWeb)s, %(createTime)s, %(updateTime)s, %(isDeleted)s, %(companyName)s, %(graphId)s, %(companyId)s, %(icon)s, %(iconOssPath)s, %(yewu)s, %(setupDate)s, %(date)s, %(round)s, %(value)s, %(hangye)s, %(location)s, %(jingpinBrandId)s, %(portray)s, %(portrayStr)s, %(logo)s, %(alias)s, %(company_name)s, %(create_time)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_findTeamMember_info(self, item):
        insert_sql = """ INSERT INTO t_zx_company_findteammember_info(info_id,teammember_id, name, title,description, icon, iconOssPath, sourceWeb, createTime, updateTime, isDeleted, isDimission, companyName, graphId, companyId, hid, toco, company_name, create_time)VALUES(%(info_id)s,%(teammember_id)s, %(name)s, %(title)s, %(description)s, %(icon)s, %(iconOssPath)s, %(sourceWeb)s, %(createTime)s, %(updateTime)s, %(isDeleted)s, %(isDimission)s, %(companyName)s, %(graphId)s, %(companyId)s, %(hid)s, %(toco)s, %(company_name)s, %(create_time)s)"""

        self.cursor.execute(insert_sql, item)
        self.conn.commit()

    """
                mq.insert_into_importAndExport_base_info(base_info)
            logger.info("数据 %s 插入成功" % base_info)

            for creditRating_item in creditRating_items:
                mq.insert_into_importAndExport_creditRating_info(creditRating_item)
                logger.info("数据%s 插入成功" % creditRating_item)

            for sanction_item in sanction_items:
                mq.insert_into_importAndExport_sanction_info(sanction_item)
                logger.info("数据%s 插入成功" % sanction_item)



    """

    def insert_into_importAndExport_base_info(self, item):
        insert_sql = """ INSERT INTO t_zx_company_importandexport_base_info(info_id,	types,	specialTradeArea,	industryCategory,	managementCategory,	companyName,	businessId,	crCode,	administrativeDivision,	economicDivision,	companyId,	validityDate,	recordDate,	customsRegisteredAddress,	annualReport,	status,	company_name,	create_time)VALUES(%(info_id)s,	%(types)s,	%(specialTradeArea)s,	%(industryCategory)s,	%(managementCategory)s,	%(companyName)s,	%(businessId)s,	%(crCode)s,	%(administrativeDivision)s,	%(economicDivision)s,	%(companyId)s,	%(validityDate)s,	%(recordDate)s,	%(customsRegisteredAddress)s,	%(annualReport)s,	%(status)s,	%(company_name)s,	%(create_time)s)"""

        self.cursor.execute(insert_sql, item)
        self.conn.commit()

    def insert_into_importAndExport_creditRating_info(self, item):
        insert_sql = """ INSERT INTO t_zx_company_importandexport_creditrating_info(info_id,	authenticationCode,	identificationTime,	creditRating,	company_name,	create_time)VALUES(%(info_id)s,	%(authenticationCode)s,	%(identificationTime)s,	%(creditRating)s,	%(company_name)s,	%(create_time)s)"""

        self.cursor.execute(insert_sql, item)
        self.conn.commit()

    def insert_into_importAndExport_sanction_info(self, item):
        insert_sql = """ INSERT INTO t_zx_company_importandexport_sanction_info(info_id,	gid,	decisionNumber,	penaltyDate,	natureOfCase,	type,	party,	company_name,	create_time)VALUES(%(info_id)s,	%(gid)s,	%(decisionNumber)s,	%(penaltyDate)s,	%(natureOfCase)s,	%(type)s,	%(party)s,	%(company_name)s,	%(create_time)s)"""
        self.cursor.execute(insert_sql, item)
        self.conn.commit()

    def insert_into_zhaopin_info(self, item):
        try:
            insert_sql = """INSERT INTO t_zx_company_zhaopin_info(info_id, education, city, companyName, webInfoPath, source, title, experience, salary, welfare, isPromise, companyGid, welfareList, allDirect, startDate, wapInfoPath, company_name, create_time,tyc_id,url)VALUES (%(info_id)s, %(education)s, %(city)s, %(companyName)s, %(webInfoPath)s, %(source)s, %(title)s, %(experience)s, %(salary)s, %(welfare)s, %(isPromise)s, %(companyGid)s, %(welfareList)s, %(allDirect)s, %(startDate)s, %(wapInfoPath)s, %(company_name)s, %(create_time)s,%(tyc_id)s,%(url)s)"""
            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_related_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_related_report_info(date,related,title,url,info_id,company_name,create_time,old_url)VALUES (%(date)s,%(related)s,%(title)s,%(url)s,%(info_id)s,%(company_name)s,%(create_time)s,%(old_url)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_company_yewu_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_yewu_info(i_id,productId,product,logo,logoOssPath,hangye,detailUrl,yewu,setupDate,gwLink,intro,sourceWeb,createTime,updateTime,isDeleted,companyName,graphId,companyId,brandId,round,base,location,info_id,company_name,create_time)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(
                insert_sql,
                (
                    item["i_id"],
                    item["productId"],
                    item["product"],
                    item["logo"],
                    item["logoOssPath"],
                    item["hangye"],
                    item["detailUrl"],
                    item["yewu"],
                    item["setupDate"],
                    item["gwLink"],
                    item["intro"],
                    item["sourceWeb"],
                    item["createTime"],
                    item["updateTime"],
                    item["isDeleted"],
                    item["companyName"],
                    item["graphId"],
                    item["companyId"],
                    item["brandId"],
                    item["round"],
                    item["base"],
                    item["location"],
                    item["info_id"],
                    item["company_name"],
                    item["create_time"],
                ),
            )
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_purchase_info(self, item):
        try:
            insert_sql = """ INSERT INTO t_zx_company_purchase_info(
             agreementStartTime,chainLink,landLevel,landSourceView,projectLocation,landUseRightPerson,electronicRegulatoryNumber,landUseType,landUsePeriod,transactionPrice,contractedVolumeRate,committedTime,contractDate,authority,category,area,companyList,businessId,district,landSupplyMethod,contractedVolumeRateCeiling,projectName,scheduledCompletion,info_id,company_name,create_time
            )VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(
                insert_sql,
                (
                    item["agreementStartTime"],
                    item["chainLink"],
                    item["landLevel"],
                    item["landSourceView"],
                    item["projectLocation"],
                    item["landUseRightPerson"],
                    item["electronicRegulatoryNumber"],
                    item["landUseType"],
                    item["landUsePeriod"],
                    item["transactionPrice"],
                    item["contractedVolumeRate"],
                    item["committedTime"],
                    item["contractDate"],
                    item["authority"],
                    item["category"],
                    item["area"],
                    str(item["companyList"]),
                    item["businessId"],
                    item["district"],
                    item["landSupplyMethod"],
                    item["contractedVolumeRateCeiling"],
                    item["projectName"],
                    item["scheduledCompletion"],
                    item["info_id"],
                    item["company_name"],
                    item["create_time"],
                ),
            )
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_final_case_info(self, item):
        try:
            insert_sql = """ INSERT INTO t_zx_company_final_case_info(caseCode,caseFinalTime,zhixingId,businessId,caseCreateTime,execCourtName,i_id,execMoney,zname,cid,info_id,company_name,create_time)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(
                insert_sql,
                (
                    item["caseCode"],
                    item["caseFinalTime"],
                    item["zhixingId"],
                    item["businessId"],
                    item["caseCreateTime"],
                    item["execCourtName"],
                    item["i_id"],
                    item["execMoney"],
                    item["zname"],
                    item["cid"],
                    item["info_id"],
                    item["company_name"],
                    item["create_time"],
                ),
            )
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_bond_info(self, item):
        try:
            insert_sql = """ INSERT INTO t_zx_company_bond_info(bondName,bondNum,publisherName,bondType,publishTime,publishExpireTime,bondTimeLimit,bondTradeTime,calInterestType,bondStopTime,creditRatingGov,debtRating,faceValue,refInterestRate,faceInterestRate,realIssuedQuantity,planIssuedQuantity,issuedPrice,interestDiff,faceValueApp,refInterestRateApp,faceInterestRateApp,realIssuedQuantityApp,planIssuedQuantityApp,issuedPriceApp,interestDiffApp,payInterestHZ,startCalInterestTime,exeRightType,exeRightTime,escrowAgent,flowRange,remark,tip,createTime,updateTime,businessId,gid,issuedPriceAll,issuedPriceUnit,planIssuedQuantityAll,planIssuedQuantityUnit,realIssuedQuantityAll,realIssuedQuantityUnit,faceInterestRateAll,faceInterestRateUnit,refInterestRateAll,refInterestRateUnit,faceValueAll,faceValueUnit,isDelete,info_id,company_name,create_time
            )VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(
                insert_sql,
                (
                    item["bondName"],
                    item["bondNum"],
                    item["publisherName"],
                    item["bondType"],
                    item["publishTime"],
                    item["publishExpireTime"],
                    item["bondTimeLimit"],
                    item["bondTradeTime"],
                    item["calInterestType"],
                    item["bondStopTime"],
                    item["creditRatingGov"],
                    item["debtRating"],
                    item["faceValue"],
                    item["refInterestRate"],
                    item["faceInterestRate"],
                    item["realIssuedQuantity"],
                    item["planIssuedQuantity"],
                    item["issuedPrice"],
                    item["interestDiff"],
                    item["faceValueApp"],
                    item["refInterestRateApp"],
                    item["faceInterestRateApp"],
                    item["realIssuedQuantityApp"],
                    item["planIssuedQuantityApp"],
                    item["issuedPriceApp"],
                    item["interestDiffApp"],
                    item["payInterestHZ"],
                    item["startCalInterestTime"],
                    item["exeRightType"],
                    item["exeRightTime"],
                    item["escrowAgent"],
                    item["flowRange"],
                    item["remark"],
                    item["tip"],
                    item["createTime"],
                    item["updateTime"],
                    item["businessId"],
                    item["gid"],
                    item["issuedPriceAll"],
                    item["issuedPriceUnit"],
                    item["planIssuedQuantityAll"],
                    item["planIssuedQuantityUnit"],
                    item["realIssuedQuantityAll"],
                    item["realIssuedQuantityUnit"],
                    item["faceInterestRateAll"],
                    item["faceInterestRateUnit"],
                    item["refInterestRateAll"],
                    item["refInterestRateUnit"],
                    item["faceValueAll"],
                    item["faceValueUnit"],
                    item["isDelete"],
                    item["info_id"],
                    item["company_name"],
                    item["create_time"],
                ),
            )
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_stock_pledge_info(self, item):
        try:
            insert_sql = """ INSERT INTO t_zx_company_stock_pledge_info(shareHolderLogo,startDate,lastValue,graphId,pledgeAmount,status,proOfSelf,businessId,shareHolderId,annDate,shareHolderAlias,companyCount,shareHolderType,endDate,shareHolder,info_id,company_name,create_time
            )VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(
                insert_sql,
                (
                    item["shareHolderLogo"],
                    item["startDate"],
                    item["lastValue"],
                    item["graphId"],
                    item["pledgeAmount"],
                    item["status"],
                    item["proOfSelf"],
                    item["businessId"],
                    item["shareHolderId"],
                    item["annDate"],
                    item["shareHolderAlias"],
                    item["companyCount"],
                    item["shareHolderType"],
                    item["endDate"],
                    item["shareHolder"],
                    item["info_id"],
                    item["company_name"],
                    item["create_time"],
                ),
            )
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_invest_org_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_invest_org_info(jigou_name,area,orgCode,imgPath,orgCodeUrl,`desc`,foundYear,info_id,company_name,create_time)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(
                insert_sql,
                (
                    item["jigou_name"],
                    item["area"],
                    item["orgCode"],
                    item["imgPath"],
                    item["orgCodeUrl"],
                    item["desc"],
                    item["foundYear"],
                    item["info_id"],
                    item["company_name"],
                    item["create_time"],
                ),
            )
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_research_report_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_research_report_info(date,related,title,url,info_id,company_name,create_time)VALUES (%(date)s,%(related)s,%(title)s,%(url)s,%(info_id)s,%(company_name)s,%(create_time)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_stock_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_stock_change_info(company_id,investor_name,publish_time,ratio_after,logo,alias,investor_type,ratio_before,i_id,investor_id,type,change_time,info_id,company_name,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(
                insert_sql,
                (
                    item["company_id"],
                    item["investor_name"],
                    item["publish_time"],
                    item["ratio_after"],
                    item["logo"],
                    item["alias"],
                    item["investor_type"],
                    item["ratio_before"],
                    item["i_id"],
                    item["investor_id"],
                    item["type"],
                    item["change_time"],
                    item["info_id"],
                    item["company_name"],
                    item["create_time"],
                ),
            )
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_holder_list_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_holder_list_info(tagList,toco,capital,companyGraphId,name,capitalActl,alias,i_id,type,info_id,company_name,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(
                insert_sql,
                (
                    str(item["tagList"]),
                    item["toco"],
                    str(item["capital"]),
                    item["companyGraphId"],
                    item["name"],
                    str(item["capitalActl"]),
                    item["alias"],
                    item["i_id"],
                    item["type"],
                    item["info_id"],
                    item["company_name"],
                    item["create_time"],
                ),
            )
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_company_holding_info(self, item):
        """



        "legal_personId": hold_info.get("legalPersonId", ""),
               "reg_status": hold_info.get("regStatus", ""),
               "chain_list": str(hold_info.get("chainList", "")),
               "estiblish_time": hold_info.get("estiblishTime", ""),
               "legal_type": hold_info.get("legalType", ""),
               "reg_capital": hold_info.get("regCapital", ""),
               "name": hold_info.get("name", ""),
               "alias": hold_info.get("alias", ""),
               "logo": hold_info.get("logo", ""),
               "percent": hold_info.get("percent", ""),
               "cid": hold_info.get("cid", ""),
               "legal_person_name": hold_info.get("legalPersonName", ""),
               "info_id": info_id,
               "tyc_id": tyc_id,
               "company_name": company_name,
               "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        """
        try:
            insert_sql = " INSERT INTO t_zx_company_holding_info(legal_personId,reg_status,chain_list,estiblish_time,legal_type,reg_capital,name,alias,logo,percent,cid,legal_person_name,info_id,tyc_id,company_name,create_time)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(
                insert_sql,
                (
                    item["legal_personId"],
                    item["reg_status"],
                    str(item["chain_list"]),
                    item["estiblish_time"],
                    item["legal_type"],
                    item["reg_capital"],
                    item["name"],
                    item["alias"],
                    item["logo"],
                    item["percent"],
                    item["cid"],
                    item["legal_person_name"],
                    item["info_id"],
                    item["tyc_id"],
                    item["company_name"],
                    item["create_time"],
                ),
            )
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_company_check_list_info(self, item):
        try:
            insert_sql = """INSERT INTO t_zx_company_check_list_info(
            checkType,
            checkOrg,
            checkResult,
            info_id,
            company_name,
            create_time
                         )VALUES (%s,%s,%s,%s,%s,%s)"""

            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(
                insert_sql,
                (
                    item["checkType"],
                    item["checkOrg"],
                    item["checkResult"],
                    item["info_id"],
                    item["company_name"],
                    item["create_time"],
                ),
            )
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_company_vendor_info(self, item):
        try:
            insert_sql = """INSERT INTO t_zx_company_vendor_info_0322(
                         summary
                        ,announcement_date
                        ,amt
                        ,companyUrl
                        ,source
                        ,supplier_graphId
                        ,logo
                        ,alias
                        ,supplier_name
                        ,relationship
                        ,category
                        ,client_name
                        ,dataSource
                        ,source_name
                        ,source_seq
                        ,ratio
                        ,info_id
                        ,company_name
                        ,tyc_id
                        ,create_time
            )VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(
                insert_sql,
                (
                    item["summary"],
                    item["announcement_date"],
                    item["amt"],
                    item["companyUrl"],
                    item["source"],
                    item["supplier_graphId"],
                    item["logo"],
                    item["alias"],
                    item["supplier_name"],
                    item["relationship"],
                    item["category"],
                    item["client_name"],
                    item["dataSource"],
                    item["source_name"],
                    item["source_seq"],
                    item["ratio"],
                    item["info_id"],
                    item["company_name"],
                    item["tyc_id"],
                    item["create_time"],
                ),
            )
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_company_supply_qichezhizaoye_info(self, item):
        try:
            insert_sql = """INSERT INTO t_zx_company_supply_info_0322(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,	bid_url_app,	alias,	bid_uuid,	logo)VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,	%(bid_url_app)s,	%(alias)s,	%(bid_uuid)s,	%(logo)s)"""
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_company_supply_info(self, item):
        try:
            insert_sql = """INSERT INTO t_zx_company_supply_info(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,	bid_url_app,	alias,	bid_uuid,	logo)VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,	%(bid_url_app)s,	%(alias)s,	%(bid_uuid)s,	%(logo)s)"""
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_company_supply_2_info(self, item):
        try:
            insert_sql = """INSERT INTO t_zx_company_supply_info_0329(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,	bid_url_app,	alias,	bid_uuid,	logo)VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,	%(bid_url_app)s,	%(alias)s,	%(bid_uuid)s,	%(logo)s)"""
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_productquality_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_productquality_info(releaseDate,productName,specification,productionDate,checkResult,disqualification,inspectionOrg,info_id,company_name,create_time)VALUES (%(releaseDate)s,%(productName)s,%(specification)s,%(productionDate)s,%(checkResult)s,%(disqualification)s,%(inspectionOrg)s,%(info_id)s,%(company_name)s,%(create_time)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_company_base_info(self, item):
        try:
            insert_sql = " INSERT INTO  t_zx_company_base_info(info_id,	history_name,	create_time,	reg_status,	estiblishTimeTitleName,	websiteRiskType,	other_e_mail,	other_mobile,	videoId,	baiduAuthURLWWW,	base_type,	inverstStatus,	equity_link,	legal_rep_type,	sensitiveEntityType,	english_name,	co_type_name,	co_type_scale,	co_synopsis,	appro_date,	industry_name,	logo_link,	base_id,	originalPercentileScore,	org_code,	isClaimed,	listedStatusTypeForSenior,	longitude,	tax_bank_mobile,	tax_bank,	entityType,	companyBizOrgType,	bus_scope,	taxpayer_no,	portray,	regCapitalCurrency,	tags,	regCapitalAmount,	mobile,	taxpayer_qualification,	co_names,	percentileScore,	extraInfo,	base_info,	reg_amount,	regLocationTitle,	staffNumRange,	latitude,	link,	industry,	legalTitleName,	regTitleName,	updateTimes,	legal_rep,	tagListV2,	reg_no,	social_credit_code,	pv_count,	fromTime,	insured_quantity,	companyOrgType,	co_alias,	actualCapitalCurrency,	baiduAuthURLWAP,	office_address,	claimLabelStyle,	e_mail,	paid_amount,	hasVideo,	phoneSourceList,	start_date,	tax_bank_account,	reg_authority,	listedStatusType,	companyBizType,	reg_address,	regCapitalAmountUnit,	fund_info,	co_website,	safetype,	tagList,	legal_rep_code,	complexName,	companyProfileRichText,	updatetime,	province_pysx,	tyc_id,	company_name)VALUES (%(info_id)s,	%(history_name)s,	%(create_time)s,	%(reg_status)s,	%(estiblishTimeTitleName)s,	%(websiteRiskType)s,	%(other_e_mail)s,	%(other_mobile)s,	%(videoId)s,	%(baiduAuthURLWWW)s,	%(base_type)s,	%(inverstStatus)s,	%(equity_link)s,	%(legal_rep_type)s,	%(sensitiveEntityType)s,	%(english_name)s,	%(co_type_name)s,	%(co_type_scale)s,	%(co_synopsis)s,	%(appro_date)s,	%(industry_name)s,	%(logo_link)s,	%(base_id)s,	%(originalPercentileScore)s,	%(org_code)s,	%(isClaimed)s,	%(listedStatusTypeForSenior)s,	%(longitude)s,	%(tax_bank_mobile)s,	%(tax_bank)s,	%(entityType)s,	%(companyBizOrgType)s,	%(bus_scope)s,	%(taxpayer_no)s,	%(portray)s,	%(regCapitalCurrency)s,	%(tags)s,	%(regCapitalAmount)s,	%(mobile)s,	%(taxpayer_qualification)s,	%(co_names)s,	%(percentileScore)s,	%(extraInfo)s,	%(base_info)s,	%(reg_amount)s,	%(regLocationTitle)s,	%(staffNumRange)s,	%(latitude)s,	%(link)s,	%(industry)s,	%(legalTitleName)s,	%(regTitleName)s,	%(updateTimes)s,	%(legal_rep)s,	%(tagListV2)s,	%(reg_no)s,	%(social_credit_code)s,	%(pv_count)s,	%(fromTime)s,	%(insured_quantity)s,	%(companyOrgType)s,	%(co_alias)s,	%(actualCapitalCurrency)s,	%(baiduAuthURLWAP)s,	%(office_address)s,	%(claimLabelStyle)s,	%(e_mail)s,	%(paid_amount)s,	%(hasVideo)s,	%(phoneSourceList)s,	%(start_date)s,	%(tax_bank_account)s,	%(reg_authority)s,	%(listedStatusType)s,	%(companyBizType)s,	%(reg_address)s,	%(regCapitalAmountUnit)s,	%(fund_info)s,	%(co_website)s,	%(safetype)s,	%(tagList)s,	%(legal_rep_code)s,	%(complexName)s,	%(companyProfileRichText)s,	%(updatetime)s,	%(province_pysx)s,	%(tyc_id)s,	%(company_name)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    # def insert_into_company_base_2_info(self, item):
    #     try:
    #         insert_sql = " INSERT INTO  ss (info_id,	history_name,	create_time,	reg_status,	estiblishTimeTitleName,	websiteRiskType,	other_e_mail,	other_mobile,	videoId,	baiduAuthURLWWW,	base_type,	inverstStatus,	equity_link,	legal_rep_type,	sensitiveEntityType,	english_name,	co_type_name,	co_type_scale,	co_synopsis,	appro_date,	industry_name,	logo_link,	base_id,	originalPercentileScore,	org_code,	isClaimed,	listedStatusTypeForSenior,	longitude,	tax_bank_mobile,	tax_bank,	entityType,	companyBizOrgType,	bus_scope,	taxpayer_no,	portray,	regCapitalCurrency,	tags,	regCapitalAmount,	mobile,	taxpayer_qualification,	co_names,	percentileScore,	extraInfo,	base_info,	reg_amount,	regLocationTitle,	staffNumRange,	latitude,	link,	industry,	legalTitleName,	regTitleName,	updateTimes,	legal_rep,	tagListV2,	reg_no,	social_credit_code,	pv_count,	fromTime,	insured_quantity,	companyOrgType,	co_alias,	actualCapitalCurrency,	baiduAuthURLWAP,	office_address,	claimLabelStyle,	e_mail,	paid_amount,	hasVideo,	phoneSourceList,	start_date,	tax_bank_account,	reg_authority,	listedStatusType,	companyBizType,	reg_address,	regCapitalAmountUnit,	fund_info,	co_website,	safetype,	tagList,	legal_rep_code,	complexName,	companyProfileRichText,	updatetime,	province_pysx,	tyc_id,	company_name)VALUES (%(info_id)s,	%(history_name)s,	%(create_time)s,	%(reg_status)s,	%(estiblishTimeTitleName)s,	%(websiteRiskType)s,	%(other_e_mail)s,	%(other_mobile)s,	%(videoId)s,	%(baiduAuthURLWWW)s,	%(base_type)s,	%(inverstStatus)s,	%(equity_link)s,	%(legal_rep_type)s,	%(sensitiveEntityType)s,	%(english_name)s,	%(co_type_name)s,	%(co_type_scale)s,	%(co_synopsis)s,	%(appro_date)s,	%(industry_name)s,	%(logo_link)s,	%(base_id)s,	%(originalPercentileScore)s,	%(org_code)s,	%(isClaimed)s,	%(listedStatusTypeForSenior)s,	%(longitude)s,	%(tax_bank_mobile)s,	%(tax_bank)s,	%(entityType)s,	%(companyBizOrgType)s,	%(bus_scope)s,	%(taxpayer_no)s,	%(portray)s,	%(regCapitalCurrency)s,	%(tags)s,	%(regCapitalAmount)s,	%(mobile)s,	%(taxpayer_qualification)s,	%(co_names)s,	%(percentileScore)s,	%(extraInfo)s,	%(base_info)s,	%(reg_amount)s,	%(regLocationTitle)s,	%(staffNumRange)s,	%(latitude)s,	%(link)s,	%(industry)s,	%(legalTitleName)s,	%(regTitleName)s,	%(updateTimes)s,	%(legal_rep)s,	%(tagListV2)s,	%(reg_no)s,	%(social_credit_code)s,	%(pv_count)s,	%(fromTime)s,	%(insured_quantity)s,	%(companyOrgType)s,	%(co_alias)s,	%(actualCapitalCurrency)s,	%(baiduAuthURLWAP)s,	%(office_address)s,	%(claimLabelStyle)s,	%(e_mail)s,	%(paid_amount)s,	%(hasVideo)s,	%(phoneSourceList)s,	%(start_date)s,	%(tax_bank_account)s,	%(reg_authority)s,	%(listedStatusType)s,	%(companyBizType)s,	%(reg_address)s,	%(regCapitalAmountUnit)s,	%(fund_info)s,	%(co_website)s,	%(safetype)s,	%(tagList)s,	%(legal_rep_code)s,	%(complexName)s,	%(companyProfileRichText)s,	%(updatetime)s,	%(province_pysx)s,	%(tyc_id)s,	%(company_name)s)"
    #         logger.debug("当前item数据为%s------------->" % item)
    #
    #         self.cursor.execute(insert_sql, item)
    #         self.conn.commit()
    #     except IntegrityError as f:
    #         logger.warning("数据重复")

    def insert_into_company_qichezhizaoye_base_info(self, item):
        try:
            insert_sql = " INSERT INTO  t_zx_company_base_info_0322 (info_id,	history_name,	create_time,	reg_status,	estiblishTimeTitleName,	websiteRiskType,	other_e_mail,	other_mobile,	videoId,	baiduAuthURLWWW,	base_type,	inverstStatus,	equity_link,	legal_rep_type,	sensitiveEntityType,	english_name,	co_type_name,	co_type_scale,	co_synopsis,	appro_date,	industry_name,	logo_link,	base_id,	originalPercentileScore,	org_code,	isClaimed,	listedStatusTypeForSenior,	longitude,	tax_bank_mobile,	tax_bank,	entityType,	companyBizOrgType,	bus_scope,	taxpayer_no,	portray,	regCapitalCurrency,	tags,	regCapitalAmount,	mobile,	taxpayer_qualification,	co_names,	percentileScore,	extraInfo,	base_info,	reg_amount,	regLocationTitle,	staffNumRange,	latitude,	link,	industry,	legalTitleName,	regTitleName,	updateTimes,	legal_rep,	tagListV2,	reg_no,	social_credit_code,	pv_count,	fromTime,	insured_quantity,	companyOrgType,	co_alias,	actualCapitalCurrency,	baiduAuthURLWAP,	office_address,	claimLabelStyle,	e_mail,	paid_amount,	hasVideo,	phoneSourceList,	start_date,	tax_bank_account,	reg_authority,	listedStatusType,	companyBizType,	reg_address,	regCapitalAmountUnit,	fund_info,	co_website,	safetype,	tagList,	legal_rep_code,	complexName,	companyProfileRichText,	updatetime,	province_pysx,	tyc_id,	company_name)VALUES (%(info_id)s,	%(history_name)s,	%(create_time)s,	%(reg_status)s,	%(estiblishTimeTitleName)s,	%(websiteRiskType)s,	%(other_e_mail)s,	%(other_mobile)s,	%(videoId)s,	%(baiduAuthURLWWW)s,	%(base_type)s,	%(inverstStatus)s,	%(equity_link)s,	%(legal_rep_type)s,	%(sensitiveEntityType)s,	%(english_name)s,	%(co_type_name)s,	%(co_type_scale)s,	%(co_synopsis)s,	%(appro_date)s,	%(industry_name)s,	%(logo_link)s,	%(base_id)s,	%(originalPercentileScore)s,	%(org_code)s,	%(isClaimed)s,	%(listedStatusTypeForSenior)s,	%(longitude)s,	%(tax_bank_mobile)s,	%(tax_bank)s,	%(entityType)s,	%(companyBizOrgType)s,	%(bus_scope)s,	%(taxpayer_no)s,	%(portray)s,	%(regCapitalCurrency)s,	%(tags)s,	%(regCapitalAmount)s,	%(mobile)s,	%(taxpayer_qualification)s,	%(co_names)s,	%(percentileScore)s,	%(extraInfo)s,	%(base_info)s,	%(reg_amount)s,	%(regLocationTitle)s,	%(staffNumRange)s,	%(latitude)s,	%(link)s,	%(industry)s,	%(legalTitleName)s,	%(regTitleName)s,	%(updateTimes)s,	%(legal_rep)s,	%(tagListV2)s,	%(reg_no)s,	%(social_credit_code)s,	%(pv_count)s,	%(fromTime)s,	%(insured_quantity)s,	%(companyOrgType)s,	%(co_alias)s,	%(actualCapitalCurrency)s,	%(baiduAuthURLWAP)s,	%(office_address)s,	%(claimLabelStyle)s,	%(e_mail)s,	%(paid_amount)s,	%(hasVideo)s,	%(phoneSourceList)s,	%(start_date)s,	%(tax_bank_account)s,	%(reg_authority)s,	%(listedStatusType)s,	%(companyBizType)s,	%(reg_address)s,	%(regCapitalAmountUnit)s,	%(fund_info)s,	%(co_website)s,	%(safetype)s,	%(tagList)s,	%(legal_rep_code)s,	%(complexName)s,	%(companyProfileRichText)s,	%(updatetime)s,	%(province_pysx)s,	%(tyc_id)s,	%(company_name)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    # def insert_into_company_base_info(self, item):
    #     try:
    #         insert_sql = " INSERT INTO  t_zx_company_base_info_0321 (info_id,	history_name,	create_time,	reg_status,	estiblishTimeTitleName,	websiteRiskType,	other_e_mail,	other_mobile,	videoId,	baiduAuthURLWWW,	base_type,	inverstStatus,	equity_link,	legal_rep_type,	sensitiveEntityType,	english_name,	co_type_name,	co_type_scale,	co_synopsis,	appro_date,	industry_name,	logo_link,	base_id,	originalPercentileScore,	org_code,	isClaimed,	listedStatusTypeForSenior,	longitude,	tax_bank_mobile,	tax_bank,	entityType,	companyBizOrgType,	bus_scope,	taxpayer_no,	portray,	regCapitalCurrency,	tags,	regCapitalAmount,	mobile,	taxpayer_qualification,	co_names,	percentileScore,	extraInfo,	base_info,	reg_amount,	regLocationTitle,	staffNumRange,	latitude,	link,	industry,	legalTitleName,	regTitleName,	updateTimes,	legal_rep,	tagListV2,	reg_no,	social_credit_code,	pv_count,	fromTime,	insured_quantity,	companyOrgType,	co_alias,	actualCapitalCurrency,	baiduAuthURLWAP,	office_address,	claimLabelStyle,	e_mail,	paid_amount,	hasVideo,	phoneSourceList,	start_date,	tax_bank_account,	reg_authority,	listedStatusType,	companyBizType,	reg_address,	regCapitalAmountUnit,	fund_info,	co_website,	safetype,	tagList,	legal_rep_code,	complexName,	companyProfileRichText,	updatetime,	province_pysx,	tyc_id,	company_name)VALUES (%(info_id)s,	%(history_name)s,	%(create_time)s,	%(reg_status)s,	%(estiblishTimeTitleName)s,	%(websiteRiskType)s,	%(other_e_mail)s,	%(other_mobile)s,	%(videoId)s,	%(baiduAuthURLWWW)s,	%(base_type)s,	%(inverstStatus)s,	%(equity_link)s,	%(legal_rep_type)s,	%(sensitiveEntityType)s,	%(english_name)s,	%(co_type_name)s,	%(co_type_scale)s,	%(co_synopsis)s,	%(appro_date)s,	%(industry_name)s,	%(logo_link)s,	%(base_id)s,	%(originalPercentileScore)s,	%(org_code)s,	%(isClaimed)s,	%(listedStatusTypeForSenior)s,	%(longitude)s,	%(tax_bank_mobile)s,	%(tax_bank)s,	%(entityType)s,	%(companyBizOrgType)s,	%(bus_scope)s,	%(taxpayer_no)s,	%(portray)s,	%(regCapitalCurrency)s,	%(tags)s,	%(regCapitalAmount)s,	%(mobile)s,	%(taxpayer_qualification)s,	%(co_names)s,	%(percentileScore)s,	%(extraInfo)s,	%(base_info)s,	%(reg_amount)s,	%(regLocationTitle)s,	%(staffNumRange)s,	%(latitude)s,	%(link)s,	%(industry)s,	%(legalTitleName)s,	%(regTitleName)s,	%(updateTimes)s,	%(legal_rep)s,	%(tagListV2)s,	%(reg_no)s,	%(social_credit_code)s,	%(pv_count)s,	%(fromTime)s,	%(insured_quantity)s,	%(companyOrgType)s,	%(co_alias)s,	%(actualCapitalCurrency)s,	%(baiduAuthURLWAP)s,	%(office_address)s,	%(claimLabelStyle)s,	%(e_mail)s,	%(paid_amount)s,	%(hasVideo)s,	%(phoneSourceList)s,	%(start_date)s,	%(tax_bank_account)s,	%(reg_authority)s,	%(listedStatusType)s,	%(companyBizType)s,	%(reg_address)s,	%(regCapitalAmountUnit)s,	%(fund_info)s,	%(co_website)s,	%(safetype)s,	%(tagList)s,	%(legal_rep_code)s,	%(complexName)s,	%(companyProfileRichText)s,	%(updatetime)s,	%(province_pysx)s,	%(tyc_id)s,	%(company_name)s)"
    #         logger.debug("当前item数据为%s------------->" % item)
    #
    #         self.cursor.execute(insert_sql, item)
    #         self.conn.commit()
    #     except IntegrityError as f:
    #         logger.warning("数据重复")

    def insert_into_patent_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_patent_info_new_data(info_id,	agent,	relatedCount,	businessId,	title,	patentNum,	uuid,	pubnumber,	applicationTime,	cat,	applicantname,	eventTime,	inventor,	patent_id,	address,	agency,	applicant_Name,	pubDate,	applicationPublishTime,	lprsLabel,	appnumber,	patentType,	imgUrl,	mainCatNum,	createTime,	lprs,	patentName,	applicationPublishNum,	allCatNum,	company_name,	create_time)VALUES (%(info_id)s,	%(agent)s,	%(relatedCount)s,	%(businessId)s,	%(title)s,	%(patentNum)s,	%(uuid)s,	%(pubnumber)s,	%(applicationTime)s,	%(cat)s,	%(applicantname)s,	%(eventTime)s,	%(inventor)s,	%(patent_id)s,	%(address)s,	%(agency)s,	%(applicant_Name)s,	%(pubDate)s,	%(applicationPublishTime)s,	%(lprsLabel)s,	%(appnumber)s,	%(patentType)s,	%(imgUrl)s,	%(mainCatNum)s,	%(createTime)s,	%(lprs)s,	%(patentName)s,	%(applicationPublishNum)s,	%(allCatNum)s,	%(company_name)s,	%(create_time)s)"
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_News_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_newslist_info(firstImg,	title,	relevantList,	imgsList,	orgGidsList,	website,	eventLabels,	abstracts,	docid,	emotionLabels,	rtm,	imgsCount,	uri,	tags_json,	labels,	comGidsList,	hGidsList,	company_name,	tyc_id,	info_id,	create_time)VALUES (%(firstImg)s,	%(title)s,	%(relevantList)s,	%(imgsList)s,	%(orgGidsList)s,	%(website)s,	%(eventLabels)s,	%(abstracts)s,	%(docid)s,	%(emotionLabels)s,	%(rtm)s,	%(imgsCount)s,	%(uri)s,	%(tags_json)s,	%(labels)s,	%(comGidsList)s,	%(hGidsList)s,	%(company_name)s,	%(tyc_id)s,	%(info_id)s,	%(create_time)s) "
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_news_detail_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_news_detail(news_id,	company_name,	tyc_id,	title,	author,	publish_time,	content,	images,create_time,uri)VALUES (%(news_id)s,	%(company_name)s,	%(tyc_id)s,	%(title)s,	%(author)s,	%(publish_time)s,	%(content)s,	%(images)s,%(create_time)s,%(uri)s)"
            # logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_certificate_file_info(self, item):
        try:
            insert_sql = "insert into t_zx_tyc_certificate_file (info_id,tyc_id,company_name,create_time,cert_no,end_date,business_id,certificate_name,id,product_name_master,start_date) VALUES (%(info_id)s,%(tyc_id)s,%(company_name)s,%(create_time)s,%(cert_no)s,%(end_date)s,%(business_id)s,%(certificate_name)s,%(id)s,%(product_name_master)s,%(start_date)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_appbkinfo_info(self, item):
        try:
            insert_sql = "insert into t_zx_tyc_appbkinfo_file(info_id,	brief,	classes,	businessId,	icon,	name,	filterName,	type,	uuid,	company_name,	create_time,tyc_id) VALUES (%(info_id)s,	%(brief)s,	%(classes)s,	%(businessId)s,	%(icon)s,	%(name)s,	%(filterName)s,	%(type)s,	%(uuid)s,	%(company_name)s,	%(create_time)s,%(tyc_id)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_summaryList_info(self, item):
        try:
            insert_sql = "insert into t_zx_tyc_summary_list_file(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,bid_url_app,alias,bid_uuid) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,%(bid_url_app)s,%(alias)s,%(bid_uuid)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_summaryList_2_info(self, item):
        try:
            insert_sql = "insert into t_zx_tyc_summary_list_file_0329(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,bid_url_app,alias,bid_uuid) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,%(bid_url_app)s,%(alias)s,%(bid_uuid)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_summaryList_qichezhizaoye_info(self, item):
        try:
            insert_sql = "insert into t_zx_tyc_summary_list_file_0322(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,bid_url_app,alias,bid_uuid) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,%(bid_url_app)s,%(alias)s,%(bid_uuid)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_summaryList_qichezhizaoye_info(self, item):
        try:
            insert_sql = "insert into t_zx_tyc_summary_list_file_0322(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,bid_url_app,alias,bid_uuid) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,%(bid_url_app)s,%(alias)s,%(bid_uuid)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_qichezhizaoye_search_info(self, item):
        try:
            # insert_sql = "insert into t_zx_tyc_summary_list_file_0321(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,bid_url_app,alias,bid_uuid) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,%(bid_url_app)s,%(alias)s,%(bid_uuid)s)"
            insert_sql = "insert into t_zx_tyc_qichezhizaoye_search_info_0321(company_name,bondname,bondnum,bondtype,tele_phone,email,website,tyc_id,legal_person,register_capital,enterprise_status,register_id,org_id,credit_id,revenue_id,industry_type,register_date,register_address,business_scope,base,city,district,create_time)VALUES (%(company_name)s,%(bondname)s,%(bondnum)s,%(bondtype)s,%(tele_phone)s,%(email)s,%(website)s,%(tyc_id)s,%(legal_person)s,%(register_capital)s,%(enterprise_status)s,%(register_id)s,%(org_id)s,%(credit_id)s,%(revenue_id)s,%(industry_type)s,%(register_date)s,%(register_address)s,%(business_scope)s,%(base)s,%(city)s,%(district)s,%(create_time)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_qichezhizaoye_search_info_2(self, item):
        try:
            # insert_sql = "insert into t_zx_tyc_summary_list_file_0321(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,bid_url_app,alias,bid_uuid) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,%(bid_url_app)s,%(alias)s,%(bid_uuid)s)"
            insert_sql = "insert into t_zx_tyc_qichezhizaoye_search_info_2_0321(company_name,bondname,bondnum,bondtype,tele_phone,email,website,tyc_id,legal_person,register_capital,enterprise_status,register_id,org_id,credit_id,revenue_id,industry_type,register_date,register_address,business_scope,base,city,district,create_time)VALUES (%(company_name)s,%(bondname)s,%(bondnum)s,%(bondtype)s,%(tele_phone)s,%(email)s,%(website)s,%(tyc_id)s,%(legal_person)s,%(register_capital)s,%(enterprise_status)s,%(register_id)s,%(org_id)s,%(credit_id)s,%(revenue_id)s,%(industry_type)s,%(register_date)s,%(register_address)s,%(business_scope)s,%(base)s,%(city)s,%(district)s,%(create_time)s)"
            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_bydqiche_search_info(self, item):
        try:
            # insert_sql = "insert into t_zx_tyc_summary_list_file_0321(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,bid_url_app,alias,bid_uuid) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,%(bid_url_app)s,%(alias)s,%(bid_uuid)s)"
            insert_sql = "insert into t_zx_tyc_bydqc_search_info_0327(company_name,bondname,bondnum,bondtype,tele_phone,email,website,tyc_id,legal_person,register_capital,enterprise_status,register_id,org_id,credit_id,revenue_id,industry_type,register_date,register_address,business_scope,base,city,district,create_time)VALUES (%(company_name)s,%(bondname)s,%(bondnum)s,%(bondtype)s,%(tele_phone)s,%(email)s,%(website)s,%(tyc_id)s,%(legal_person)s,%(register_capital)s,%(enterprise_status)s,%(register_id)s,%(org_id)s,%(credit_id)s,%(revenue_id)s,%(industry_type)s,%(register_date)s,%(register_address)s,%(business_scope)s,%(base)s,%(city)s,%(district)s,%(create_time)s)"
            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_lack_company_search_info(self, item):
        try:
            # insert_sql = "insert into t_zx_tyc_summary_list_file_0321(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,bid_url_app,alias,bid_uuid) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,%(bid_url_app)s,%(alias)s,%(bid_uuid)s)"
            insert_sql = "insert into t_zx_tyc_lack_company_search_info_0411(info_id,code,category,zwjc,company_name,bondname,bondnum,bondtype,tele_phone,email,website,tyc_id,legal_person,register_capital,enterprise_status,register_id,org_id,credit_id,revenue_id,industry_type,register_date,register_address,business_scope,base,city,district,create_time)VALUES (%(info_id)s,%(code)s,%(category)s,%(zwjc)s,%(company_name)s,%(bondname)s,%(bondnum)s,%(bondtype)s,%(tele_phone)s,%(email)s,%(website)s,%(tyc_id)s,%(legal_person)s,%(register_capital)s,%(enterprise_status)s,%(register_id)s,%(org_id)s,%(credit_id)s,%(revenue_id)s,%(industry_type)s,%(register_date)s,%(register_address)s,%(business_scope)s,%(base)s,%(city)s,%(district)s,%(create_time)s)"
            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_list_company_search_info(self, item):
        try:
            # insert_sql = "insert into t_zx_tyc_summary_list_file_0321(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,bid_url_app,alias,bid_uuid) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,%(bid_url_app)s,%(alias)s,%(bid_uuid)s)"
            insert_sql = "insert into t_zx_tyc_list_company_search_info_0411(listedType,company_name,bondname,bondnum,bondtype,tele_phone,email,website,tyc_id,legal_person,register_capital,enterprise_status,register_id,org_id,credit_id,revenue_id,industry_type,register_date,register_address,business_scope,base,city,district,create_time)VALUES (%(listedType)s,%(company_name)s,%(bondname)s,%(bondnum)s,%(bondtype)s,%(tele_phone)s,%(email)s,%(website)s,%(tyc_id)s,%(legal_person)s,%(register_capital)s,%(enterprise_status)s,%(register_id)s,%(org_id)s,%(credit_id)s,%(revenue_id)s,%(industry_type)s,%(register_date)s,%(register_address)s,%(business_scope)s,%(base)s,%(city)s,%(district)s,%(create_time)s)"
            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_jingzhengduishou_info(self, item):
        try:
            # insert_sql = "insert into t_zx_tyc_summary_list_file_0321(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,bid_url_app,alias,bid_uuid) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,%(bid_url_app)s,%(alias)s,%(bid_uuid)s)"
            insert_sql = "insert into t_zx_tyc_jingzhengduishou(info_id,	tyc_id,	company_name,	create_time,	gid,	competeOpponentName,	competeOpponentLogo,	competeOpponentAlias,	regCapital,	establishmentTime,	competeProductCount,	competeDisputeCaseCount,	bidCompeteCount)VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(gid)s,	%(competeOpponentName)s,	%(competeOpponentLogo)s,	%(competeOpponentAlias)s,	%(regCapital)s,	%(establishmentTime)s,	%(competeProductCount)s,	%(competeDisputeCaseCount)s,	%(bidCompeteCount)s)"
            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_list_company_code_info(self, item):
        try:
            # insert_sql = "insert into t_zx_tyc_summary_list_file_0321(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,bid_url_app,alias,bid_uuid) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,%(bid_url_app)s,%(alias)s,%(bid_uuid)s)"
            insert_sql = "insert into t_zx_list_company_code_info_0328 (info_id,	tyc_id,	company_name,	create_time,	stockType,	listingBoardName,	listingStatus,	listingType,	bondNum,	shorthand,	type) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(stockType)s,	%(listingBoardName)s,	%(listingStatus)s,	%(listingType)s,	%(bondNum)s,	%(shorthand)s,	%(type)s)"
            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_list_company_code_info_2(self, item):
        try:
            # insert_sql = "insert into t_zx_tyc_summary_list_file_0321(info_id,	tyc_id,	company_name,	create_time,	summary,	announcement_date,	amt,	companyUrl,	source,	supplier_graphId,	supplier_name,	relationship,	category,	client_name,	dataSource,	source_name,	source_seq,	ratio,bid_url_app,alias,bid_uuid) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(summary)s,	%(announcement_date)s,	%(amt)s,	%(companyUrl)s,	%(source)s,	%(supplier_graphId)s,	%(supplier_name)s,	%(relationship)s,	%(category)s,	%(client_name)s,	%(dataSource)s,	%(source_name)s,	%(source_seq)s,	%(ratio)s,%(bid_url_app)s,%(alias)s,%(bid_uuid)s)"
            insert_sql = "insert into t_zx_list_company_code_info_0411 (info_id,	tyc_id,	company_name,	create_time,	stockType,	listingBoardName,	listingStatus,	listingType,	bondNum,	shorthand,	type) VALUES (%(info_id)s,	%(tyc_id)s,	%(company_name)s,	%(create_time)s,	%(stockType)s,	%(listingBoardName)s,	%(listingStatus)s,	%(listingType)s,	%(bondNum)s,	%(shorthand)s,	%(type)s)"
            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_history_company_background_info(self, item):
        """历史工商信息"""
        try:
            insert_sql = """
            insert into t_zx_tyc_history_company_back_ground_info (info_id, company_name, locationlist, total, businessscopelist, typelist, orgnumberlist, deadlinelist, regcapitallist, historynamelist, uniquet_id, create_time) 
            VALUES (%(info_id)s, %(company_name)s, %(locationlist)s, %(total)s,	%(businessscopelist)s, %(typelist)s, %(orgnumberlist)s, %(deadlinelist)s, %(regcapitallist)s, %(historynamelist)s, %(uniquet_id)s,  %(create_time)s)
            """
            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_history_notice_delivery(self, item):
        """历史送达公告"""
        try:
            insert_sql = """
            INSERT INTO t_zx_tyc_history_notice_delivery(info_id,businessid,title,court,startdate,caseno,casereason,identitylist,content,company_name,tyc_id,uniquet_id,create_time)
            VALUES (%(info_id)s,%(businessid)s,%(title)s,%(court)s,%(startdate)s,%(caseno)s,%(casereason)s,%(identitylist)s,%(content)s,%(company_name)s,%(tyc_id)s,%(uniquet_id)s,%(create_time)s)
            """

            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_history_filing_information(self, item):
        """历史立案信息"""
        try:
            insert_sql = """
            INSERT INTO t_zx_tyc_history_filing_information(info_id, casedate, businessid, companyid, court, caseno, casetype, judge, assistant, department, closedate, starttime, identitylist, casestatus, company_name, tyc_id, uniquet_id, create_time)
            VALUES (%(info_id)s, %(casedate)s, %(businessid)s, %(companyid)s, %(court)s, %(caseno)s, %(casetype)s, %(judge)s, %(assistant)s, %(department)s, %(closedate)s, %(starttime)s, %(identitylist)s, %(casestatus)s, %(company_name)s, %(tyc_id)s,  %(uniquet_id)s, %(create_time)s)
            """

            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_lawsuitscr1_info(self, item):
        try:
            insert_sql = " INSERT INTO t_zx_company_lawsuitscr_info(info_id,	submittime,	plaintiffList,	casereason,	judgment,	defendantList,	docid,	lawsuitUrl,	amountPaperWork,	businessId,	title,	court,	uuid,	caseno,	url,	doctype,	judgetime,	eventTime,	casetype,	amountUnit,	amount,	explainMessage,	total,	company_name,lawsuitData,	hasCaseExplanation)VALUES(%(info_id)s,	%(submittime)s,	%(plaintiffList)s,	%(casereason)s,	%(judgment)s,	%(defendantList)s,	%(docid)s,	%(lawsuitUrl)s,	%(amountPaperWork)s,	%(businessId)s,	%(title)s,	%(court)s,	%(uuid)s,	%(caseno)s,	%(url)s,	%(doctype)s,	%(judgetime)s,	%(eventTime)s,	%(casetype)s,	%(amountUnit)s,	%(amount)s,	%(explainMessage)s,	%(total)s,	%(company_name)s,%(lawsuitData)s,	%(hasCaseExplanation)s)"

            self.cursor.execute(insert_sql, item)
            self.conn.commit()
        except Exception as e:
            logger.debug(e)

    def insert_into_administrative_licensing(self, item):
        """行政许可"""
        try:
            insert_sql = """
                INSERT INTO t_zx_tyc_administrative_licensing(info_id, similarcount, detailbusinessid, enddate, similarid, gid, originalid, businessid, onesimilarinfo, sourceid, detailshowtype, url_id, fromdate, onesimilarshowtype, licencedepartment, licencename, showtypename, licencecontent, similarbusinessid, licencenumber, unique_id, company_name, tyc_id, create_time)
                VALUES (%(info_id)s, %(similarcount)s, %(detailbusinessid)s, %(enddate)s, %(similarid)s, %(gid)s, %(originalid)s, %(businessid)s, %(onesimilarinfo)s, %(sourceid)s, %(detailshowtype)s, %(url_id)s, %(fromdate)s, %(onesimilarshowtype)s, %(licencedepartment)s, %(licencename)s, %(showtypename)s, %(licencecontent)s, %(similarbusinessid)s, %(licencenumber)s, %(unique_id)s, %(company_name)s, %(tyc_id)s, %(create_time)s)
                    """
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def insert_into_administrative_licensing_detail(self, item):
        """行政许可详情info_id"""
        try:
            insert_sql = """
                INSERT INTO t_zx_tyc_administrative_licensing_detail(info_id, licencecontent, validitytime, legalpersonid, enddate, licencenumber, localcode, department, auditype, dataupdatetime, decisiondate, legalpersonname, cid, company_name, tyc_id, create_time)
                VALUES (%(info_id)s, %(licencecontent)s, %(validitytime)s, %(legalpersonid)s, %(enddate)s, %(licencenumber)s, %(localcode)s, %(department)s, %(auditype)s, %(dataupdatetime)s, %(decisiondate)s, %(legalpersonname)s, %(cid)s, %(company_name)s, %(tyc_id)s, %(create_time)s)
                    """
            logger.debug("当前item数据为%s------------->" % item)

            self.cursor.execute(insert_sql, item)
            self.conn.commit()

        except IntegrityError as f:
            logger.warning("数据重复")

    def close(self):
        self.cursor.close()
        self.conn.close()


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


if __name__ == "__main__":
    my_sql = MysqlPipeline()
    print(my_sql)
