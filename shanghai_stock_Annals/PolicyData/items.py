# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class enterprisePolicyInterpretationItem(scrapy.Item):
    """
    国家中小企业政策资讯
    """

    spider_name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    publishNo = scrapy.Field()
    publishTime = scrapy.Field()
    execTime = scrapy.Field()
    deadTime = scrapy.Field()
    applyUrl = scrapy.Field()
    source = scrapy.Field()
    publishUnit = scrapy.Field()
    publishUnit2 = scrapy.Field()
    publishUnit3 = scrapy.Field()
    publishUnit4 = scrapy.Field()
    content = scrapy.Field()
    policyState = scrapy.Field()
    isTop = scrapy.Field()
    rightTop = scrapy.Field()
    pArticleState = scrapy.Field()
    pAnalyseState = scrapy.Field()
    policyType = scrapy.Field()
    pbmsm = scrapy.Field()
    videoUrl = scrapy.Field()
    subject = scrapy.Field()
    applicationType = scrapy.Field()
    url = scrapy.Field()
    specialType = scrapy.Field()
    urlmd5 = scrapy.Field()
    isCrawled = scrapy.Field()
    publishUnitFilter = scrapy.Field()
    createTime = scrapy.Field()
    creatorId = scrapy.Field()
    createUser = scrapy.Field()
    updateTime = scrapy.Field()
    updateUserId = scrapy.Field()
    updateUserName = scrapy.Field()
    delFlag = scrapy.Field()
    analyse = scrapy.Field()
    essence = scrapy.Field()
    policyType2 = scrapy.Field()
    policyType1 = scrapy.Field()
    policyType3 = scrapy.Field()
    policyType4 = scrapy.Field()
    orderBy = scrapy.Field()
    publishTimeTo = scrapy.Field()
    createTimeTo = scrapy.Field()
    percents = scrapy.Field()
    userId = scrapy.Field()
    topicType = scrapy.Field()
    isTopic = scrapy.Field()
    isCollect = scrapy.Field()
    fav_id = scrapy.Field()
    queryYear = scrapy.Field()
    panalyseState = scrapy.Field()
    particleState = scrapy.Field()
    sem_attachment = scrapy.Field()
    page = scrapy.Field()


class enterprisePolicyDeclarationItem(scrapy.Item):
    """
    国家中小企业政策申报信息
    """

    spider_name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    publishNo = scrapy.Field()
    publishTime = scrapy.Field()
    execTime = scrapy.Field()
    deadTime = scrapy.Field()
    applyUrl = scrapy.Field()
    source = scrapy.Field()
    publishUnit = scrapy.Field()
    publishUnit2 = scrapy.Field()
    publishUnit3 = scrapy.Field()
    publishUnit4 = scrapy.Field()
    content = scrapy.Field()
    policyState = scrapy.Field()
    isTop = scrapy.Field()
    rightTop = scrapy.Field()
    pArticleState = scrapy.Field()
    pAnalyseState = scrapy.Field()
    policyType = scrapy.Field()
    pbmsm = scrapy.Field()
    videoUrl = scrapy.Field()
    subject = scrapy.Field()
    applicationType = scrapy.Field()
    url = scrapy.Field()
    specialType = scrapy.Field()
    urlmd5 = scrapy.Field()
    isCrawled = scrapy.Field()
    publishUnitFilter = scrapy.Field()
    createTime = scrapy.Field()
    creatorId = scrapy.Field()
    createUser = scrapy.Field()
    updateTime = scrapy.Field()
    updateUserId = scrapy.Field()
    updateUserName = scrapy.Field()
    delFlag = scrapy.Field()
    analyse = scrapy.Field()
    essence = scrapy.Field()
    policyType2 = scrapy.Field()
    policyType1 = scrapy.Field()
    policyType3 = scrapy.Field()
    policyType4 = scrapy.Field()
    orderBy = scrapy.Field()
    publishTimeTo = scrapy.Field()
    createTimeTo = scrapy.Field()
    percents = scrapy.Field()
    userId = scrapy.Field()
    topicType = scrapy.Field()
    isTopic = scrapy.Field()
    isCollect = scrapy.Field()
    fav_id = scrapy.Field()
    queryYear = scrapy.Field()
    panalyseState = scrapy.Field()
    particleState = scrapy.Field()
    sem_attachment = scrapy.Field()
    page = scrapy.Field()


