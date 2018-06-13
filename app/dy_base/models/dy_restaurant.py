# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: dy_store 
# author: tangdayi
# data: 2018年03月16日 22时21分
# ===================================================
import os

from odoo import fields, models, api, tools
from tools.ydt.utils import today


class DyRestaurant(models.Model):
    """
    门店====》餐厅
    """

    _name = 'dy.restaurant'

    _description = u'餐厅门店，类似公司'

    _order = 'id desc'

    @api.model
    def get_main_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def get_main_country(self):
        """
        获取国家
        :return:
        """
        return self.env['ir.model.data'].xmlid_to_object('base.cn')

    @api.multi
    def _default_logo(self):
        """
        默认logo
        :return:
        """
        return open(os.path.join(tools.config['root_path'], '..', '..', 'app', 'dy_init', 'static', 'img', 'logo.png'), 'rb').read().encode('base64')

    sequence = fields.Char(string=u'序号')
    name = fields.Char(string=u'名称', required=True)
    simple_name = fields.Char(string=u'简称')
    number = fields.Char(string=u'编号')
    phone = fields.Char(string=u'电话')
    mobile = fields.Char(string=u'手机')
    store_type_id = fields.Many2one('dy.store.type', string=u'类型')
    active = fields.Boolean(string=u'有效', default=True)
    email = fields.Char(string=u'电子邮箱', default='dy@fbb.com.cn')
    logo = fields.Binary(string=u'LOGO', compute='_default_logo', store=True)

    address = fields.Char(string=u'详细地址', compute='get_address')
    street = fields.Char(string=u'所在街道')
    street2 = fields.Char(string=u'所在街道2')
    country_id = fields.Many2one('res.country', string=u"国家", default=get_main_country)
    province_id = fields.Many2one('dy.province', string=u'所在省', required=True)
    city_id = fields.Many2one('dy.city', string=u'所在市', required=True)
    county_id = fields.Many2one('dy.county', string=u'所在县/区', required=True)
    town_id = fields.Many2one('dy.town', string=u'所在镇', required=True)
    website = fields.Char(string=u'网站', default='www.fbb.com')

    legal_person_id = fields.Many2one('res.users', string=u'法人代表')
    company_id = fields.Many2one('res.company', string=u'公司')
    parent_id = fields.Many2one('res.company', string=u'上级公司', default=get_main_company_id)
    start_date = fields.Date(string=u'开业日期', default=today())

    report_header = fields.Text(string=u'餐厅标语')
    remark = fields.Text(string=u'备注')

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
                'website': 'https://www.fbb.com' if not values.get('website', None) else values.get('website', None),
                'parent_id': values.get('parent_id', None),
            })
        res = super(DyRestaurant, self).create(values)
        if res:
            vale.update({'street': res.address})
            company_id = company.sudo().create(vale)
            if company_id:
                res.write({'company_id': company_id.id})
        return res

    def check_company_is_have(self, name):
        """
        检查公司名称是否重复
        :return:
        """
        company = self.env['res.company'].search([('name', '=', name)])
        if company:
            return True
        else:
            return False

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

    @api.multi
    def write(self, values):
        """
        数据更新
        :param values:
        :return:
        """
        if values:
            self.env['res.company'].sudo().write(values)
        return super(DyRestaurant, self).write(values)