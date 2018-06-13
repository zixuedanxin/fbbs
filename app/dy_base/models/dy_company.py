# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: res_company 
# author: tangdayi
# data: 2018年03月16日 23时04分
# ===================================================
import os

from odoo import fields, models, api, tools


class DyCompany(models.Model):
    """
    继承公司
    """
    _name = 'dy.company'

    _description = u'公司创建入口'

    @api.multi
    def _default_logo(self):
        """
        默认logo
        :return:
        """
        return open(os.path.join(tools.config['root_path'], '..', '..', 'app', 'dy_init', 'static', 'img', 'logo.png'),
                    'rb').read().encode('base64')

    @api.model
    def get_main_country(self):
        """
        获取国家
        :return:
        """
        return self.env['ir.model.data'].xmlid_to_object('base.cn')

    number = fields.Char(string=u'编号')
    name = fields.Char(string=u'名称', required=True)
    simple_name = fields.Char(string=u'简称')
    sequence = fields.Integer(default=10)
    parent_id = fields.Many2one('res.company', string=u'上级公司')
    logo = fields.Binary(default=_default_logo, string=u"公司LOG")
    account_no = fields.Char(string=u'科目号')
    address = fields.Char(string=u'详细地址', compute='get_address', store=True)
    street = fields.Char(string=u'所在街道')
    street2 = fields.Char(string=u'所在街道2')
    country_id = fields.Many2one('res.country', string=u"国家", default=get_main_country)
    province_id = fields.Many2one('dy.province', string=u'所在省', required=True)
    city_id = fields.Many2one('dy.city', string=u'所在市', required=True)
    county_id = fields.Many2one('dy.county', string=u'所在县/区', required=True)
    town_id = fields.Many2one('dy.town', string=u'所在镇', required=True)
    active = fields.Boolean(string=u'有效', default=True)
    email = fields.Char(string=u'电子邮箱', default='dy@fbb.com.cn')
    phone = fields.Char(string=u'电话', default='08548889966')
    website = fields.Char(string=u'网站', default='www.fbb.com')
    company_registry = fields.Char(string=u'公司注册')
    report_header = fields.Text(string=u'公司标语')
    vat = fields.Char(string=u"税务登记证号码")

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', "名称已经存在，请重新创建一个，谢谢🙏！"),
    ]

    @api.model
    def create(self, values):
        """
        :param values:
        :return:
        """
        company = self.env['res.company']
        vale = {}
        name = values.get('name', None)
        if values and name:
            vale.update({
                'name': name,
                'simple_name': values.get('simple_name', None),
                'street': values.get('address', None),
                'email': values.get('email', None),
                'phone': values.get('phone', None),
                'country_id': values.get('country_id', None),
                'website': values.get('website', None),
                'parent_id': values.get('parent_id', None),
                'company_registry': values.get('company_registry', None),
                'vat': values.get('vat', None),
                'report_header': values.get('report_header', None),
                'logo': values.get('logo', None),
            })
        res = super(DyCompany, self).create(values)
        if res:
            vale.update({'street': res.address})
            company_id = company.sudo().create(vale)
            if company_id:
                res.write({'company_id': company_id.id})
        return res

    @api.multi
    def write(self, values):
        """
        数据更新
        :param values:
        :return:
        """
        if values:
            self.env['res.company'].sudo().write(values)
        return super(DyCompany, self).write(values)

    @api.multi
    @api.depends('province_id', 'city_id', 'county_id', 'town_id', 'street', 'street2')
    def get_address(self):
        """
        获取地址
        :return:
        """
        address = ''
        for obj in self:
            if obj and obj.province_id:
                address = '%s%s' % (address, obj.province_id.name)
            if obj.city_id:
                address = '%s%s' % (address, obj.city_id.name)
            if obj.county_id:
                address = '%s%s' % (address, obj.county_id.name)
            if obj.town_id:
                address = '%s%s' % (address, obj.town_id.name)
            if obj.street and obj.street2:
                address = '%s%s%s' % (address, obj.street, obj.street2)
            obj.update({
                'address': address
            })