class qingdaoPolicyItem(scrapy.Item):
    """
    青岛政策通惠企政策
    """

    spider_name = scrapy.Field()
    languageType = scrapy.Field()
    baseId = scrapy.Field()
    policyType = scrapy.Field()
    policyTitle = scrapy.Field()
    sendingGov = scrapy.Field()
    sendingGovId = scrapy.Field()
    policyTheme = scrapy.Field()
    sendingSize = scrapy.Field()
    issueDate = scrapy.Field()
    endDate = scrapy.Field()
    city = scrapy.Field()
    useType = scrapy.Field()
    browseNum = scrapy.Field()
    policyContent = scrapy.Field()
    writeDate = scrapy.Field()
    isLose = scrapy.Field()
    loseDate = scrapy.Field()
    attachmentVoList = scrapy.Field()
    basisVoList = scrapy.Field()


class qingdaoPolicyInterpretationItem(scrapy.Item):
    """
    青岛政策通政策解读
    """

    spider_name = scrapy.Field()
    baseId = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    content = scrapy.Field()
    baseCreateTime = scrapy.Field()
    views = scrapy.Field()


class policyQingdaoGovItem(scrapy.Item):
    # define the fields for your item here like:
    spider_name = scrapy.Field()
    url = scrapy.Field()  # 详情页url
    wibsite = scrapy.Field()  # 网站
    title = scrapy.Field()  # 标题
    datetime = scrapy.Field()  # 发布时间
    source_type = scrapy.Field()  # 类型来源
    content = scrapy.Field()  # 正文内容
    div_content = scrapy.Field()  # div正文内容
    remark = scrapy.Field()  # 备注


class policyShandongGovItem(scrapy.Item):
    # define the fields for your item here like:
    spider_name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    datetime = scrapy.Field()
    source_type = scrapy.Field()
    content = scrapy.Field()
    div_content = scrapy.Field()


class policyJinanGovItem(scrapy.Item):
    # define the fields for your item here like:
    spider_name = scrapy.Field()
    url = scrapy.Field()
    pdf_url = scrapy.Field()
    title = scrapy.Field()
    datetime = scrapy.Field()
    source_type = scrapy.Field()
    content = scrapy.Field()
    div_content = scrapy.Field()


class policyQuanhuiqiItem(scrapy.Item):
    # define the fields for your item here like:
    spider_name = scrapy.Field()
    url_id = scrapy.Field()  # 网页内id
    title = scrapy.Field()  # 标题
    city = scrapy.Field()  # 城市
    policy_type = scrapy.Field()  # 政策类型
    issuing_department = scrapy.Field()  # 发文部门
    publishtime = scrapy.Field()  # 发布时间
    dispatchtime = scrapy.Field()  # 成文时间
    dispatchnum = scrapy.Field()  # 发文号
    applicable_industry = scrapy.Field()  # 适用行业
    keywords = scrapy.Field()  # 关键词
    url = scrapy.Field()  # url
    attachmentfile = scrapy.Field()  # 附件相关
    file_message = scrapy.Field()  # 附件信息
    content = scrapy.Field()  # 正文
    div_content = scrapy.Field()  # 带div正文
    ishelper = scrapy.Field()
    status = scrapy.Field()
    viewtimes = scrapy.Field()


class policyQuanhuiqiexplainItem(scrapy.Item):
    spider_name = scrapy.Field()
    url = scrapy.Field()
    attachmentfile = scrapy.Field()
    content = scrapy.Field()
    div_content = scrapy.Field()
    dispatchdeparttaglistshow = scrapy.Field()
    url_id = scrapy.Field()
    ishelper = scrapy.Field()
    policyid = scrapy.Field()
    policytitle = scrapy.Field()
    ptype = scrapy.Field()
    publishtime = scrapy.Field()
    title = scrapy.Field()
    viewtimes = scrapy.Field()


class policyQuanhuiqiDeclareItem(scrapy.Item):
    url = scrapy.Field()
    spider_name = scrapy.Field()
    applicationstatus = scrapy.Field()
    content = scrapy.Field()
    div_content = scrapy.Field()
    applicationtimeend = scrapy.Field()
    applicationtimese = scrapy.Field()
    applicationtimestart = scrapy.Field()
    applicationtimetype = scrapy.Field()
    applicationtype = scrapy.Field()
    area = scrapy.Field()
    attachmentfile = scrapy.Field()
    dispatchdeparttaglistshow = scrapy.Field()
    distanceend = scrapy.Field()
    distancestart = scrapy.Field()
    url_id = scrapy.Field()
    industry = scrapy.Field()
    isnotapp = scrapy.Field()
    ispublicity = scrapy.Field()
    ispublicity2 = scrapy.Field()
    ispublicity3 = scrapy.Field()
    ispublicity4 = scrapy.Field()
    level = scrapy.Field()
    policytitle = scrapy.Field()
    policytype = scrapy.Field()
    policyid = scrapy.Field()
    processdefinitionkey = scrapy.Field()
    publish = scrapy.Field()
    publishtime = scrapy.Field()
    suitable = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()


