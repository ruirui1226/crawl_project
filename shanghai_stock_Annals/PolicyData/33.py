# -*- coding: utf-8 -*-
"""
@desc: 
@version: python3
@author: shenr
@time: 2023/6/1 
"""
def lll(items, table_name):
    if isinstance(items, list) and isinstance(table_name, str):
        str_fields = ", ".join([fields for fields, data in items[0].items()])
        str_data = "'" + "'), ('".join(["', '".join("%s" % data for fields, data in item.items()) for item in items]) + "'"
        sql = f"""insert into {table_name} ({str_fields}) values ({str_data}) """
        print(sql)

lll(
    [
        {"legalPersonId": "1759821805", "name": "威海拓展纤维有限公司", "total": 1},
        {"legalPersonId": "1828157438", "name": "云南红塔特铜新材料股份有限公司", "total": 2},
        {"legalPersonId": "2219605198", "name": "威海光威能源新材料有限公司", "total": 3}
        ],
    't_zx_company_invest_info'
)


