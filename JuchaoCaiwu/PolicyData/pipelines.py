# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface


import psycopg2
import pymysql
from loguru import logger
# import settings


# mysql存储
# class mysqlPipeline(object):
#     mysql = None
#     cursor = None
#
#     def open_spider(self,spider):
#
#         self.mysql = pymysql.Connect(host='localhost', user='postgres', password='zhongxing', port=5432, charset='utf8', database='test')
#         self.cursor = self.mysql.cursor()
#
#     def process_item(self, item, spider):
#         # table = 'create table if not exists t_zx_policy_shandong(' \
#         #         'id int not null primary key auto_increment' \
#         #         ',baseId varchar(250)' \
#         #         ',createUser varchar(250)' \
#         #         ',createTime Date' \
#         #         ',updateUserName varchar(250)' \
#         #         ',updateTime Date' \
#         #         ',title varchar(250)' \
#         #         ',publishTime Date'\
#         #         ',content LONGTEXT' \
#         #         ',showTage varchar(250)' \
#         #         ',sources varchar(250)' \
#         #         ',deadTime Date' \
#         #         ',viewCount varchar(250)' \
#         #         ',attachment varchar(250)' \
#         #         ',comment varchar(250)' \
#         #         ');'
#
#         insert = 'insert into pilicy_elucidation(id,create_by,create_time,update_by,update_time,title,release_date,status,content,label,source,end_date,view_number,file_link_id,remark) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(item['id'],item['create_by'],item['create_time'],item['update_by'],item['update_time'],item['title'],item['release_date'],item['status'],item['content'],item['label'],item['source'],item['end_date'],item['view_number'],item['file_link_id'],item['remark'])
#         try:
#             logger.info(insert)
#             # self.cursor.execute(table)
#             self.cursor.execute(insert)
#             self.mysql.commit()
#
#         except Exception as e:
#             logger.info('===============插入数据失败===============', e)
#             self.mysql.rollback()
#
#         return item  # 传递给下一个即将被执行的管道类
#
#     # 关闭MySQL连接
#     def close_spider(self,spider):
#         self.cursor.close()
#         self.mysql.close()


