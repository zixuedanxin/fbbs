# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: users_main
# author: tangdayi
# data: 2018年04月02日 23时28分
# ===================================================

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import jinja2
import json
import logging
import operator
import os
import re
import sys
from odoo import http

_logger = logging.getLogger(__name__)

if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('client.addons.web', "templates")

env = jinja2.Environment(loader=loader, autoescape=True)
env.filters["json"] = json.dumps


class Database(http.Controller):

    @http.route('/fbb/home1', type='http', auth='public')
    def home1(self, **post):
        """
        页面首页
        :param post:
        :return:
        """
        # template_list = env.get_template("test.html")
        # data = {}
        # html = template_list.render(data=data)
        # return html

        data = {}
        template_list = env.get_template("test1.html")
        html = template_list.render(data=data)
        return html