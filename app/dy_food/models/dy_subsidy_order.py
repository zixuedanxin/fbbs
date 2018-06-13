# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: dy_subsidy 
# author: tangdayi
# data: 2018年03月19日 22时26分
# ===================================================

from odoo import fields, models, api
from odoo.addons import decimal_precision as dp
from tools.ydt.utils import today


class DySubsidyOrder(models.Model):

    """
    补贴单
    补贴单：公司针对餐馆和员工的补贴，
    形式：通过发放补贴金额形式返回
    """
    _name = 'dy.subsidy.order'

    _description = u'补贴单：公司针对餐馆和员工的补贴， 形式：通过发放补贴金额形式返回'

    _order = 'id desc'

    name = fields.Char(string=u'补贴名称', required=True)
    number = fields.Char(string=u'编号', readnoly=True,
                         default=lambda self: self.env['ir.sequence'].next_by_code(self._name))
    company_id = fields.Many2one('res.company', string=u'所属单位')
    biz_date = fields.Date(string=u'业务日期', default=today())
    subsidy_type_id = fields.Many2one('dy.subsidy.type', string=u'补贴类型')
    subsidy_model_id = fields.Many2one('dy.subsidy.model', string=u'补贴模式')
    amount = fields.Float(string=u'金额', digits=dp.get_precision('Account'))
    partner_id = fields.Many2one('res.partner', string=u'补贴对象', required=True,
                                 domain=lambda self: [('company_id', 'in', self.env.user.company_ids.ids)])
    remark = fields.Char(string=u'备注')
