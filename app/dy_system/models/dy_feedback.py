# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: dy_feedback 
# author: tangdayi
# data: 2018年03月22日 20时36分
# ===================================================

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class DyFeedBack(models.Model):
    """
    用户反馈
    """

    _name = 'dy.feedback'

    _description = u'用户反馈'

    _order = 'id desc'

    number = fields.Char(string=u'编号', readnoly=True,
                         default=lambda self: self.env['ir.sequence'].next_by_code(self._name))
    user_id = fields.Many2one('res.users', string=u'反馈用户',
                              default=lambda self: self.env.uid)
    restaurant_id = fields.Many2one('dy.restaurant', string=u'供应商')
    content = fields.Text(string=u'建议内容')
    date = fields.Date(string=u'日期')
    score = fields.Float(string=u'评分', compute='get_score', store=True, digits=dp.get_precision('Account'))
    food_time = fields.Selection([('breakfast', u'早'), ('lunch', u'午'), ('dinner', u'晚')], string=u'用餐阶段')
    health_score = fields.Many2one('dy.score', string=u'卫生')
    taste_score = fields.Many2one('dy.score', string=u'味道')
    weight_score = fields.Many2one('dy.score', string=u'份量')
    remark = fields.Char(string=u'备注')

    @api.multi
    @api.depends('health_score', 'taste_score', 'weight_score')
    def _get_score(self):
        """
        获取评分
        :return:
        """
        for obj in self:
            total = 0.0
            if obj.health_score:
                total = total + obj.health_score.values
            if obj.taste_score:
                total = total + obj.taste_score.values
            if obj.weight_score:
                total = total + obj.taste_score.values
            total = total/3.0
            obj.update({
                'score': total
            })
