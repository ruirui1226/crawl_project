#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/5/11 15:49
@Author : zhangpf
@File : urls.py
@Desc :所有的url
@Software: PyCharm
"""
# url

# 历史开庭通告
HISTORY_NOTICE_OF_COURT_SESSION = "https://api6.tianyancha.com/cloud-history-information/historyJudicialRisk/hearingAnnouncement?riskType=0&needHidden=1&pageSize=10&id={}&pageNum={}"
# 历史法院公告
HISTORY_COURT_ANNOUNCEMENT = "https://api6.tianyancha.com/cloud-history-information/historyJudicialRisk/courtAnnouncementForApp?pageSize=20&id={}&pageNum={}&needHidden=1"
# 历史被执行人
HISTORY_PERSON_SUBJECT_TO_ENFORCEMENT = "https://api6.tianyancha.com/cloud-history-information/historyJudicialRisk/executedPerson?needHidden=1&pageSize=20&id={}&pageNum={}"
# 历史法定代表人
HISTORY_LEGAL_REPRESENTATIVE = (
    "https://api6.tianyancha.com/cloud-history-information/historyCompanyBackground/legalPerson?gid={}"
)
# 历史股东信息
HISTORY_SHAREHOLDER = "https://api6.tianyancha.com/cloud-history-information/historyCompanyBackground/shareHolders?shareHolderType=-100&needHidden=1&pageSize=20&id={}&percentLevel=-100&pageNum={}&hkVersion=1"
# 历史对外投资
HISTORY_INVESTMENTS_ABROAD = "https://api6.tianyancha.com/cloud-history-information/historyCompanyBackground/foreignInvestment?needHidden=1&pageNum={}&sortField=&id={}&pageSize=20&sortType=-1"
# 历史法律诉讼
HISTORY_ACTION_AT_LAW = "https://api6.tianyancha.com/cloud-history-information/historyJudicialRisk/lawsuitWithLabel?needHidden=1&pageSize=20&id={}&pageNum={}"
# 历史高管
HISTORY_SENIOR_EXECUTIVE = (
    "https://api6.tianyancha.com/cloud-history-information/historyCompanyBackground/officer?gid={}"
)
# 历史失信被执行人
HISTORY_SHIXIN_BEIZHIXINGREN = "https://api6.tianyancha.com/cloud-history-information/historyJudicialRisk/dishonest?keyWords={}&pageSize=20&gid={}&pageNum={}&needHidden=1"
# 历史送达公告
HISTORICAL_NOTICE_OF_SERVICE = (
    "https://api6.tianyancha.com/cloud-history-information/judicialRisk/company/sendAnnouncement"
)
# 历史送达公告详情
HISTORICAL_NOTICE_OF_SERVICE_DETAIL = (
    "https://api6.tianyancha.com/cloud-newdim/company/getSendAnnouncementsByBusinessId?businessId={}"
)
# 历史工商信息
HISTORY_INDUSTRY_COMMERCE_DATA = "https://api6.tianyancha.com/cloud-history-information/historyCompanyBackground/industrialCommercialInformation?needHidden=1&cid={}"
# 历史立案信息
HISTORY_FILING_INFORMATION = "https://api6.tianyancha.com/cloud-history-information/judicialRisk/courtRegisters"
# 天眼查作品著作权
Copyright_Of_Works_Url = "https://api6.tianyancha.com/cloud-intellectual-property/intellectualProperty/worksCopyrightListNew?gid={}&pageSize=20&category=-100&pageNum={}&registrationYear=-100"
# 天眼查地块公示
PUBLICITY_OF_LAND_PLOtS = (
    "https://api6.tianyancha.com/cloud-business-state/company/getLandPublicitys?gid={}&pageSize=20&pageNum={}"
)
# 天眼查资质证书
QUALIFICATION_CERTIFICATE = (
    "https://api6.tianyancha.com/cloud-business-state/certificate/list?pageSize=20&graphId={}&pageNum={}"
)
# 天眼查行政许可
ADMINISTRATIVE_LICENSING = (
    "https://api6.tianyancha.com/cloud-business-state/license/licenseList?gid={}&pageSize=20&pageNum={}"
)
# 天眼查行政许可详情
ADMINISTRATIVE_LICENSING_DETAIL = (
    "https://api6.tianyancha.com/cloud-business-state/license/credit/china/detailV2?graphId={}&businessId={}"
)
# 资质证书详情
QUALIFICATION_CERTIFICATE_DETAIls = "https://api6.tianyancha.com/services/v3/expanse/certificateDetail?id={}"
# 地块公式详情
PUBLICITY_OF_LAND_PLOtS_DETAILS = (
    "https://api6.tianyancha.com/cloud-business-state/company/getLandPublicityDetail?businessId={}"
)
# 历史法院公告详情
HISTORY_COURT_ANNOUNCEMENT_DETAILS = "https://api6.tianyancha.com/cloud-judicial-risk/judicialCase/relatedForApp/v2"
# 历史被执行人详情
HISTORY_PERSON_SUBJECT_TO_ENFORCEMENT_DETAILS = (
    "https://api6.tianyancha.com/cloud-judicial-risk/judicialCase/relatedForApp/v2"
)
# 主要人员
# KEY_PERSONNEL = "https://api4.tianyancha.com/services/v3/expanse/staff?pageSize=20&id={}&pageNum={}"
KEY_PERSONNEL = "https://api6.tianyancha.com/cloud-company-background/company/dim/staff?gid={}&pageSize=20&pageNum={}"
# 对外投资
INVESTMENTS_ABROAD = "https://api6.tianyancha.com/cloud-company-background/company/investListV2"
# 工商详情
BUSINESS_INFORMATION = "https://api6.tianyancha.com/services/v3/t/details/appComIcV4/{}?pageSize=1000"
# 企业市值
ENTERPRISE_MARKET_VALUE = "https://api6.tianyancha.com/cloud-listed-company/listed/stock/market?gid={}&bondNum={}"
# 历史行政处罚
HISTORY_ADMINISTRATIVE_PENALTY = "https://api6.tianyancha.com/cloud-history-information/historyOperatingRisk/historyPunishIndexList?needHidden=1&pageNum={}&gid={}&pageSize=20"
# 历史知识产权出质
HISTORY_INTELLECTUAL_PROPERTY_PLEDGED = "https://api6.tianyancha.com/cloud-operating-risk/operating/pledgeReg/getHistoryPledgeReg.json?gid={}&pageSize=20&pageNum={}"
# 历史终本案件
HISTORICAL_FINAL_CASE = "https://api6.tianyancha.com/cloud-history-information/historyJudicialRisk/terminationCaseList?gid={}&needHidden=1&pageSize=20&pageNum={}"
# 最终受益人
FINAL_BENEFICIARY = (
    "https://api6.tianyancha.com/cloud-equity-provider/v4/hold/humanholdingV2?pageSize=20&id={}&pageNum={}"
)
# 实际控制权
COMPANY_HOLDING = (
    "https://api6.tianyancha.com/cloud-equity-provider/v4/hold/companyholding?pageSize=20&id={}&pageNum={}"
)
# 股东信息
HOLDER_INFO = "https://api6.tianyancha.com/cloud-company-background/companyV2/dim/holderForApp?gid={}&shareHolderType=-100&pageSize=20&percentLevel=-100&pageNum={}&hkVersion=1"
# 变更记录
# CHANGE_INFO = "https://api4.tianyancha.com/services/v3/expanse/changeinfoEm3?pageSize=20&id={}&pageNum={}"
CHANGE_INFO = "https://api6.tianyancha.com/cloud-company-background/company/changeinfoEm?gid={}&pageSize=20&pageNum={}"
# 实际控制人
ACTUAL_CONTROL_INFO = (
    "https://capi.tianyancha.com/cloud-equity-provider/v4/actualControl/company/list?id={}&height=750&width=610"
)
# 商标详情
TRADEMARK_DETAILS = (
    "https://api6.tianyancha.com/cloud-intellectual-property/intellectualProperty/trademarkDetailV1?regNo={}&tmClass={}"
)
# 专利信息
PATENT_LIST = "https://api6.tianyancha.com/cloud-intellectual-property/patent/patentListV6?applyYear=-100&sortIndex=-100&pubYear=-100&lprs=-100&pageSize=20&mainIpcType=-100&id={}&type=-100&pageNum={}"
# 专利详情
PATENT_DETAIL = "https://api6.tianyancha.com/cloud-intellectual-property/patent/patentDetail?id={}"
# 软件著作权
COPYREG_LIST = "https://api6.tianyancha.com/cloud-intellectual-property/intellectualProperty/softwareCopyrightListV2?regYear=-100&pageSize=20&id={}&pageNum={}"
# 投资事件
TZANLI_LIST = (
    "https://api6.tianyancha.com/cloud-company-development/company/development/tzanlilist?gid={}&pageSize=20&pageNum={}"
)
# 企业业务
ENTERPRISE_BUSINESS_LIST = "https://api6.tianyancha.com/cloud-company-development/company/development/enterprisebusinesslist?gid={}&pageSize=20&pageNum={}"
# 竞品信息
FINDJINGPIN_LIST = "https://api6.tianyancha.com/cloud-company-development/company/development/jingpinlist?gid={}&pageSize=20&pageNum={}"
# 投资机构
INVESTOR_ORG_LIST = (
    "https://api6.tianyancha.com/cloud-company-development/company/development/investorgs?gid={}&pageSize=20&pageNum={}"
)
# 融资历程
FINDHISTORY_RONGZI_LIST = "https://api6.tianyancha.com/cloud-company-development/company/development/financinghistorylist?gid={}&pageSize=1000&pageNum={}"
# 核心团队
FIND_TEAMMEMBER_LIST = "https://api6.tianyancha.com/cloud-company-development/company/development/teammemberlist?gid={}&pageSize=20&pageNum={}"
# 私募基金
HEDGEFUND_INFOS = "https://api6.tianyancha.com/cloud-company-development/company/development/hedgeFundInfos?id={}"
# 网站备案
ICPRECORD_LIST = "https://api6.tianyancha.com/cloud-intellectual-property/intellectualProperty/icpRecordList?pageSize=20&id={}&pageNum={}"
# 司法拍卖
JUDICIAL_SALE = "https://api6.tianyancha.com/cloud-operating-risk/operating/sale/judicialSaleV2/list?auctionStage=-100&gid={}&pageSize=20&pageNum={}"
# 环保处罚
ENVIRONMENTAL_PENALTIE = "https://api6.tianyancha.com/cloud-operating-risk/operating/environmental/getEnvironmentalPenaltiesNew?gid={}&punishYear=-100&pageSize=20&pageNum={}"
# 终本案件
ENDCASE_LIST = "https://api6.tianyancha.com/cloud-judicial-risk/risk/getFinalCase?gid={}&pageSize=20&pageNum={}"
# 失信被执行人
DISHONESTY_LIST = (
    "https://api6.tianyancha.com/cloud-judicial-risk/risk/dishonestApp?keyWords={}&pageSize=20&gid={}&pageNum={}"
)
# 送达公告
DELIVERYNOTICE_LIST = "https://api6.tianyancha.com/cloud-judicial-risk/judicialRisk/company/sendAnnouncement"
# 被执行人
DEBETOR_LIST = "https://api6.tianyancha.com/cloud-judicial-risk/risk/zhixing?gid={}&pageSize=20&pageNum={}"
# 涉诉关系列表
LITIGATIONRELATIONSHIP_LIST = "https://api6.tianyancha.com/cloud-judicial-risk/litigationRelated/list/v2?relationType=-100&pageSize=20&gid={}&pageNum={}&subjectType=-100"
# 涉诉关系详情
LITIGATIONRELATIONSHIP_DETAILS = "https://api6.tianyancha.com/cloud-judicial-risk/litigationRelated/detail/v2?needFilter=1&pageNum={}&oppositeGid={}&subjectType={}&gid={}&isSameSerialCaseAgg={}&pageSize=20"
# 法院公告
COURTAPP_LIST = (
    "https://api6.tianyancha.com/cloud-judicial-risk/risk/courtApp?keyWords={}&pageSize=20&gid={}&pageNum={}"
)
# 破产重整
BANKRUPTCY_LIST = "https://api6.tianyancha.com/cloud-judicial-risk/bankruptcy/list?gid={}&pageSize=20&pageNum={}"
# 涉金融黑名单列表
FINANCIALBLACKLIST_LIST = (
    "https://api6.tianyancha.com/cloud-judicial-risk/risk/getCreditFinacialBlacklist?gid={}&pageSize=20&pageNum={}"
)
# 涉金融黑名单详情
FINANCIALBLACKLIST_DETAILS = (
    "https://api6.tianyancha.com/cloud-judicial-risk/risk/getCreditFinacialBlacklistDetail?gid={}&businessId={}"
)
# 询价评估结果
INQUIRY_EVALUATION_LIST = "https://api6.tianyancha.com/cloud-operating-risk/operating/inquiryEvaluation/getInquiryEvaluationResultList?pageNum={}&gid={}&pageSize=20"
# 开庭公告
ANNOUNCEMENT_LIST = "https://api6.tianyancha.com/cloud-judicial-risk/risk/courtNotice?gid={}&pageSize=20&pageNum={}"
# 司法解析列表
JUDICIALCASE_LIST = "https://api6.tianyancha.com/cloud-judicial-risk/judicialCase/list/v2"
# 限制消费令
LIMIT_CONSUMPTION_LIST = (
    "https://api6.tianyancha.com/cloud-judicial-risk/risk/getRestrictOrder?gid={}&year=-100&pageSize=20&pageNum={}"
)
# 司法解析详情
JUDICIALCASE_DETAILS = "https://api6.tianyancha.com/cloud-judicial-risk/judicialCase/detailV2"
# 司法协助列表
MUTUALLEGALASSISTANCE_LIST = (
    "https://api6.tianyancha.com/cloud-judicial-risk/risk/getJudicialList?gid={}&pageSize=20&pageNum={}"
)
# 司法协助详情
MUTUALLEGALASSISTANCE_DETAILS = "https://api6.tianyancha.com/cloud-judicial-risk/risk/getJudicialDetail?assId={}"
# 限制出境
OUTBOUNDRESTRICTIONS_LIST = (
    "https://api6.tianyancha.com/cloud-judicial-risk/risk/company/restrictedOutbound/list?gid={}&pageSize=20&pageNum={}"
)
# 选定评估机构
SELECTEDEVALUATIONAGENCY_LIST = "https://api6.tianyancha.com/cloud-operating-risk/operating/inquiryEvaluation/getInquiryEvaluationList.json?pageNum={}&gid={}&pageSize=20"
# 法律诉讼
LAWSUITSCR_LIST = (
    "https://api6.tianyancha.com/cloud-judicial-risk/risk/lawsuit?keyWords={}&gid={}&pageSize=20&pageNum={}"
)
# 立案信息
COURTREGISTER_LIST = (
    "https://api6.tianyancha.com/cloud-judicial-risk/risk/getCourtRegister?pageNum={}&gid={}&pageSize=20"
)
# 税务评级
TAX_RATING = "https://api6.tianyancha.com/cloud-business-state/v3/ar/taxcred?gid={}&pageSize=20&pageNum={}"
# 股权出质
EQUITY_PLEDGE = "https://api6.tianyancha.com/cloud-operating-risk/operating/equity/getCompanyEquityInfoListV3.json?pageSize=20&state=-100&gid={}&pageNum={}&identity=-100"
# 历史股权出质
HISTORY_EQUITY_PLEDGE = "https://api6.tianyancha.com/cloud-history-information/historyOperatingRisk/equityPledgeV2?pageSize=20&state=-100&id={}&pageNum={}&identity=-100&needHidden=1"
# 天眼查一般纳税人
GENERAL_TAXPAYER = (
    "https://api6.tianyancha.com/cloud-business-state/common/taxpayer/list?pageSize=20&graphId={}&pageNum={}"
)
# 基本信息
BASIC_INFO = "https://api6.tianyancha.com/services/v3/t/common/baseinfoV5ForApp/{}"
# 天眼查上榜榜单
ON_THE_LIST = (
    "https://api6.tianyancha.com/cloud-business-state/rankingList/list?gid={}&year=-100&pageSize=20&pageNum={}"
)
# 担保风险
GUARANTY_INSURANCE = "https://api6.tianyancha.com/cloud-operating-risk/guaranty/insurance"
# 股权质押
PLEDGE_OF_STOCK_RIGHT = "https://api6.tianyancha.com/cloud-operating-risk/operating/stockPledge/detailList.json?gid={}&pageSize=20&pageNum={}&status=-100"
# 经营异常
ABNORMALOPERATION_LIST = "https://api6.tianyancha.com/cloud-operating-risk/operating/abnormal/getAbnormalList.json?gid={}&pageSize=20&pageNum={}"
# 行政处罚
ADMINISTRATIVE_PENALTY = "https://api6.tianyancha.com/cloud-operating-risk/operating/punishment/punishIndexList?gid={}&pageSize=20&pageNum={}"
# 欠税公告
ANNOUNCEMENT_OF_TAX = (
    "https://api6.tianyancha.com/cloud-operating-risk/operating/tax/companyowntax.json?gid={}&pageSize=20&pageNum={}"
)


# 招投标详情
BID_DETAIL = "https://m.tianyancha.com/app/h5/bid/{}"
