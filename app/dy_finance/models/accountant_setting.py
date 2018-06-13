# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: accountant 
# author: tangdayi
# data: 2018年05月23日 18时45分
# ===================================================

from odoo import api, models, fields


class AccountantSetting(models.Model):
    """
    会计，记账
    """

    _name = 'dy.accountant.account.setting'

    _description = '会计科目配置'

    biz_date = fields.Date(string=u'业务日期')
    company_id = fields.Many2one('res.company', string=u'公司', required=True)
    name = fields.Char(string=u'名称')
    remark = fields.Char(string=u'备注')

    @api.multi
    def action_create_account(self):
        """
        创建公司科目表
        :return:
        """
        for obj in self:
            if obj.company_id:
                simple_name = obj.company_id.simple_name
                account_model = self.env['account.account']
                # 获取主公司科目表
                accounts = account_model.search([('company_id', '=', 1)])
                if accounts:
                    for account in accounts:
                        val = {
                            'name': account.name,
                            'currency_id': account.currency_id.id,
                            'code': account.code,
                            'user_type_id': account.user_type_id.id,
                            'internal_type': account.internal_type,
                            'company_id': obj.company_id.id,
                            'deprecated': account.deprecated,
                            'reconcile': account.reconcile
                        }
                        domain = [('name', '=', account.name), ('company_id', '=', obj.company_id.id)]
                        exit_account = account_model.search(domain)
                        if not exit_account:
                            account_model.sudo().create(val)
