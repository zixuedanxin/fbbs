# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: dy_department 
# author: tangdayi
# data: 2018年03月20日 22时14分
# ===================================================



import logging
from lxml import etree

from odoo import models, fields, api, SUPERUSER_ID
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class DyDepartment(models.Model):

    _name = 'dy.department'
    _description = u'部门'

    number = fields.Char(u'编码', index=True, required=True,
                         default=lambda self: self.env['ir.sequence'].next_by_code(self._name))
    name = fields.Char(u'名称', index=True, required=True)
    leader_id = fields.Many2one('res.users', string=u'部门领导')
    company_id = fields.Many2one('res.company', string=u'公司', index=True, required=True,
                                 default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string=u'有效', default=True)
    remark = fields.Char(string=u'备注')

    _sql_constraints = [
        ('number_unique', 'unique(number)', '部门有重复的编码!'),
    ]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('number', '=ilike', name + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        ids = self.sudo().search(domain + args, limit=limit)
        return ids.name_get()

    @api.multi
    def name_get(self):
        result = []
        for i in self:
            if i.company_id and i.name:
                result.append((i.id, "[%s]%s" % (i.company_id.name, i.name)))
            elif i.name:
                result.append((i.id, "%s" % (i.name,)))
        return result