class qingdaoPolicydeclarationItem(scrapy.Item):
    """
    青岛政策通政策申报
    """

    spider_name = scrapy.Field()
    languageType = scrapy.Field()
    baseId = scrapy.Field()
    projectType = scrapy.Field()
    title = scrapy.Field()
    reportType = scrapy.Field()
    startDate = scrapy.Field()
    endDate = scrapy.Field()
    money = scrapy.Field()
    moneyUnit = scrapy.Field()
    maxReward = scrapy.Field()
    supportType = scrapy.Field()
    reportData = scrapy.Field()
    reportFlow = scrapy.Field()
    reportLink = scrapy.Field()
    reportDay = scrapy.Field()
    reportStatus = scrapy.Field()
    city = scrapy.Field()
    cityId = scrapy.Field()
    industry = scrapy.Field()
    compScale = scrapy.Field()
    compAttribute = scrapy.Field()
    buildYear = scrapy.Field()
    sendingGov = scrapy.Field()
    keyWords = scrapy.Field()
    theme = scrapy.Field()
    useType = scrapy.Field()
    specialPerson = scrapy.Field()
    browseNum = scrapy.Field()
    isCollect = scrapy.Field()
    dealAddress = scrapy.Field()
    content = scrapy.Field()
    reportCondition = scrapy.Field()
    dealDepart = scrapy.Field()
    dealDepartId = scrapy.Field()
    contactPerson = scrapy.Field()
    contactPhone = scrapy.Field()
    contactOffices = scrapy.Field()
    policyTitle = scrapy.Field()
    setNotice = scrapy.Field()
    sendingSize = scrapy.Field()
    isHasFeedBack = scrapy.Field()
    basisVoList = scrapy.Field()
    conditionVoList = scrapy.Field()
    contentVoList = scrapy.Field()
    contactVoList = scrapy.Field()
    questionVoList = scrapy.Field()
    attachmentVoList = scrapy.Field()
    publicityVoList = scrapy.Field()
    cityProject = scrapy.Field()
    relativeProject = scrapy.Field()
    isAddArea = scrapy.Field()
    applicationTemplate = scrapy.Field()
    page = scrapy.Field()


class smesdPolicyItem(scrapy.Item):
    """中小企业政策资讯"""

    spider_name = scrapy.Field()
    webSource = scrapy.Field()
    viewCount = scrapy.Field()
    typeName = scrapy.Field()
    type = scrapy.Field()
    tsViewCount = scrapy.Field()
    topTime = scrapy.Field()
    topSort = scrapy.Field()
    topPic = scrapy.Field()
    title = scrapy.Field()
    tagName = scrapy.Field()
    synchTime = scrapy.Field()
    supportmodeName = scrapy.Field()
    subTitle = scrapy.Field()
    source = scrapy.Field()
    read = scrapy.Field()
    policyTypeName = scrapy.Field()
    personalgroupName = scrapy.Field()
    newTypeName = scrapy.Field()
    newType = scrapy.Field()
    keywordTagName = scrapy.Field()
    isTop = scrapy.Field()
    industryDomainName = scrapy.Field()
    emotionTagName = scrapy.Field()
    emotionTag = scrapy.Field()
    deptName = scrapy.Field()
    creatorName = scrapy.Field()
    creator = scrapy.Field()
    content = scrapy.Field()
    baseUpdateTime = scrapy.Field()
    baseNote = scrapy.Field()
    baseId = scrapy.Field()
    baseCreateTime = scrapy.Field()
    auditTime = scrapy.Field()
    auditState = scrapy.Field()
    areaNamer = scrapy.Field()
    page = scrapy.Field()


class smesdpolicyInformationItem(scrapy.Item):
    """中小企业政策解读"""

    spider_name = scrapy.Field()
    baseId = scrapy.Field()
    title = scrapy.Field()
    viewCount = scrapy.Field()
    baseCreateTime = scrapy.Field()
    type = scrapy.Field()
    isHot = scrapy.Field()
    policyId = scrapy.Field()
    picUrl = scrapy.Field()
    content = scrapy.Field()
    policy = scrapy.Field()
    page = scrapy.Field()


