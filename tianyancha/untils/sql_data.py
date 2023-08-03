# -*- coding: utf-8 -*-
"""
@desc: sql数据集合
@version: python3
@author: shenr
@time: 2023/7/13 
"""
from untils.pysql import MysqlPipelinePublic


MYSQLTABLE_STR = "company_name_0727_new"
MYSQLFIELD_LIST = ["id", "co_name as co_name", "co_id as co_id"]
MUSQLWHERE_DIC = {"co_id": "2960171546"}

# 天眼查数据集合
mq = MysqlPipelinePublic()
TYC_DATA = mq.select_sql(MYSQLTABLE_STR, MYSQLFIELD_LIST, MUSQLWHERE_DIC)
