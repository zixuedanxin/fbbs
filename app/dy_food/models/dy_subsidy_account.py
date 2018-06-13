# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: dy_employees_account 
# author: tangdayi
# data: 2018年03月21日 13时17分
# ===================================================

from odoo import fields, api, models
from odoo.addons import decimal_precision as dp


class DySubsidyAccount(models.Model):
    """
    补贴账户设置
    补贴设置，与员工绑定在一起
    """

    _name = 'dy.subsidy.account'

    _description = u'补贴账户设置'

    _order = 'id desc'

    number = fields.Char(string=u'编号', default=lambda self: self.env['ir.sequence'].next_by_code(self._name))
    subsidy_id = fields.Many2one('dy.subsidy.order', string=u'补贴单')
    subsidy_amount = fields.Float(related='subsidy_id.amount', string=u'补贴金额', digits=dp.get_precision('Account'), store=True)
    user_id = fields.Many2one('res.users', string=u'补贴员工', required=True)
    partner_id = fields.Many2one(related='user_id.partner_id', string=u'补贴对象', required=True,
                                 domain=lambda self: [('company_id', 'in', self.env.user.company_ids.ids)])
    mobile = fields.Char(related='user_id.mobile', string=u'手机号', store=True)
    email = fields.Char(related='user_id.email', string=u'邮箱', store=True)
    department_id = fields.Many2one('dy.department', string=u'部门')
    company_id = fields.Many2one(related='user_id.company_id', string=u'单位')
    remark = fields.Char(string=u'备注')

    @api.multi
    @api.onchange('user_id')
    def onchange_partner_id(self):
        """
        关联用户
        :return:
        """
        for obj in self:
            if obj.partner_id:
                user = self.env['res.users'].search([('partner_id', '=', obj.partner_id.id)])
                if user:
                    obj.update({
                        'department_id': user.department_id.id,
                        'company_id': user.company_id.id
                    })

    @api.multi
    @api.depends('user_id')
    def department_user(self):
        """
        :return:
        """
        pass