class policySmesdProjectItem(scrapy.Item):
    spider_name = scrapy.Field()
    url = scrapy.Field()
    mx_url = scrapy.Field()
    statustext = scrapy.Field()
    leftday = scrapy.Field()
    detailstatustext = scrapy.Field()
    baseid = scrapy.Field()
    isqnsb = scrapy.Field()
    validityperiodstart = scrapy.Field()
    validityperiodend = scrapy.Field()
    starttime = scrapy.Field()
    endtime = scrapy.Field()
    nextapplydate = scrapy.Field()
    isimportant = scrapy.Field()
    sort = scrapy.Field()
    parentid = scrapy.Field()
    place = scrapy.Field()
    type_ = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    applyurl = scrapy.Field()
    styleid = scrapy.Field()
    financemeasure = scrapy.Field()
    financemeasurelist = scrapy.Field()
    competentdepartment = scrapy.Field()
    source = scrapy.Field()
    description = scrapy.Field()
    rewardmoney = scrapy.Field()
    conditions = scrapy.Field()
    conditionslist = scrapy.Field()
    departmentphone = scrapy.Field()
    departmentphonelist = scrapy.Field()
    systemtype = scrapy.Field()
    logicrelation = scrapy.Field()
    logicdesc = scrapy.Field()
    viewcount = scrapy.Field()
    basecreatetime = scrapy.Field()
    baseupdatetime = scrapy.Field()
    instructions = scrapy.Field()
    creator = scrapy.Field()
    taxdiscount = scrapy.Field()
    iszqsb = scrapy.Field()
    isdelete = scrapy.Field()
    id_ = scrapy.Field()
    subjectkeyword = scrapy.Field()
    creatorname = scrapy.Field()
    audittime = scrapy.Field()
    auditstate = scrapy.Field()
    dept = scrapy.Field()
    method = scrapy.Field()
    personalgroup = scrapy.Field()
    scale = scrapy.Field()
    policy = scrapy.Field()
    industry = scrapy.Field()
    reward = scrapy.Field()
    projecttype = scrapy.Field()
    placename = scrapy.Field()
    provincename = scrapy.Field()
    cityname = scrapy.Field()
    districtname = scrapy.Field()
    areaname = scrapy.Field()
    methodname = scrapy.Field()
    scalename = scrapy.Field()
    deptname = scrapy.Field()
    industryname = scrapy.Field()
    personalgroupname = scrapy.Field()
    rewardname = scrapy.Field()
    projecttypename = scrapy.Field()
    applytime = scrapy.Field()
    coreid = scrapy.Field()
    shorturl = scrapy.Field()
    sname = scrapy.Field()


class smesdpolicyNewsBulletinItem(scrapy.Item):
    """中小企业政策解读"""

    spider_name = scrapy.Field()
    mx_url = scrapy.Field()
    baseid = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    viewcount = scrapy.Field()
    topnew = scrapy.Field()
    source = scrapy.Field()
    genre = scrapy.Field()
    fullname = scrapy.Field()
    fullpath = scrapy.Field()
    fullnewname = scrapy.Field()
    category = scrapy.Field()
    sourcelevel = scrapy.Field()
    isshow = scrapy.Field()
    ishot = scrapy.Field()
    basecreatetime = scrapy.Field()
    baseupdatetime = scrapy.Field()
    isdelete = scrapy.Field()
    creator = scrapy.Field()


class smesdpolicyAnnouncementItem(scrapy.Item):
    """中小企业通知公告"""

    spider_name = scrapy.Field()
    baseId = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    viewCount = scrapy.Field()
    topNew = scrapy.Field()
    source = scrapy.Field()
    genre = scrapy.Field()
    fullName = scrapy.Field()
    fullPath = scrapy.Field()
    fullNewName = scrapy.Field()
    category = scrapy.Field()
    sourceLevel = scrapy.Field()
    isShow = scrapy.Field()
    isHot = scrapy.Field()
    baseCreateTime = scrapy.Field()
    baseUpdateTime = scrapy.Field()
    isDelete = scrapy.Field()
    creator = scrapy.Field()
    page = scrapy.Field()


class JnjxwGovWorkTrendItem(scrapy.Item):
    """
    济南市工业和信息化局-工信动态-工作动态
    济南市工业和信息化局-工信动态-区县信息
    济南市工业和信息化局-工信动态-公共通知
    人民号-工信微报
    """

    spider_name = scrapy.Field()
    url = scrapy.Field()
    url_id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    div_content = scrapy.Field()
    datetime = scrapy.Field()
    source_type = scrapy.Field()


