# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFood
# file_name: __manifest__ 
# author: tangdayi
# data: 2018年01月16日 13时34分
# ===================================================

{
    'name': 'FBB DYCLIENT',
    'summary': '客户端，用户模块，前端页面显示',
    'version': '1.0',
    'category': 'client',
    'sequence': 2,
    'author': 'YiDaTang',
    'website': 'http://www.fbb.com',
    'images': [],
    'depends': ['dy_base'],
    'data': [
        'views/init_product_category.xml',
        'views/init_product_uom.xml',
        'views/inti_products.xml',

    ],
    'qweb': [

    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'description': u"""
        前端页面初始化安装模块
        1、用户登录注册，访问前端模块
        2、用户数据入口，购物，购物车，个人信息维护
        3、外卖商城维护，商品管理，商家管理，供应商管理
    """,
}
