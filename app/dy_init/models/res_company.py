# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086
# email: tangdayi520@126.com
# projectname: FBBFood
# file_name: res_company.py
# author: tangdayi
# data: 2018年01月14日 23时29分
# ===================================================

import os
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _get_logo(self):
        return open(os.path.join(tools.config['root_path'], '..', '..', 'app', 'dy_init', 'static', 'img', 'logo.png'), 'rb') .read().encode('base64')

    @api.model
    def create(self, vals):
        """
        创建公司默认logo
        :param vals:
        :return:
        """
        vals.update({
            'logo': self._get_logo()
        })
        return super(ResCompany, self).create(vals)