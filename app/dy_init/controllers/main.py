# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFood
# file_name: main 
# author: tangdayi
# data: 2018年01月16日 13时41分
# ===================================================


import logging
import json
from odoo import http
from odoo.http import content_disposition, dispatch_rpc, request, \
                      serialize_exception as _serialize_exception

_logger = logging.getLogger(__name__)


class CommonService(http.Controller):
    @http.route('/web/common/random_culture/<int:num>', type='json', auth="none", csrf=False)
    def random_culture(self, num=1):
        """
        随机企业文化宣传语句json接口，用于长时间加载等待或错误提示页面
        :return:
        """
        lines = request.env['dy.init.culture'].get_random_line(num)
        if not lines:
            lines = [{'id': 0, 'line': u'...加载中...'}]
        return lines


