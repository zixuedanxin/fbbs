# -*- coding: utf-8 -*-

{
    'name': 'FBB DYSYSTEM',
    'sequence': 3,
    'author': 'YiDaTang',
    'version': '1.0',
    'depends': ['dy_base'],
    'category': 'DYBASE',
    'summary': '系统管理',
    'description': """ 数据管理，用户管理，菜单管理，餐厅管理，公司管理，权限管理 """,
    'data': [
        'sequences.xml',
        'security/ir.model.access.csv',
        'views/res_users_view.xml',
        'views/simple_users_view.xml',
        'views/feedback_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,

}
