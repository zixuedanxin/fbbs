# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFoods
# file_name: main 
# author: tangdayi
# data: 2018年04月02日 22时10分
# ===================================================

import logging
import os
import requests
import json
import time
import random
import string
import datetime
from jinja2 import Environment, FileSystemLoader
from odoo import http, SUPERUSER_ID, exceptions
from odoo.http import content_disposition, dispatch_rpc, request

import sys

from tools.ydt.utils import today

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'templates'))

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

templateLoader = FileSystemLoader(searchpath=path)

env = Environment(loader=templateLoader, autoescape=True)

logger = logging.getLogger(__name__)


class MainController(http.Controller):
    """
    前端数据接口访问
    页面跳转
    数据传递
    数据接口

    """

    @http.route('/fbb/home', type='http', auth='public')
    def home(self, **post):
        """
        注册
        :param post:
        :return:
        """
        data = {}
        template_list = env.get_template("home/home.html")
        html = template_list.render(data=data)
        return html

    @http.route('/fbb/login', type='http', auth='public')
    def login(self, **post):
        """
        页面首页
        :param post:
        :return:
        """
        data = {}
        template_list = env.get_template("home/login.html")
        html = template_list.render(data=data)
        return html

    @http.route('/fbb/register', type='http', auth='public')
    def register(self, **post):
        """
        登录
        :param post:
        :return:
        """
        data = {}
        template_list = env.get_template("home/register.html")
        html = template_list.render(data=data)
        return html

    @http.route('/fbb/sort', type='http', auth='public')
    def sort(self, **post):
        """
        分类
        :param post:
        :return:
        """
        template_list = env.get_template('home/sort.html')
        return template_list.render(data={})

    @http.route('/fbb/index', type='http', auth='public')
    def index(self, **post):
        """
        我的 个人中心
        :param post:
        :return:
        """
        template_list = env.get_template('person/index.html')
        return template_list.render(data={})

    @http.route('/fbb/shopcart', type='http', auth='public')
    def shop_cart(self, **post):
        """
        购物车
        :param post:
        :return:
        """
        template_list = env.get_template('home/shopcart.html')
        return template_list.render(data={})

    @http.route('/fbb/pay', type='http', auth='public')
    def payment(self, **post):
        """
        结算
        :param post:
        :return:
        """
        template_list = env.get_template("home/pay.html")
        data = {}
        html = template_list.render(data=data)
        return html

    @http.route('/fbb/success', type='http', auth='public')
    def success(self, **post):
        """
        购买成功页面
        :param post:
        :return:
        """
        template_list = env.get_template("home/success.html")
        data = {}
        html = template_list.render(data=data)
        return html

    @http.route('/ws/eas/fin/dynamic/settle/init', type='http', auth='public', csrf=False)
    def eas_settle_dynamic_data(self, **post):
        """
        后台数据处理，接收前端请求，返回数据
        :param post:
        :return:
        """
        data_type = post.get('type', None)
        day = str(today())
        params = [
            {'value': data_type, 'type': 'String'},
            {'value': day, 'type': 'String'},
            {'value': day, 'type': 'String'}
        ]
        data = self.requestManyEASData('getMonthData', params)
        if not data:
            data = [{}]  # 返回空的数据
            print "请求出错，没有请求到eas 动态代扣数据 eas_settle_dynamic_data"
        settleAmt = 0.0
        settleQty = 0
        for item in data:
            settleQty = item.get('payqty', 0)
            settleAmt = round(item.get('payamt', 0.00), 2)
        value = {
            'settleAmt': settleAmt,
            'settleQty': settleQty
        }
        new_data = {"data": value, "code": 200, "type": data_type}  # 包装新的数据格式
        # 经数据字典转化为 json 格式
        data = json.dumps(new_data)
        print new_data
        return http.Response(data, 200)

