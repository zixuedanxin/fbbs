# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: sale_order 
# author: tangdayi
# data: 2018年06月06日 13时25分
# ===================================================

from odoo import api, models, fields


class SaleOrder(models.Model):
    """
    继承 sale order
    """

    _inherit = 'sale.order'

    subsidy_id = fields.Many2one('dy.subsidy.order', string=u'补贴')
