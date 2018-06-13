# -*- coding: utf-8 -*-

{
    'name': 'FBB DYBASE',
    'sequence': 2,
    'author': 'YiDaTang',
    'version': '1.0',
    'depends': ['base', 'web', 'decimal_precision', 'sale'],
    'category': 'DYBASE',
    'summary': '基础数据管理',
    'description': """ 基础数据管理初始化 """,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'sequences.xml',
        'views/store_type_view.xml',
        'views/restaurant_view.xml',
        'views/address_view.xml',
        'views/department_view.xml',
        'views/company_view.xml',
        'views/score_view.xml',
        'statics/init_dy_province_data.xml',
        'views/menus.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,

}
