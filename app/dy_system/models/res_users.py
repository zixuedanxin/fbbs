# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: res_users 
# author: tangdayi
# data: 2018年03月20日 22时12分
# ===================================================


from odoo import api, models, fields, SUPERUSER_ID


class ResUser(models.Model):

    _inherit = "res.users"

    restaurant_ids = fields.Many2many('dy.restaurant', 'ref_user_restaurant', 'user_id',
                                      'restaurant_id', string=u'餐厅门店')
    all_restaurant_ids = fields.One2many('dy.restaurant', compute='_get_all_restaurant_ids',
                                         string=u'餐厅门店')
    department_id = fields.Many2one('dy.department', string=u'所属部门')

    all_company_ids = fields.One2many('res.company', compute='_get_all_company_ids', string=u'公司')

    @api.multi
    @api.depends('company_ids')
    def _get_all_company_ids(self):
        for item in self:
            all_company_ids = []
            for company in item.company_ids:
                sql = '''select id from res_company where parent_id=%s'''
                self.env.cr.execute(sql, (company.id,))
                rs = self.env.cr.dictfetchall()
                all_company_ids = [r['id'] for r in rs]
                all_company_ids.append(company.id)
            item.all_company_ids = all_company_ids

    @api.multi
    @api.depends('restaurant_ids')
    def _get_all_restaurant_ids(self):
        """
        get professional_ids
        :return:
        """
        for item in self:
            restaurant_ids = []
            if not item.professional_ids:
                return
            for restaurant_id in item.restaurant_ids.ids:
                if restaurant_id:
                    restaurant_ids.append(restaurant_id)
            item.all_restaurant_ids = restaurant_ids

    @api.model
    def create(self, vals):
        """
        :param vals:
        :return:
        """

        login = vals.get('login', None)
        if login:
            vals.update({
                'email': '%s@fbb.com' % login
            })
        res = super(ResUser, self).create(vals)
        if res and not res.restaurant_ids:
            company_ids = res.company_ids.ids
            if company_ids:
                restaurant = self.env['dy.restaurant'].sudo().search(
                    [('company_id', 'in', company_ids)])
                if restaurant:
                    res.write({'professional_ids': [[6, 0, restaurant.ids]]})
        return res