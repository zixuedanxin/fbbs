# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: dy_store_category 
# author: tangdayi
# data: 2018年03月16日 22时50分
# ===================================================


from odoo import fields, models, api


class DyStoreType(models.Model):
    """
    餐管类型
    餐馆类类型，酒店，餐厅，小吃，饭店
    """

    _name = 'dy.store.type'

    _description = u'餐馆类型，酒店，餐厅，小吃，饭店'

    _order = 'id desc'

    name = fields.Char(string=u'名称', required=True)
    number = fields.Char(string=u'编号')
    remark = fields.Char(string=u'备注')