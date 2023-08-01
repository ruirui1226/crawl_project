# -*- coding: utf-8 -*-
"""
@desc:
@version: python3
@author: shenr
@time: 2023/7/13
"""

# from paddlenlp import Taskflow
#
# from untils.pysql import MysqlPipelinePublic
#
# mq = MysqlPipelinePublic()
#
# # 需处理数据
# sel_data = mq.select_sql("t_zx_bid_info", ["bid_id", "info_type", "bid_html_con"], {"1": "1"})
# print(sel_data[0])
# # keyword
# keyword_data = mq.select_sql("type_keyword", ["type_", "keyword_"], {"1": "1"})
# print(keyword_data)
# type_s = set()
#
# keyword_dic_all = {}
# for rows in keyword_data:
#     type_s.add(rows["type_"])
# print(type_s)
#
# for ty in type_s:
#     keyword_list = []
#     for key in keyword_data:
#         if key.get("type_") == ty:
#             keyword_list.append(key.get("keyword_"))
#     keyword_dic_all[ty] = keyword_list
# print(keyword_dic_all)
# data_all = []
# for each in sel_data[:3]:
#     print("cccccc", each.get("info_type"))
#     schema = keyword_dic_all.get(each.get("info_type"))
#     # print("kkkk", schema)
#     ie = Taskflow("information_extraction", schema=schema)
#     xxx = ie(each.get("bid_html_con"))
#     print(xxx)
#     data = xxx[0]
#     print(type(data))
#     data_end = {"bid_id": each.get("bid_id")}
#     for kkk, vvv in data.items():
#         data_end[kkk] = [jj.get("text") for jj in vvv]
#     data_all.append(data_end)
# print("llllll", data_all)


# # print(ie("""
# #
# #
# # 扶余市人民医院64排CT球管采购项目中标公示
# #
# #                   【信息时间：2023-06-28 来源：】【我要打印】【关闭】
# #
# #
# #                中标结果公告
# #  
# # 一、项目编号：FYGGZYCG-2023084
# # 二、项目名称：扶余市人民医院64排CT球管采购项目
# # 三、中标信息：
# # 中标公司名称：上海佐医得贸易商行
# # 中标公司地址：上海市金山区吕巷镇璜溪西街88号（吕巷经济园区）
# # 中标金额：118万元
# # 四、主要标的信息
# # 名称：64排CT球管
# # 型号：ATHLON X线球管
# # 数量：一个
# # 总价：118万元
# # 采购需求：详见招标文件；
# # 合同履行期限：自签订合同之日起5日内到货并验收合格。
# # 五、代理服务收费标准及金额：按照吉省价【2016】98号；发改价格【2015】299号等相关文件的取费标准计费。
# # 六、公告期限
# # 自本公告发布之日起1个工作日。
# # 七、其他补充事宜
# # 1.中标公示发布媒介：吉林省公共资源交易公共服务平台、中国政府采购网、吉林省政府采购网、松原市公共资源交易中心网。 
# # 2.政府采购信用贷款，请联系松原市信用综合金融服务平台。       
# # 联系人：李明峻  
# # 联系电话：0438-8888336    18686500569
# # 八、凡对本次公告内容提出询问，请按以下方式联系
# # 1.采购人信息
# # 名 称：扶余市人民医院
# # 地址：扶余市
# # 联系方式：吴坤明  0438-5865577
# # 2.采购代理机构信息
# # 名 称：长春中建招标投标代理有限责任公司
# # 地　址：长春市净月开发区伟峰.生态新城11#办公楼1202号
# # 联系方式：0438-5029666
# # 3.项目联系方式
# # 项目联系人：张丽
# # 电　话：0438-5029666
# # 九、附件
# # 无交易文件下载:http://syggzy.jlsy.gov.cn/EpointWebBuilder/WebbuilderMIS/RedirectPage/RedirectPage.jspx?locationurl=http://syggzy.jlsy.gov.cn/&infoid=0bef5fd7-856c-43c2-9008-bee00eb28cab
# #
# #
# # """
# #          ))
# for each in sel_data:
#     xx = ie(each.get("bid_html_con"))
#     print(xx)

