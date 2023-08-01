# -*- coding: utf-8 -*-
# @ Time      : 2023/5/29 13:19
# @ Author    : wym
# @ FileName  : env_demo.py
# @ SoftWare  : PyCharm
#!/usr/bin/conf python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/19 16:11
# @Author  : wym
# @File    : conf.py


# 数据库类型 MYSQL/SQLITE3
# DATABASE_TYPE = "MYSQL"
# # 数据库地址
# DATABASE_HOST = "10.67.78.14"
# # 数据库端口
# DATABASE_PORT = 3306
# # 数据库用户名
# DATABASE_USER = "root"
# # 数据库密码
# DATABASE_PASSWORD = "zxicet"
# # 数据库名
# DATABASE_NAME = "industrial_chain_project"

# X-AUTH-TOKEN
GET_AUTHORZATION_API = "http://10.69.6.18:9898/get_authorzation"

GET_AUTHORZATION_LOCAL_API = "http://127.0.0.1:9964/get_authorzation"

# (host="10.67.78.14", port=3306, user="root", password="zxicet", db="enterprise_analysis")
# JSON保存目录文件夹
FILE_PATH = ""
#
# 数据库类型 MYSQL/SQLITE3
DATABASE_TYPE = "MYSQL"
# 数据库地址
# DATABASE_HOST = "10.67.78.125"
DATABASE_HOST = "10.69.6.18"
# 数据库端口
DATABASE_PORT = 3306
# 数据库用户名
DATABASE_USER = "root"
# 数据库密码
DATABASE_PASSWORD = "121314"
# 数据库名
DATABASE_NAME = "industrial_chain_enterprise_project"

# 是否启用Redis缓存
# 注：不使用redis则无法使用celery
REDIS_ENABLE = False
REDIS_DB = 1
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWORD = "121314"
REDIS_ENCODING = "utf-8"
# celery 定时任务redis 库号
CELERY_DB = 2


str_host = ""
