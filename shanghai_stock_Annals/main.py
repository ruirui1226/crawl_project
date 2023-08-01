# -*- coding: utf-8 -*-
# @ Time      : 2023/4/6 14:25
# @ Author    : wym
# @ FileName  : main.py
# @ SoftWare  : PyCharm
from scrapy import cmdline

cmdline.execute("scrapy crawl shanghai_stock_exchange_annual_report".split())
# juchao_web_caiwu_data
# juchao_annual_data

x = [
    [
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848763136",
            "ORG_FILE_TYPE": 0,
            "SECURITY_CODE": "600557",
            "SECURITY_NAME": "康缘药业",
            "SSEDATE": "2023-02-21",
            "TITLE": "江苏康缘药业股份有限公司2022年年度报告摘要",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/600557_20230221_7YP0.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848763136",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "600557",
            "SECURITY_NAME": "康缘药业",
            "SSEDATE": "2023-02-21",
            "TITLE": "江苏康缘药业股份有限公司2022年度独立董事述职报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/600557_20230221_4WWU.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848763136",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "600557",
            "SECURITY_NAME": "康缘药业",
            "SSEDATE": "2023-02-21",
            "TITLE": "江苏康缘药业股份有限公司2022年内部控制评价报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/600557_20230221_BXGW.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848763136",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "600557",
            "SECURITY_NAME": "康缘药业",
            "SSEDATE": "2023-02-21",
            "TITLE": "江苏康缘药业股份有限公司独立董事关于第七届董事会第二十次会议相关事项的独立意见",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/600557_20230221_M4J4.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848763136",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "600557",
            "SECURITY_NAME": "康缘药业",
            "SSEDATE": "2023-02-21",
            "TITLE": "江苏康缘药业股份有限公司2022年度企业社会责任报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/600557_20230221_PD40.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848763136",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "600557",
            "SECURITY_NAME": "康缘药业",
            "SSEDATE": "2023-02-21",
            "TITLE": "江苏康缘药业股份有限公司2022年年度报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/600557_20230221_SHDW.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848763136",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "600557",
            "SECURITY_NAME": "康缘药业",
            "SSEDATE": "2023-02-21",
            "TITLE": "江苏康缘药业股份有限公司内部控制审计报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/600557_20230221_TBOD.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848763136",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "600557",
            "SECURITY_NAME": "康缘药业",
            "SSEDATE": "2023-02-21",
            "TITLE": "江苏康缘药业股份有限公司董事会审计委员会2022年度履职情况报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/600557_20230221_VXA8.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848763136",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "600557",
            "SECURITY_NAME": "康缘药业",
            "SSEDATE": "2023-02-21",
            "TITLE": "江苏康缘药业股份有限公司2022年度审计报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/600557_20230221_XOPH.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848763136",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "600557",
            "SECURITY_NAME": "康缘药业",
            "SSEDATE": "2023-02-21",
            "TITLE": "江苏康缘药业股份有限公司关于康缘药业非经营性资金占用及其他关联资金往来情况汇总表的专项审计报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/600557_20230221_ZC4D.pdf",
        },
    ],
    [
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848773006",
            "ORG_FILE_TYPE": 0,
            "SECURITY_CODE": "603077",
            "SECURITY_NAME": "和邦生物",
            "SSEDATE": "2023-02-21",
            "TITLE": "和邦生物2022年年度报告摘要",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603077_20230221_JW1L.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848773006",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603077",
            "SECURITY_NAME": "和邦生物",
            "SSEDATE": "2023-02-21",
            "TITLE": "华信会计师事务所关于和邦生物2022年度控股股东及其他关联方占用资金情况的专项审核报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603077_20230221_39FM.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848773006",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603077",
            "SECURITY_NAME": "和邦生物",
            "SSEDATE": "2023-02-21",
            "TITLE": "和邦生物2022年度财务报表审计报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603077_20230221_4IOL.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848773006",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603077",
            "SECURITY_NAME": "和邦生物",
            "SSEDATE": "2023-02-21",
            "TITLE": "和邦生物2022年度独立董事述职报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603077_20230221_8GH8.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848773006",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603077",
            "SECURITY_NAME": "和邦生物",
            "SSEDATE": "2023-02-21",
            "TITLE": "和邦生物独立董事关于公司对外担保情况等相关事项的独立意见",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603077_20230221_90CF.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848773006",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603077",
            "SECURITY_NAME": "和邦生物",
            "SSEDATE": "2023-02-21",
            "TITLE": "和邦生物董事会审计委员会2022年度履职报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603077_20230221_BPS8.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848773006",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603077",
            "SECURITY_NAME": "和邦生物",
            "SSEDATE": "2023-02-21",
            "TITLE": "和邦生物2022年年度报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603077_20230221_LYEQ.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848773006",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603077",
            "SECURITY_NAME": "和邦生物",
            "SSEDATE": "2023-02-21",
            "TITLE": "和邦生物2022年度内部控制审计报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603077_20230221_TJUY.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8247890848773006",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603077",
            "SECURITY_NAME": "和邦生物",
            "SSEDATE": "2023-02-21",
            "TITLE": "和邦生物2022年度内部控制评价报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603077_20230221_ZWG9.pdf",
        },
    ],
    [
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8447890854967780",
            "ORG_FILE_TYPE": 0,
            "SECURITY_CODE": "603856",
            "SECURITY_NAME": "东宏股份",
            "SSEDATE": "2023-02-21",
            "TITLE": " 东宏股份2022年年度报告摘要",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603856_20230221_IM0V.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8447890854967780",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603856",
            "SECURITY_NAME": "东宏股份",
            "SSEDATE": "2023-02-21",
            "TITLE": "山东东宏管业股份有限公司2022年度审计报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603856_20230221_8ZWN.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8447890854967780",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603856",
            "SECURITY_NAME": "东宏股份",
            "SSEDATE": "2023-02-21",
            "TITLE": "关于山东东宏管业股份有限公司非经营性资金占用及其他关联资金往来的专项说明",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603856_20230221_J7RM.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8447890854967780",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603856",
            "SECURITY_NAME": "东宏股份",
            "SSEDATE": "2023-02-21",
            "TITLE": "东宏股份2022年度独立董事述职报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603856_20230221_JLVZ.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8447890854967780",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603856",
            "SECURITY_NAME": "东宏股份",
            "SSEDATE": "2023-02-21",
            "TITLE": "东宏股份独立董事关于公司2022年度对外担保情况的专项说明及独立意见",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603856_20230221_N61M.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8447890854967780",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603856",
            "SECURITY_NAME": "东宏股份",
            "SSEDATE": "2023-02-21",
            "TITLE": "东宏股份2022年度董事会审计委员会履职情况报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603856_20230221_UZHO.pdf",
        },
        {
            "BULLETIN_TYPE_DESC": "年报",
            "BULLETIN_YEAR": "2023",
            "IS_HOLDER_DISCLOSE": "0",
            "ORG_BULLETIN_ID": "8447890854967780",
            "ORG_FILE_TYPE": 1,
            "SECURITY_CODE": "603856",
            "SECURITY_NAME": "东宏股份",
            "SSEDATE": "2023-02-21",
            "TITLE": "东宏股份2022年年度报告",
            "URL": "/disclosure/listedinfo/announcement/c/new/2023-02-21/603856_20230221_XQ1G.pdf",
        },
    ],
]
