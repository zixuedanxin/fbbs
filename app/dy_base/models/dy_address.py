# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: dy_address 
# author: tangdayi
# data: 2018年03月16日 22时32分
# ===================================================

from odoo import fields, models, api


class DyProvince(models.Model):
    """
    基础资料，地址，省份，市，县/区，镇，街道
    """
    _description = u"省"
    _name = 'dy.province'
    _order = 'code'

    @api.model
    def get_main_country(self):
        """
        获取国家
        :return:
        """
        return self.env['ir.model.data'].xmlid_to_object('base.cn')

    name = fields.Char(string=u'名称', required=True, help=u'省名，如：贵州省')
    simple_name = fields.Char(string=u'简称')
    country_id = fields.Many2one('res.country', string=u'国家', default=get_main_country)
    code = fields.Char(string=u'编码', help=u'省代码，P1', required=True, default='PROVINCE1')
    remark = fields.Char(u'备注')

    _sql_constraints = [
        ('name_code_uniq', 'unique(name,code)', u'省名或者代码称唯一，不能重复创建！')
    ]

    @api.model
    def create(self, vals):
        """
        :param vals:
        :return:
        """
        province_ids = self.search([])
        if province_ids:
            vals.update({
                'code': 'PROVINCE%s' % str(len(province_ids) + 1)
            })
        return super(DyProvince, self).create(vals)


class DyCity(models.Model):
    """
    城市
    """
    _description = u"市"
    _name = 'dy.city'
    _order = 'code'

    province_id = fields.Many2one('dy.province', string=u'省', required=True)
    name = fields.Char(string=u'名称', required=True, help=u'城市名，如：贵阳市，云浮市')
    code = fields.Char(string=u'编码', help=u'市编码，C0001', required=True, default='CITY1')
    remark = fields.Char(u'备注')

    _sql_constraints = [
        ('name_code_uniq', 'unique(province_id,name)', u'市名或者代码称唯一，不能重复创建！')
    ]

    @api.model
    def create(self, vals):
        """
        :param vals:
        :return:
        """
        obj_ids = self.search([])
        if obj_ids:
            vals.update({
                'code': 'CITY%s' % str(len(obj_ids) + 1)
            })
        return super(DyCity, self).create(vals)


class DyCounty(models.Model):
    """
    县／区
    """
    _description = u"县／区"
    _name = 'dy.county'
    _order = 'code'

    city_id = fields.Many2one('dy.city', string=u'市', required=True)
    name = fields.Char(string=u'名称', required=True, help=u'名，县／区如：龙岗区，贵定县，新兴县')
    code = fields.Char(string=u'编码', help=u'县编码，COUNTY1', required=True, default='COUNTY1')
    remark = fields.Char(u'备注')

    _sql_constraints = [
        ('name_code_uniq', 'unique(city_id,name)', u'县名或者代码称唯一，不能重复创建！')
    ]

    @api.model
    def create(self, vals):
        """
        :param vals:
        :return:
        """
        obj_ids = self.search([])
        if obj_ids:
            vals.update({
                'code': 'COUNTY%s' % str(len(obj_ids) + 1)
            })
        return super(DyCounty, self).create(vals)


class DyTown(models.Model):
    """
    城镇
    """
    _description = u"镇"
    _name = 'dy.town'
    _order = 'code'

    county_id = fields.Many2one('dy.county', string=u'县/区', required=True)
    name = fields.Char(string=u'名称', required=True, help=u'城市名，如：云雾镇，新城镇')
    code = fields.Char(string=u'编码', help=u'镇编码，TOWN', required=True, default='TOWN1')
    remark = fields.Char(u'备注')

    _sql_constraints = [
        ('name_code_uniq', 'unique(county_id,name)', u'镇名或者代码称唯一，不能重复创建！')
    ]

    @api.model
    def create(self, vals):
        """
        :param vals:
        :return:
        """
        obj_ids = self.search([])
        if obj_ids:
            vals.update({
                'code': 'TOWN%s' % str(len(obj_ids) + 1)
            })
        return super(DyTown, self).create(vals)