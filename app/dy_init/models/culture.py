# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFood
# file_name: culture 
# author: tangdayi
# data: 2018年01月16日 13时37分
# ===================================================

import logging

from odoo import models, fields, api
_logger = logging.getLogger(__name__)


class CultureCategory(models.Model):
    _name = 'dy.init.culture.category'
    _description = u'分类'

    key = fields.Integer(string=u"序号", required=True, help=u'序号')
    name = fields.Char(string=u'名称', required=True, help=u'名称')
    description = fields.Text(string=u'描述', help=u'描述')


class Culture(models.Model):
    _name = 'dy.init.culture'
    _description = u'企业文化'

    category_id = fields.Many2one('dy.init.culture.category', string=u'分类', required=True)
    key = fields.Integer(string=u"序号", required=True, help=u'序号')
    name = fields.Char(string=u'名称', required=True, help=u'名称')
    description = fields.Text(string=u'描述', help=u'描述')

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        context = self._context or {}
        import time
        time.sleep(15)
        return super(Culture, self).search(args, offset, limit, order, count=count)

    @api.multi
    def get_random_line(self, num):
        """
        获取随机记录
        :return: line_str
        """
        cr = self._cr
        cr.execute('''SELECT a.id,
                             '<font color="yellow"><b>'|| c.name || '</b></font>: <font color="white"><b>' || a.name || '</b></font>' AS line
                      FROM dy_init_culture a
                      LEFT JOIN dy_init_culture_category c ON a.category_id=c.id
                      ORDER BY RANDOM() LIMIT %s''', (num,))
        rows = cr.dictfetchall()
        return rows