# Postgres存储
class PostgresPipeline:
    def __init__(self):
        hostname = "10.67.78.125"
        username = "root"
        password = "hsd#H&hdj6sd"
        port = 3306
        database = "list_company_annual_report"

        self.connection = pymysql.connect(
            database=database,
            user=username,
            port=port,
            password=password,
            host=hostname,
        )

        self.cur = self.connection.cursor()

        # self.cur.execute("""
        # CREATE TABLE IF NOT EXISTS policy_elucidation(
        #     id serial PRIMARY KEY
        # )
        # """)

    def process_item(self, item, spider):
        if item["spider_name"] == "t_zx_sme_policy_interpretation":
            try:
                self.cur.execute(
                    "INSERT INTO t_zx_sme_policy_interpretation (id,title,publishNo,publishTime,execTime,deadTime,applyUrl,source,publishUnit,publishUnit2,publishUnit3,publishUnit4,content,policyState,isTop,rightTop,pArticleState,pAnalyseState,policyType,pbmsm,videoUrl,subject,applicationType,url,specialType,urlmd5,isCrawled,publishUnitFilter,createTime,creatorId,createUser,updateTime,updateUserId,updateUserName,delFlag,essence,policyType2,policyType1,policyType3,policyType4,orderBy,publishTimeTo,createTimeTo,percents,userId,topicType,isTopic,isCollect,fav_id,queryYear,sem_attachment,page) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        item["id"],
                        item["title"],
                        item["publishNo"],
                        item["publishTime"],
                        item["execTime"],
                        item["deadTime"],
                        item["applyUrl"],
                        item["source"],
                        item["publishUnit"],
                        item["publishUnit2"],
                        item["publishUnit3"],
                        item["publishUnit4"],
                        item["content"],
                        item["policyState"],
                        item["isTop"],
                        item["rightTop"],
                        item["pArticleState"],
                        item["pAnalyseState"],
                        item["policyType"],
                        item["pbmsm"],
                        item["videoUrl"],
                        item["subject"],
                        item["applicationType"],
                        item["url"],
                        item["specialType"],
                        item["urlmd5"],
                        item["isCrawled"],
                        item["publishUnitFilter"],
                        item["createTime"],
                        item["creatorId"],
                        item["createUser"],
                        item["updateTime"],
                        item["updateUserId"],
                        item["updateUserName"],
                        item["delFlag"],
                        item["essence"],
                        item["policyType2"],
                        item["policyType1"],
                        item["policyType3"],
                        item["policyType4"],
                        item["orderBy"],
                        item["publishTimeTo"],
                        item["createTimeTo"],
                        item["percents"],
                        item["userId"],
                        item["topicType"],
                        item["isTopic"],
                        item["isCollect"],
                        item["fav_id"],
                        item["queryYear"],
                        item["sem_attachment"],
                        item["page"],
                    ),
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败==============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "t_zx_sme_policy_declaration":
            try:
                self.cur.execute(
                    "INSERT INTO t_zx_sme_policy_declaration (id,title,publishNo,publishTime,execTime,deadTime,applyUrl,source,publishUnit,publishUnit2,publishUnit3,publishUnit4,content,policyState,isTop,rightTop,pArticleState,pAnalyseState,policyType,pbmsm,videoUrl,subject,applicationType,url,specialType,urlmd5,isCrawled,publishUnitFilter,createTime,creatorId,createUser,updateTime,updateUserId,updateUserName,delFlag,essence,policyType2,policyType1,policyType3,policyType4,orderBy,publishTimeTo,createTimeTo,percents,userId,topicType,isTopic,isCollect,fav_id,queryYear,sem_attachment,page) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        item["id"],
                        item["title"],
                        item["publishNo"],
                        item["publishTime"],
                        item["execTime"],
                        item["deadTime"],
                        item["applyUrl"],
                        item["source"],
                        item["publishUnit"],
                        item["publishUnit2"],
                        item["publishUnit3"],
                        item["publishUnit4"],
                        item["content"],
                        item["policyState"],
                        item["isTop"],
                        item["rightTop"],
                        item["pArticleState"],
                        item["pAnalyseState"],
                        item["policyType"],
                        item["pbmsm"],
                        item["videoUrl"],
                        item["subject"],
                        item["applicationType"],
                        item["url"],
                        item["specialType"],
                        item["urlmd5"],
                        item["isCrawled"],
                        item["publishUnitFilter"],
                        item["createTime"],
                        item["creatorId"],
                        item["createUser"],
                        item["updateTime"],
                        item["updateUserId"],
                        item["updateUserName"],
                        item["delFlag"],
                        item["essence"],
                        item["policyType2"],
                        item["policyType1"],
                        item["policyType3"],
                        item["policyType4"],
                        item["orderBy"],
                        item["publishTimeTo"],
                        item["createTimeTo"],
                        item["percents"],
                        item["userId"],
                        item["topicType"],
                        item["isTopic"],
                        item["isCollect"],
                        item["fav_id"],
                        item["queryYear"],
                        item["sem_attachment"],
                        item["page"],
                    ),
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败==============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "qingdao_gov_policy":
            try:
                self.cur.execute(
                    f"INSERT INTO public.t_zx_qingdao_gov_policy (url, wibsite, title, datetime, source_type, content, div_content) VALUES ('{item['url']}', '{item['wibsite']}', '{item['title']}', '{item['datetime']}', '{item['source_type']}', '{item['content']}', '{item['div_content']}')"
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败===============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "jinan_gov_business":
            try:
                self.cur.execute(
                    f"INSERT INTO public.t_zx_jinan_gov_business (title, datetime, source_type, url, pdf_url, content, div_content) VALUES ('{item['title']}', '{item['datetime']}', '{item['source_type']}', '{item['url']}', '{item['pdf_url']}', '{item['content']}', '{item['div_content']}')"
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败===============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "quanhuiqi_zcfw_policy":
            try:
                self.cur.execute(
                    f"""INSERT INTO public.t_zx_quanhuiqi_zcfw_policy (url_id, title, city, policy_type, issuing_department, publishtime, dispatchtime, dispatchnum, applicable_industry, keywords, url, attachmentfile, file_message, content, div_content, ishelper, status, viewtimes)
                                     VALUES ('{item['url_id']}', '{item['title']}', '{item['city']}', '{item['policy_type']}', '{item['issuing_department']}', '{item['publishtime']}', '{item['dispatchtime']}', '{item['dispatchnum']}', '{item['applicable_industry']}', '{item['keywords']}', '{item['url']}', '{item['attachmentfile']}', '{item['file_message']}', '{item['content']}', '{item['div_content']}', {item['ishelper']}, '{item['status']}', '{item['viewtimes']}')"""
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败===============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "quanhuiqi_explain_policy":
            try:
                self.cur.execute(
                    f"""INSERT INTO public.t_zx_quanhuiqi_explain_policy (attachmentfile, content, div_content, dispatchdeparttaglistshow, url_id, ishelper, policyid, policytitle, ptype, publishtime, title, viewtimes, url)
                                     VALUES ('{item['attachmentfile']}', '{item['content']}', '{item['div_content']}', '{item['dispatchdeparttaglistshow']}', '{item['url_id']}', '{item['ishelper']}', '{item['policyid']}', '{item['policytitle']}', '{item['ptype']}', '{item['publishtime']}', '{item['title']}', '{item['viewtimes']}', '{item['url']}')"""
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败===============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "quanhuiqi_declare_policy":
            try:
                self.cur.execute(
                    f"""INSERT INTO public.t_zx_quanhuiqi_declare_policy (url, applicationstatus, content, div_content, applicationtimeend, applicationtimese, applicationtimestart, applicationtimetype, applicationtype, area, attachmentfile, dispatchdeparttaglistshow, distanceend, distancestart, url_id, industry, isnotapp, ispublicity, ispublicity2, ispublicity3, ispublicity4, level, policytitle, policytype, policyid, processdefinitionkey, publish, publishtime, suitable, title, year)
                                     VALUES ('{item["url"]}', '{item["applicationstatus"]}', '{item["content"]}', '{item["div_content"]}', '{item["applicationtimeend"]}', '{item["applicationtimese"]}', '{item["applicationtimestart"]}', '{item["applicationtimetype"]}', '{item["applicationtype"]}', '{item["area"]}', '{item["attachmentfile"]}', '{item["dispatchdeparttaglistshow"]}', '{item["distanceend"]}', '{item["distancestart"]}', '{item["url_id"]}', '{item["industry"]}', '{item["isnotapp"]}', '{item["ispublicity"]}', '{item["ispublicity2"]}', '{item["ispublicity3"]}', '{item["ispublicity4"]}', '{item["level"]}', '{item["policytitle"]}', '{item["policytype"]}', '{item["policyid"]}', '{item["processdefinitionkey"]}', '{item["publish"]}', '{item["publishtime"]}', '{item["suitable"]}', '{item["title"]}', '{item["year"]}')"""
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败===============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "shandong_gov_focus":
            try:
                self.cur.execute(
                    f"INSERT INTO public.t_zx_shandong_gov_focus (url, title, datetime, source_type, content, div_content) VALUES ('{item['url']}', '{item['title']}', '{item['datetime']}', '{item['source_type']}', '{item['content']}', '{item['div_content']}')"
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败===============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "t_zx_zccx_qingdao_policy_declaration":
            try:
                self.cur.execute(
                    "INSERT INTO t_zx_zccx_qingdao_policy_declaration (languageType,baseId,policyType,policyTitle,sendingGov,sendingGovId,policyTheme,sendingSize,issueDate,endDate,city,useType,browseNum,policyContent,writeDate,isLose,loseDate,attachmentVoList,basisVoList) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        item["languageType"],
                        item["baseId"],
                        item["policyType"],
                        item["policyTitle"],
                        item["sendingGov"],
                        item["sendingGovId"],
                        item["policyTheme"],
                        item["sendingSize"],
                        item["issueDate"],
                        item["endDate"],
                        item["city"],
                        item["useType"],
                        item["browseNum"],
                        item["policyContent"],
                        item["writeDate"],
                        item["isLose"],
                        item["loseDate"],
                        item["attachmentVoList"],
                        item["basisVoList"],
                    ),
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败==============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "t_zx_zccx_qingdao_policy_interpretation":
            try:
                self.cur.execute(
                    "INSERT INTO t_zx_zccx_qingdao_policy_interpretation (baseId,title,type,content,baseCreateTime,views) VALUES(%s,%s,%s,%s,%s,%s)",
                    (
                        item["baseId"],
                        item["title"],
                        item["type"],
                        item["content"],
                        item["baseCreateTime"],
                        item["views"],
                    ),
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败==============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "t_zx_smesd_policy":
            try:
                self.cur.execute(
                    "INSERT INTO t_zx_smesd_policy (webSource,viewCount,typeName,type,tsViewCount,topTime,topSort,topPic,title,tagName,synchTime,supportmodeName,subTitle,source,read,policyTypeName,personalgroupName,newTypeName,newType,keywordTagName,isTop,industryDomainName,emotionTagName,emotionTag,deptName,creatorName,creator,content,baseUpdateTime,baseNote,baseId,baseCreateTime,auditTime,auditState,areaNamer,page) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        item["webSource"],
                        item["viewCount"],
                        item["typeName"],
                        item["type"],
                        item["tsViewCount"],
                        item["topTime"],
                        item["topSort"],
                        item["topPic"],
                        item["title"],
                        item["tagName"],
                        item["synchTime"],
                        item["supportmodeName"],
                        item["subTitle"],
                        item["source"],
                        item["read"],
                        item["policyTypeName"],
                        item["personalgroupName"],
                        item["newTypeName"],
                        item["newType"],
                        item["keywordTagName"],
                        item["isTop"],
                        item["industryDomainName"],
                        item["emotionTagName"],
                        item["emotionTag"],
                        item["deptName"],
                        item["creatorName"],
                        item["creator"],
                        item["content"],
                        item["baseUpdateTime"],
                        item["baseNote"],
                        item["baseId"],
                        item["baseCreateTime"],
                        item["auditTime"],
                        item["auditState"],
                        item["areaNamer"],
                        item["page"],
                    ),
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败==============", e)
                self.connection.rollback()
        elif item["spider_name"] == "t_zx_smesd_policy_information":
            try:
                self.cur.execute(
                    "INSERT INTO t_zx_smesd_policy_information (baseId,title,viewCount,baseCreateTime,type,isHot,policyId,picUrl,content,policy,page) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        item["baseId"],
                        item["title"],
                        item["viewCount"],
                        item["baseCreateTime"],
                        item["type"],
                        item["isHot"],
                        item["policyId"],
                        item["picUrl"],
                        item["content"],
                        item["policy"],
                        item["page"],
                    ),
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败==============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "smesd_project_report":
            try:
                self.cur.execute(
                    f"""INSERT INTO public.t_zx_smesd_project_report (mx_url, url, statustext, leftday, detailstatustext, baseid, isqnsb, validityperiodstart, validityperiodend, starttime, endtime, nextapplydate, isimportant, sort, parentid, place, type_, province, city, district, applyurl, styleid, financemeasure, financemeasurelist, competentdepartment, source, description, rewardmoney, conditions, conditionslist, departmentphone, departmentphonelist, systemtype, logicrelation, logicdesc, viewcount, basecreatetime, baseupdatetime, instructions, creator, taxdiscount, iszqsb, isdelete, id_, subjectkeyword, creatorname, audittime, auditstate, dept, method, personalgroup, scale, policy, industry, reward, projecttype, placename, provincename, cityname, districtname, areaname, methodname, scalename, deptname, industryname, personalgroupname, rewardname, projecttypename, applytime, coreid, shorturl, sname)
                                    VALUES ('{item['mx_url']}', '{item['url']}', '{item['statustext']}', '{item['leftday']}', '{item['detailstatustext']}', '{item['baseid']}', '{item['isqnsb']}', '{item['validityperiodstart']}', '{item['validityperiodend']}', '{item['starttime']}', '{item['endtime']}', '{item['nextapplydate']}', '{item['isimportant']}', '{item['sort']}', '{item['parentid']}', '{item['place']}', '{item['type_']}', '{item['province']}', '{item['city']}', '{item['district']}', '{item['applyurl']}', '{item['styleid']}', '{item['financemeasure']}', '{item['financemeasurelist']}', '{item['competentdepartment']}', '{item['source']}', '{item['description']}', '{item['rewardmoney']}', '{item['conditions']}', '{item['conditionslist']}', '{item['departmentphone']}', '{item['departmentphonelist']}', '{item['systemtype']}', '{item['logicrelation']}', '{item['logicdesc']}', '{item['viewcount']}', '{item['basecreatetime']}', '{item['baseupdatetime']}', '{item['instructions']}', '{item['creator']}', '{item['taxdiscount']}', '{item['iszqsb']}', '{item['isdelete']}', '{item['id_']}', '{item['subjectkeyword']}', '{item['creatorname']}', '{item['audittime']}', '{item['auditstate']}', '{item['dept']}', '{item['method']}', '{item['personalgroup']}', '{item['scale']}', '{item['policy']}', '{item['industry']}', '{item['reward']}', '{item['projecttype']}', '{item['placename']}', '{item['provincename']}', '{item['cityname']}', '{item['districtname']}', '{item['areaname']}', '{item['methodname']}', '{item['scalename']}', '{item['deptname']}', '{item['industryname']}', '{item['personalgroupname']}', '{item['rewardname']}', '{item['projecttypename']}', '{item['applytime']}', '{item['coreid']}', '{item['shorturl']}', '{item['sname']}');
                                    """
                )
                logger.info("=====================插入成功======================")
                self.connection.commit()
            except Exception as e:
                logger.info(
                    f"""INSERT INTO public.t_zx_smesd_project_report (mx_url, url, statustext, leftday, detailstatustext, baseid, isqnsb, validityperiodstart, validityperiodend, starttime, endtime, nextapplydate, isimportant, sort, parentid, place, type_, province, city, district, applyurl, styleid, financemeasure, financemeasurelist, competentdepartment, source, description, rewardmoney, conditions, conditionslist, departmentphone, departmentphonelist, systemtype, logicrelation, logicdesc, viewcount, basecreatetime, baseupdatetime, instructions, creator, taxdiscount, iszqsb, isdelete, id_, subjectkeyword, creatorname, audittime, auditstate, dept, method, personalgroup, scale, policy, industry, reward, projecttype, placename, provincename, cityname, districtname, areaname, methodname, scalename, deptname, industryname, personalgroupname, rewardname, projecttypename, applytime, coreid, shorturl, sname)
                                    VALUES ('{item['mx_url']}', '{item['url']}', '{item['statustext']}', '{item['leftday']}', '{item['detailstatustext']}', '{item['baseid']}', '{item['isqnsb']}', '{item['validityperiodstart']}', '{item['validityperiodend']}', '{item['starttime']}', '{item['endtime']}', '{item['nextapplydate']}', '{item['isimportant']}', '{item['sort']}', '{item['parentid']}', '{item['place']}', '{item['type_']}', '{item['province']}', '{item['city']}', '{item['district']}', '{item['applyurl']}', '{item['styleid']}', '{item['financemeasure']}', '{item['financemeasurelist']}', '{item['competentdepartment']}', '{item['source']}', '{item['description']}', '{item['rewardmoney']}', '{item['conditions']}', '{item['conditionslist']}', '{item['departmentphone']}', '{item['departmentphonelist']}', '{item['systemtype']}', '{item['logicrelation']}', '{item['logicdesc']}', '{item['viewcount']}', '{item['basecreatetime']}', '{item['baseupdatetime']}', '{item['instructions']}', '{item['creator']}', '{item['taxdiscount']}', '{item['iszqsb']}', '{item['isdelete']}', '{item['id_']}', '{item['subjectkeyword']}', '{item['creatorname']}', '{item['audittime']}', '{item['auditstate']}', '{item['dept']}', '{item['method']}', '{item['personalgroup']}', '{item['scale']}', '{item['policy']}', '{item['industry']}', '{item['reward']}', '{item['projecttype']}', '{item['placename']}', '{item['provincename']}', '{item['cityname']}', '{item['districtname']}', '{item['areaname']}', '{item['methodname']}', '{item['scalename']}', '{item['deptname']}', '{item['industryname']}', '{item['personalgroupname']}', '{item['rewardname']}', '{item['projecttypename']}', '{item['applytime']}', '{item['coreid']}', '{item['shorturl']}', '{item['sname']}');
                                    """
                )
                logger.info("===============插入数据失败===============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "smesd_policy_news_bulletin":
            try:
                self.cur.execute(
                    f"""INSERT INTO public.t_zx_smesd_policy_news_bulletin (mx_url, baseid, title, content, viewcount, topnew, source, genre, fullname, fullpath, fullnewname, category, sourcelevel, isshow, ishot, basecreatetime, baseupdatetime, isdelete, creator)
                                    VALUES ('{item['mx_url']}', '{item['baseid']}', '{item['title']}', '{item['content']}', '{item['viewcount']}', '{item['topnew']}', '{item['source']}', '{item['genre']}', '{item['fullname']}', '{item['fullpath']}', '{item['fullnewname']}', '{item['category']}', '{item['sourcelevel']}', '{item['isshow']}', '{item['ishot']}', '{item['basecreatetime']}', '{item['baseupdatetime']}', '{item['isdelete']}', '{item['creator']}');
                                    """
                )
                logger.info("=====================插入成功======================")
                self.connection.commit()
            except Exception as e:
                logger.info(
                    f"""INSERT INTO public.t_zx_smesd_policy_news_bulletin (mx_url, baseid, title, content, viewcount, topnew, source, genre, fullname, fullpath, fullnewname, category, sourcelevel, isshow, ishot, basecreatetime, baseupdatetime, isdelete, creator)
                                    VALUES ('{item['mx_url']}', '{item['baseid']}', '{item['title']}', '{item['content']}', '{item['viewcount']}', '{item['topnew']}', '{item['source']}', '{item['genre']}', '{item['fullname']}', '{item['fullpath']}', '{item['fullnewname']}', '{item['category']}', '{item['sourcelevel']}', '{item['isshow']}', '{item['ishot']}', '{item['basecreatetime']}', '{item['baseupdatetime']}', '{item['isdelete']}', '{item['creator']}');
                                    """
                )
                logger.info("===============插入数据失败===============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "t_zx_smesd_policy_announcement":
            try:
                self.cur.execute(
                    "INSERT INTO t_zx_smesd_policy_announcement (baseId,title,content,viewCount,topNew,source,genre,fullName,fullPath,fullNewName,category,sourceLevel,isShow,isHot,baseCreateTime,baseUpdateTime,isDelete,creator,page) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        item["baseId"],
                        item["title"],
                        item["content"],
                        item["viewCount"],
                        item["topNew"],
                        item["source"],
                        item["genre"],
                        item["fullName"],
                        item["fullPath"],
                        item["fullNewName"],
                        item["category"],
                        item["sourceLevel"],
                        item["isShow"],
                        item["isHot"],
                        item["baseCreateTime"],
                        item["baseUpdateTime"],
                        item["isDelete"],
                        item["creator"],
                        item["page"],
                    ),
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败==============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "jnjxw_jinan_gov_work_trend":
            try:
                self.cur.execute(
                    f"""INSERT INTO public.t_zx_jnjxw_jinan_gov_work_trend (url, title, content, div_content, datetime, source_type, url_id)
                                    VALUES ('{item['url']}', '{item['title']}', '{item['content']}', '{item['div_content']}', '{item['datetime']}', '{item['source_type']}', '{item['url_id']}' );
                                    """
                )
                logger.info("=====================插入成功======================")
                self.connection.commit()
            except Exception as e:
                logger.info(
                    f"""INSERT INTO public.t_zx_jnjxw_jinan_gov_work_trend (url, title, content, div_content, datetime, source_type, url_id)
                                    VALUES ('{item['url']}', '{item['title']}', '{item['content']}', '{item['div_content']}', '{item['datetime']}', '{item['source_type']}', '{item['url_id']}' );
                                    """
                )
                logger.info("===============插入数据失败===============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "jnjxw_jinan_gov_district_message":
            try:
                self.cur.execute(
                    f"""INSERT INTO public.t_zx_jnjxw_jinan_gov_district_message (url, title, content, div_content, datetime, source_type, url_id)
                                    VALUES ('{item['url']}', '{item['title']}', '{item['content']}', '{item['div_content']}', '{item['datetime']}', '{item['source_type']}', '{item['url_id']}' );
                                    """
                )
                logger.info("=====================插入成功======================")
                self.connection.commit()
            except Exception as e:
                logger.info(
                    f"""INSERT INTO public.t_zx_jnjxw_jinan_gov_district_message (url, title, content, div_content, datetime, source_type, url_id)
                                    VALUES ('{item['url']}', '{item['title']}', '{item['content']}', '{item['div_content']}', '{item['datetime']}', '{item['source_type']}', '{item['url_id']}' );
                                    """
                )
                logger.info("===============插入数据失败===============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "jnjxw_jinan_gov_inform_public":
            try:
                self.cur.execute(
                    f"""INSERT INTO public.t_zx_jnjxw_jinan_gov_inform_public (url, title, content, div_content, datetime, source_type, url_id)
                                    VALUES ('{item['url']}', '{item['title']}', '{item['content']}', '{item['div_content']}', '{item['datetime']}', '{item['source_type']}', '{item['url_id']}' );
                                    """
                )
                logger.info("=====================插入成功======================")
                self.connection.commit()
            except Exception as e:
                logger.info(
                    f"""INSERT INTO public.t_zx_jnjxw_jinan_gov_inform_public (url, title, content, div_content, datetime, source_type, url_id)
                                    VALUES ('{item['url']}', '{item['title']}', '{item['content']}', '{item['div_content']}', '{item['datetime']}', '{item['source_type']}', '{item['url_id']}' );
                                    """
                )
                logger.info("===============插入数据失败===============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "people_message_report_tiny":
            try:
                self.cur.execute(
                    f"""INSERT INTO public.t_zx_people_message_report_tiny (url, title, content, div_content, datetime, source_type, url_id)
                                    VALUES ('{item['url']}', '{item['title']}', '{item['content']}', '{item['div_content']}', '{item['datetime']}', '{item['source_type']}', '{item['url_id']}' );
                                    """
                )
                logger.info("=====================插入成功======================")
                self.connection.commit()
            except Exception as e:
                logger.info(
                    f"""INSERT INTO t_zx_people_message_report_tiny (url, title, content, div_content, datetime, source_type, url_id)
                                    VALUES ('{item['url']}', '{item['title']}', '{item['content']}', '{item['div_content']}', '{item['datetime']}', '{item['source_type']}', '{item['url_id']}' );
                                    """
                )
                logger.info("===============插入数据失败===============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "shanghai_stock_exchange_annual_report":
            try:
                self.cur.execute(
                    f"""INSERT INTO shanghai_stock_exchange (bulletin_type_desc, bulletin_year, is_holder_disclose, org_bulletin_id, org_file_type, security_code, security_name, ssedate, title, pdf_url, creat_time)
                                    VALUES ('{item['bulletin_type_desc']}', '{item['bulletin_year']}', '{item['is_holder_disclose']}', '{item['org_bulletin_id']}', '{item['org_file_type']}', '{item['security_code']}', '{item['security_name']}', '{item['ssedate']}', '{item['title']}', '{item['pdf_url']}', '{item['creat_time']}' );
                                    """
                )
                logger.info("=====================插入成功======================")
                self.connection.commit()
            except Exception as e:
                logger.info(
                    f"""INSERT INTO public.shanghai_stock_exchange (bulletin_type_desc, bulletin_year, is_holder_disclose, org_bulletin_id, org_file_type, security_code, security_name, ssedate, title, pdf_url, creat_time)
                                    VALUES ('{item['bulletin_type_desc']}', '{item['bulletin_year']}', '{item['is_holder_disclose']}', '{item['org_bulletin_id']}', '{item['org_file_type']}', '{item['security_code']}', '{item['security_name']}', '{item['ssedate']}', '{item['title']}', '{item['pdf_url']}', '{item['creat_time']}' );
                                    """
                )
                logger.info("===============插入数据失败===============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "shenzhen_stock_exchange":
            try:
                self.cur.execute(
                    "INSERT INTO shenzhen_stock_exchange (id,annid,title,content,publishTime,attachPath,attachFormat,attachSize,secCode,secName,bondType,bigIndustryCode,bigCategoryId,smallCategoryId,channelCode,_index,download_page) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        item["id"],
                        item["annid"],
                        item["title"],
                        item["content"],
                        item["publishTime"],
                        item["attachPath"],
                        item["attachFormat"],
                        item["attachSize"],
                        item["secCode"],
                        item["secName"],
                        item["bondType"],
                        item["bigIndustryCode"],
                        item["bigCategoryId"],
                        item["smallCategoryId"],
                        item["channelCode"],
                        item["_index"],
                        item["download_page"],
                    ),
                )
                self.connection.commit()
            except Exception as e:
                logger.info("===============插入数据失败==============", e)
                self.connection.rollback()
            return item
        elif item["spider_name"] == "xinlang_companies_annals":
            try:
                self.cur.execute(
                    f"""INSERT INTO public.xinlang_companies_annals (code, zwjc, pdf_url, pdf_name)
                                VALUES ('{item['code']}', '{item['zwjc']}', '{item['pdf_url']}', '{item['pdf_name']}');
                                """
                )
                self.connection.commit()
            except Exception as e:
                logger.info("插入数据失败>>>>>>>>>>xinlang_companies_annals>>>>>>>>>>>>>>>", e)
                logger.info(
                    f"""INSERT INTO public.xinlang_companies_annals (code, zwjc, pdf_url, pdf_name)
                                VALUES ('{item['code']}', '{item['zwjc']}', '{item['pdf_url']}', '{item['pdf_name']}');
                                """
                )
                self.connection.rollback()
            return item
        elif item["spider_name"] == "juchao_annual_data":
            try:
                self.cur.execute(
                    f"""INSERT INTO public.juchao_annual_data  (id, seccode, secname, orgid, announcementid, announcementtitle, announcementtime, adjuncturl, adjunctsize, adjuncttype, storagetime, columnid, pagecolumn, announcementtype, associateannouncement, important, batchnum, announcementcontent, orgname, tilesecname, shorttitle, announcementtypename, secnamelist, pdf_url, creat_time)
                                VALUES ('{item['id']}', '{item['seccode']}', '{item['secname']}', '{item['orgid']}', '{item['announcementid']}', '{item['announcementtitle']}', '{item['announcementtime']}', '{item['adjuncturl']}', '{item['adjunctsize']}', '{item['adjuncttype']}', '{item['storagetime']}', '{item['columnid']}', '{item['pagecolumn']}', '{item['announcementtype']}', '{item['associateannouncement']}', '{item['important']}', '{item['batchnum']}', '{item['announcementcontent']}', '{item['orgname']}', '{item['tilesecname']}', '{item['shorttitle']}', '{item['announcementtypename']}', '{item['secnamelist']}', '{item['pdf_url']}', '{item['creat_time']}')
                                """
                )
                logger.info("=========插入成功=========")
                self.connection.commit()
            except Exception as e:
                logger.info("插入数据失败>>>>>>>>>>xinlang_companies_annals>>>>>>>>>>>>>>>", e)
                logger.info(
                    f"""INSERT INTO public.juchao_annual_data  (id, seccode, secname, orgid, announcementid, announcementtitle, announcementtime, adjuncturl, adjunctsize, adjuncttype, storagetime, columnid, pagecolumn, announcementtype, associateannouncement, important, batchnum, announcementcontent, orgname, tilesecname, shorttitle, announcementtypename, secnamelist, pdf_url, creat_time)
                                VALUES ('{item['id']}', '{item['seccode']}', '{item['secname']}', '{item['orgid']}', '{item['announcementid']}', '{item['announcementtitle']}', '{item['announcementtime']}', '{item['adjuncturl']}', '{item['adjunctsize']}', '{item['adjuncttype']}', '{item['storagetime']}', '{item['columnid']}', '{item['pagecolumn']}', '{item['announcementtype']}', '{item['associateannouncement']}', '{item['important']}', '{item['batchnum']}', '{item['announcementcontent']}', '{item['orgname']}', '{item['tilesecname']}', '{item['shorttitle']}', '{item['announcementtypename']}', '{item['secnamelist']}', '{item['pdf_url']}', '{item['creat_time']}')
                                """
                )
                self.connection.rollback()
            return item
        elif item["spider_name"] == "juchao_web_caiwu_data":
            try:
                self.cur.execute(
                    f"""INSERT INTO public.juchao_web_caiwu_data  (enddate, f004n, f008n, f010n, f011n, f016n, f017n, f022n, f023n, f025n, f026n, f029n, f041n, f042n, f043n, f052n, f053n, f054n, f056n, f058n, f067n, f078n, code, company, unique_id, creat_time)
                                VALUES ('{item['enddate']}', '{item['f004n']}', '{item['f008n']}', '{item['f010n']}', '{item['f011n']}', '{item['f016n']}', '{item['f017n']}', '{item['f022n']}', '{item['f023n']}', '{item['f025n']}', '{item['f026n']}', '{item['f029n']}', '{item['f041n']}', '{item['f042n']}', '{item['f043n']}', '{item['f052n']}', '{item['f053n']}', '{item['f054n']}', '{item['f056n']}', '{item['f058n']}', '{item['f067n']}', '{item['f078n']}', '{item['code']}', '{item['company']}', '{item['unique_id']}', '{item['creat_time']}')
                                """
                )
                logger.info("=========插入成功=========")
                self.connection.commit()
            except Exception as e:
                logger.info("插入数据失败>>>>>>>>>>juchao_web_caiwu_data>>>>>>>>>>>>>>>", e)
                logger.info(
                    f"""INSERT INTO public.juchao_web_caiwu_data  (enddate, f004n, f008n, f010n, f011n, f016n, f017n, f022n, f023n, f025n, f026n, f029n, f041n, f042n, f043n, f052n, f053n, f054n, f056n, f058n, f067n, f078n, creat_time)
                                VALUES ('{item['enddate']}', '{item['f004n']}', '{item['f008n']}', '{item['f010n']}', '{item['f011n']}', '{item['f016n']}', '{item['f017n']}', '{item['f022n']}', '{item['f023n']}', '{item['f025n']}', '{item['f026n']}', '{item['f029n']}', '{item['f041n']}', '{item['f042n']}', '{item['f043n']}', '{item['f052n']}', '{item['f053n']}', '{item['f054n']}', '{item['f056n']}', '{item['f058n']}', '{item['f067n']}', '{item['f078n']}', '{item['creat_time']}')
                                """
                )
                self.connection.rollback()
            return item
        elif item["spider_name"] == "juchao_web_social_responsibility_report":
            try:
                self.cur.execute(
                    f"""INSERT INTO public.juchao_web_social_responsibility_report (id, seccode, secname, orgid, announcementid, announcementtitle, announcementtime, adjuncturl, adjunctsize, adjuncttype, storagetime, columnid, pagecolumn, announcementtype, associateannouncement, important, batchnum, announcementcontent, orgname, tilesecname, shorttitle, announcementtypename, secnamelist, pdf_url, creat_time) 
                                VALUES ('{item['id']}', '{item['seccode']}', '{item['secname']}', '{item['orgid']}', '{item['announcementid']}', '{item['announcementtitle']}', '{item['announcementtime']}', '{item['adjuncturl']}', '{item['adjunctsize']}', '{item['adjuncttype']}', '{item['storagetime']}', '{item['columnid']}', '{item['pagecolumn']}', '{item['announcementtype']}', '{item['associateannouncement']}', '{item['important']}', '{item['batchnum']}', '{item['announcementcontent']}', '{item['orgname']}', '{item['tilesecname']}', '{item['shorttitle']}', '{item['announcementtypename']}', '{item['secnamelist']}', '{item['pdf_url']}', '{item['creat_time']}')
                                """
                )
                logger.info("=========插入成功=========")
                self.connection.commit()
            except Exception as e:
                logger.info("插入数据失败>>>>>>>>>>juchao_web_social_responsibility_report>>>>>>>>>>>>>>>", e)
                logger.info(
                    f"""INSERT INTO public.juchao_web_social_responsibility_report (id, seccode, secname, orgid, announcementid, announcementtitle, announcementtime, adjuncturl, adjunctsize, adjuncttype, storagetime, columnid, pagecolumn, announcementtype, associateannouncement, important, batchnum, announcementcontent, orgname, tilesecname, shorttitle, announcementtypename, secnamelist, pdf_url, creat_time) 
                                VALUES ('{item['id']}', '{item['seccode']}', '{item['secname']}', '{item['orgid']}', '{item['announcementid']}', '{item['announcementtitle']}', '{item['announcementtime']}', '{item['adjuncturl']}', '{item['adjunctsize']}', '{item['adjuncttype']}', '{item['storagetime']}', '{item['columnid']}', '{item['pagecolumn']}', '{item['announcementtype']}', '{item['associateannouncement']}', '{item['important']}', '{item['batchnum']}', '{item['announcementcontent']}', '{item['orgname']}', '{item['tilesecname']}', '{item['shorttitle']}', '{item['announcementtypename']}', '{item['secnamelist']}', '{item['pdf_url']}', '{item['creat_time']}')
                                """
                )
                self.connection.rollback()
            return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
