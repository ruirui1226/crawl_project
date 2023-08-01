# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BidScrapyProjectItem(scrapy.Item):
    bid_id = scrapy.Field()  # 经过md5后的唯一id
    create_datetime = scrapy.Field()
    bid_url = scrapy.Field()  # 详情链接
    bid_md5_url = scrapy.Field()  # 特殊网站加密详情链接
    bid_province = scrapy.Field()  # 省份
    bid_city = scrapy.Field()  # 市
    bid_county = scrapy.Field()  # 县
    bid_zone = scrapy.Field()  # 所属专区
    bid_category = scrapy.Field()  # 大分类
    bid_info_type = scrapy.Field()  # 二级类别
    bid_source = scrapy.Field()  # 来源网站
    bid_name = scrapy.Field()  # 标题
    bid_public_time = scrapy.Field()  # 发布时间
    bid_html_con = scrapy.Field()  # 带有html的文本
    bid_content = scrapy.Field()  # 纯净文本
    bid_json_data = scrapy.Field()  # 详情json
    bid_industry = scrapy.Field()  # 所属行业
    bid_orgin_url = scrapy.Field()  # 原始链接 （接口链接）
    description = scrapy.Field()  # 描述
    website_name = scrapy.Field()  # 网站
    website_url = scrapy.Field()  # 网站链接
    list_parse = scrapy.Field()  # 列表获取详情去重使用


class GovernmentProcurementItem(scrapy.Item):
    po_id = scrapy.Field()  # url md5
    bid_url = scrapy.Field()  # 详情url
    po_province = scrapy.Field()  # 省
    po_city = scrapy.Field()  # url 市
    po_zone = scrapy.Field()  # 所属专区
    po_county = scrapy.Field()  # url 区
    po_industry = scrapy.Field()  # 所属行业
    po_category = scrapy.Field()  # 采购类别
    po_info_type = scrapy.Field()  # 采购类型
    po_public_time = scrapy.Field()  # 采购发布时间
    bo_name = scrapy.Field()  # 采购标题
    po_source = scrapy.Field()  # 采购数据来源
    po_html_con = scrapy.Field()  # 采购网页内容
    po_content = scrapy.Field()  # 采购详情
    po_json_data = scrapy.Field()  # json
    description = scrapy.Field()  # 描述
    website_name = scrapy.Field()  # 网站
    website_url = scrapy.Field()  # 网站链接
    bid_orgin_url = scrapy.Field()  # 原始网页链接
    create_datetime = scrapy.Field()  # 创建时间
    list_parse = scrapy.Field()  # 列表获取详情去重使用
