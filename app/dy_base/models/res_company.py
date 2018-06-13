# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: res_company 
# author: tangdayi
# data: 2018年03月20日 20时47分
# ===================================================

from odoo import fields, models


class ResCompany(models.Model):
    """
    公司继承
    """

    _inherit = 'res.company'

    simple_name = fields.Char(string=u'简称')
