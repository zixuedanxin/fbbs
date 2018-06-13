# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: dy_score 
# author: tangdayi
# data: 2018年03月22日 21时19分
# ===================================================

from odoo import models, fields, api


class DyScore(models.Model):
    """
    评分
    """

    _name = 'dy.score'

    _description = u'用户评价分数'

    _order = 'values'

    name = fields.Char(string=u'名称', help=u'5分，8分')
    values = fields.Integer(string=u'分值', default=5)
    remark = fields.Char(string=u'名称')