class ShanghaiStorkExchangeItem(scrapy.Item):
    """上交所-年报"""

    spider_name = scrapy.Field()
    bulletin_type_desc = scrapy.Field()
    bulletin_year = scrapy.Field()
    is_holder_disclose = scrapy.Field()
    org_bulletin_id = scrapy.Field()
    org_file_type = scrapy.Field()
    security_code = scrapy.Field()
    security_name = scrapy.Field()
    ssedate = scrapy.Field()
    title = scrapy.Field()
    pdf_url = scrapy.Field()
    creat_time = scrapy.Field()


class stockExchangeItem(scrapy.Item):
    """
    深圳证券交易所
    """

    spider_name = scrapy.Field()
    id = scrapy.Field()
    annid = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    publishTime = scrapy.Field()
    attachPath = scrapy.Field()
    attachFormat = scrapy.Field()
    attachSize = scrapy.Field()
    secCode = scrapy.Field()
    secName = scrapy.Field()
    bondType = scrapy.Field()
    bigIndustryCode = scrapy.Field()
    bigCategoryId = scrapy.Field()
    smallCategoryId = scrapy.Field()
    channelCode = scrapy.Field()
    _index = scrapy.Field()
    download_page = scrapy.Field()


class XinlangCompaniesItem(scrapy.Item):
    """
    深圳证券交易所
    """

    spider_name = scrapy.Field()
    code = scrapy.Field()
    pdf_url = scrapy.Field()
    pdf_name = scrapy.Field()
    zwjc = scrapy.Field()


class JuchaoAppAnnualItem(scrapy.Item):
    """
    巨潮app-年报
    """

    spider_name = scrapy.Field()
    id = scrapy.Field()
    seccode = scrapy.Field()
    secname = scrapy.Field()
    orgid = scrapy.Field()
    announcementid = scrapy.Field()
    announcementtitle = scrapy.Field()
    announcementtime = scrapy.Field()
    adjuncturl = scrapy.Field()
    adjunctsize = scrapy.Field()
    adjuncttype = scrapy.Field()
    storagetime = scrapy.Field()
    columnid = scrapy.Field()
    pagecolumn = scrapy.Field()
    announcementtype = scrapy.Field()
    associateannouncement = scrapy.Field()
    important = scrapy.Field()
    batchnum = scrapy.Field()
    announcementcontent = scrapy.Field()
    orgname = scrapy.Field()
    tilesecname = scrapy.Field()
    shorttitle = scrapy.Field()
    announcementtypename = scrapy.Field()
    secnamelist = scrapy.Field()
    pdf_url = scrapy.Field()
    creat_time = scrapy.Field()


class JuchaoWebCaiwuData(scrapy.Item):

    spider_name = scrapy.Field()
    enddate = scrapy.Field()
    f004n = scrapy.Field()
    f008n = scrapy.Field()
    f010n = scrapy.Field()
    f011n = scrapy.Field()
    f016n = scrapy.Field()
    f017n = scrapy.Field()
    f022n = scrapy.Field()
    f023n = scrapy.Field()
    f025n = scrapy.Field()
    f026n = scrapy.Field()
    f029n = scrapy.Field()
    f041n = scrapy.Field()
    f042n = scrapy.Field()
    f043n = scrapy.Field()
    f052n = scrapy.Field()
    f053n = scrapy.Field()
    f054n = scrapy.Field()
    f056n = scrapy.Field()
    f058n = scrapy.Field()
    f067n = scrapy.Field()
    f078n = scrapy.Field()
    code = scrapy.Field()
    company = scrapy.Field()
    unique_id = scrapy.Field()
    creat_time = scrapy.Field()


class JuchaoWebSocialResponsibilityData(scrapy.Item):

    spider_name = scrapy.Field()
    id = scrapy.Field()
    seccode = scrapy.Field()
    secname = scrapy.Field()
    orgid = scrapy.Field()
    announcementid = scrapy.Field()
    announcementtitle = scrapy.Field()
    announcementtime = scrapy.Field()
    adjuncturl = scrapy.Field()
    adjunctsize = scrapy.Field()
    adjuncttype = scrapy.Field()
    storagetime = scrapy.Field()
    columnid = scrapy.Field()
    pagecolumn = scrapy.Field()
    announcementtype = scrapy.Field()
    associateannouncement = scrapy.Field()
    important = scrapy.Field()
    batchnum = scrapy.Field()
    announcementcontent = scrapy.Field()
    orgname = scrapy.Field()
    tilesecname = scrapy.Field()
    shorttitle = scrapy.Field()
    announcementtypename = scrapy.Field()
    secnamelist = scrapy.Field()
    pdf_url = scrapy.Field()
    creat_time = scrapy.Field()