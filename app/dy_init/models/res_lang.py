# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086
# email: tangdayi520@126.com
# projectname: FBBFood
# file_name: res_lang.py
# author: tangdayi
# data: 2018年01月13日 23时29分
# ===================================================

from odoo import models,fields,api


class lang(models.Model):
    _inherit = "res.lang"
    _description = "Languages"

    @api.model
    def install_lang_zh(self):
        lang_ids = self.search([('code', '=', 'zh_CN')])
        if not lang_ids:
            self.load_lang('zh_CN')

        return self.install_lang()

    @api.model
    def install_lang_tw(self):
        lang_ids = self.search([('code', '=', 'zh_TW')])
        if not lang_ids:
            self.load_lang('zh_TW')

        return self.install_lang()

    @api.model
    def set_format(self):
        self.search([('code', '=', 'zh_CN')]).write({
            'date_format': '%Y-%m-%d',
            'time_format': '%H:%M:%S',
        })

    @api.model
    def translate_hard(self):
        self.env['ir.translation'].search([('src', '=', 'Whole Company')]).write({
                'value': '所有公司',
                'state': 'translated',
            })