# 黄页88
# import requests
#
#
# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     "Referer": "https://b2b.huangye88.com/qiye/yiqiyibiao3/",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
#     "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\""
# }
# cookies = {
#     "Hm_lvt_c8184fd80a083199b0e82cc431ab6740": "1690349362",
#     "PHPSESSID": "16903493899506-f71a60cda6ef52a543599b6c9f837d33125a09bf",
#     "Hm_lpvt_c8184fd80a083199b0e82cc431ab6740": "1690349433"
# }
# url = "https://b2b.huangye88.com/guangdong/yiqiyibiao3/"
# response = requests.get(url, headers=headers)#, cookies=cookies)
#
# # print(response.text)
# print("黄页88", response)
#
#
# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     "Referer": "https://b2b.huangye88.com/",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-site",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
#     "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\""
# }
# cookies = {
#     "Hm_lvt_c8184fd80a083199b0e82cc431ab6740": "1690349362",
#     "PHPSESSID": "16903493899506-f71a60cda6ef52a543599b6c9f837d33125a09bf",
#     "Hm_lpvt_c8184fd80a083199b0e82cc431ab6740": "1690350921"
# }
# url = "https://xq13790145202.b2b.huangye88.com/"
# response = requests.get(url, headers=headers, cookies=cookies)
#
# # print(response.text)
# print("黄页88详情页", response)
#
#
# # 行业信息网
#
# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     "If-Modified-Since": "Wed, 26 Jul 2023 05:20:01 GMT",
#     "If-None-Match": "\"9d5791d380bfd91:0\"",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
# }
# cookies = {
#     "Hm_lvt_8803f7fa56465a59d0c1a12ec666f533": "1690349685",
#     "Hm_lpvt_8803f7fa56465a59d0c1a12ec666f533": "1690349685",
#     "ASP.NET_SessionId": "tq025mfezrp312svxbmvvxzg",
#     "Hm_lvt_24969605ad342d5ccd2702ab1acc3525": "1690349706",
#     "Hm_lpvt_24969605ad342d5ccd2702ab1acc3525": "1690349706"
# }
# url = "http://www.cnlinfo.net/company/index.htm"
# response = requests.get(url, headers=headers, cookies=cookies, verify=False)
#
# # print(response.text)
# print("行业信息网列表页", response)
#
#
#
# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     "Referer": "http://www.cnlinfo.net/company/index.htm",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
# }
# cookies = {
#     "Hm_lvt_8803f7fa56465a59d0c1a12ec666f533": "1690349685",
#     "ASP.NET_SessionId": "tq025mfezrp312svxbmvvxzg",
#     "Hm_lvt_24969605ad342d5ccd2702ab1acc3525": "1690349706",
#     "Hm_lpvt_24969605ad342d5ccd2702ab1acc3525": "1690349706",
#     "Hm_lpvt_8803f7fa56465a59d0c1a12ec666f533": "1690349722"
# }
# url = "http://www.cnlinfo.net/s_gongsi/b38aacf.htm"
# response = requests.get(url, headers=headers, cookies=cookies, verify=False)
#
# # print(response.text)
# print("行业信息网详情页", response)


# import requests
#
#
# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     "Referer": "http://www.cnlinfo.net/",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
# }
# cookies = {
#     "Hm_lvt_8803f7fa56465a59d0c1a12ec666f533": "1690349685",
#     "Hm_lvt_24969605ad342d5ccd2702ab1acc3525": "1690349706",
#     "Hm_lpvt_24969605ad342d5ccd2702ab1acc3525": "1690349706",
#     "SECKEY_ABVK": "lOmRsU3WetZblY2o0BLMuek0a1OKduCM+doSwtBJZCI%3D",
#     "BMAP_SECKEY": "KeOnjGJkQA6FWx0XLyR1IL0HxAwCZpjicPR97WZOlxDjtgeONXOIANouMJguOFJVTBf0DD5jkJBQs8guFo3MvJDl9GfZphYbniQYV3_sS41mZvODjlZv7wf6eIMgDpYatWZJ5KbX042tB4XBdJE0-lgfJ5XrcO81A0ZYKxDuE-PlVd_PTYXJkoLYxmExYUnb",
#     "Hm_lpvt_8803f7fa56465a59d0c1a12ec666f533": "1690349722"
# }
# url = "http://cangzhou52259157.cn.cnlinfo.net/"
# response = requests.get(url, headers=headers)#, cookies=cookies, verify=False)
#
# print(response.text)
# print(response)


# import requests
#
#
# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Origin": "https://china.chemnet.com",
#     "Referer": "https://china.chemnet.com/company/supplier.cgi",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
#     "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\""
# }
# url = "https://china.chemnet.com/company/supplier.cgi"
# data = {
#     "f": "",
#     "t": "company",
#     "terms": "",
#     "search": "company",
#     "property": "",
#     "regional": "",
#     "submit.x": "0",
#     "submit.y": "0"
# }
# response = requests.post(url, headers=headers, data=data)
#
# print(response.text)
# print(response)


# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
# }
# url = "http://willingchem.cn.chemnet.com/show/"
# response = requests.get(url, headers=headers, verify=False)
#
# print(response.text)
# print(response)


import requests


headers = {
    "authority": "dachiauto.en.made-in-china.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "referer": "https://www.made-in-china.com/",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}
cookies = {
    "se": "TI0LjEyOC42OS4xMjYyMDIzMDcyNTE1MTkxMjM2MTcwMTc5NTAxM",
    "lang": "en",
    "pid": "TI0LjEyOC42OS4xMjYyMDIzMDcyNTE1MTkxMjM2MTQ0MjI1OTg0M",
    "sf_img": "AM",
    "inquiry_id": "zkwMDAzNzkzNTU3OTQ4OTQ6OjEyNC4xMjguNjkuMTI2M",
    "webp": "t",
    "dpr": "1",
    "__pd": "1h65ul3ihe32",
    "cid": "jAyMzA3MjUxNTE5MTMwMjYwMDA6MTI3MjYxODkzMjE2OTMxMDUyMTUM",
    "sid": "zkwMDE3MDY2MDIzNjIyNjE6OjEyNC4xMjguNjkuMTI2M",
    "sajssdk_2015_cross_new_user": "1",
    "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%221898bea8f33159-0919bbb1a64f4b-26031b51-2073600-1898bea8f341b4f%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%7D%2C%22%24device_id%22%3A%221898bea8f33159-0919bbb1a64f4b-26031b51-2073600-1898bea8f341b4f%22%7D",
    "JSESSIONID": "5EB198FC09DFABA8BCC81D9387E4D815",
    "_skwd": "29tX35Hb2xmIENhcn4hLGNvbV9+RWxlY3RyaWMgR29sZiBDYXJ+ISxjb21fflJWY",
    "_uat": "AM.lAxTUsxOTI2MTk0NzA0R.1.20230725151918"
}
url = "https://dachiauto.en.made-in-china.com/"
response = requests.get(url, headers=headers, cookies=cookies)

print(response.text)
print(response)