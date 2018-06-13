# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: dy_subsidy_model 
# author: tangdayi
# data: 2018年03月21日 19时19分
# ===================================================


from odoo import fields, api, models


class DySubsidyModel(models.Model):
    """
    补贴模式
    如：按月补贴，按餐补贴等
    """
    _name = 'dy.subsidy.model'

    _description = u'补贴模式'

    _order = 'id desc'

    name = fields.Char(string=u'名称', help=u'按月补贴，按餐补贴')
    number = fields.Char(string=u'编号', default=lambda self: self.env['ir.sequence'].next_by_code(self._name))
    company_id = fields.Many2one('res.company', string=u'公司')
    is_all = fields.Boolean(string=u'是否全局', default=False)
    active = fields.Boolean(string=u'有效')
    remark = fields.Char(string=u'备注')

