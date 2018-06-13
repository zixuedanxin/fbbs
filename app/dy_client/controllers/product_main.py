# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: foods_main 
# author: tangdayi
# data: 2018年04月02日 23时27分
# ===================================================


import logging
import os
import requests
import json
import time
import random
import string
import datetime
import jinja2
from jinja2 import Environment, FileSystemLoader
from odoo import http, SUPERUSER_ID, exceptions
from odoo.http import content_disposition, dispatch_rpc, request

import sys

from tools.ydt.utils import today

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'templates'))

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# path = BASE_DIR + "/templates"
templateLoader = FileSystemLoader(searchpath=path)

# templateLoader = jinja2.PackageLoader('app.dy_client', "templates")

env = Environment(loader=templateLoader, autoescape=True)

logger = logging.getLogger(__name__)


class ProductController(http.Controller):
    """
    前端数据接口访问
    商品详情
    """

    @http.route('/fbb/introduction', type='http', auth='public')
    def introduction(self, **post):
        """
        商品详情
        :param post:
        :return:
        """
        data = {}
        template_list = env.get_template("home/introduction.html")
        html = template_list.render(data=data)
        return html

    @http.route('/fbb/product/list', type='http', auth='public', csrf=False)
    def get_product_list(self, **post):
        """
        获取产品列表
        数据格式：
        :param post: {"data_type": "data_type","a":232}
        :return: 返回值：JSON数据
        """
        # 数据类型
        return self.get_product_info(post)

    @staticmethod
    def get_product_info(data_type):
        """
        获取产品信息
        :return:
        """
        data = {}
        value = []
        domain = []
        company_id = data_type.get('company_id', None)
        product_id = data_type.get('product_id', None)
        product_model = request.env['product.template']
        if company_id:
            domain.append(('company_id', '=', company_id))
        if product_id:
            domain.append(('product_id', '=', product_id))
        products = product_model.search(domain)
        if products:
            for product in products:
                # 产品数据包
                value.append({
                    'id': product.id,
                    'name': product.name,  # 产品名称
                    'image_medium': product.image_medium,
                    'uom_id': product.uom_id.name,  # 单位名称
                    'default_code': product.default_code,
                    'list_price': product.list_price,
                    'categ_id': product.categ_id.name,
                    'description_sale': product.description_sale
                })
        data.update({'data': value, 'state': 200})
        # 将字典转为JSON对象
        json_data = json.dumps(data)
        return http.Response(json_data, 200)

