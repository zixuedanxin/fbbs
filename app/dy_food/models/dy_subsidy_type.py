# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: dy_subsidy_type 
# author: tangdayi
# data: 2018年03月19日 22时29分
# ===================================================

from odoo import models, fields, api


class DySubsidyType(models.Model):
    """
    补贴类型： 如：奖金，日常补贴，饭补，体检补贴，公交补，社会保险补贴等
    """
    _name = 'dy.subsidy.type'

    _description = u'如：奖金，日常补贴，饭补，体检补贴，公交补，社会保险补贴等'

    _order = 'id desc'

    name = fields.Char(string=u'名称')
    number = fields.Char(string=u'编号', default=lambda self: self.env['ir.sequence'].next_by_code(self._name))
    company_id = fields.Many2one('res.company', string=u'单位')
    is_all = fields.Boolean(string=u'是否全局', default=False)
    remark = fields.Char(string=u'备注')



