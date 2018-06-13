# -*- coding: utf-8 -*-

{
    'name': 'FBB DYMENUS',
    'sequence': 4,
    'author': 'YiDaTang',
    'version': '1.0',
    'depends': ['dy_system', 'dy_food'],
    'category': 'DYBASE',
    'summary': '菜单管理',
    'description': """ 系统菜单分类，所有模块菜单都放于此，通过依赖来产生联系""",
    'data': [
        'system_menus.xml',
        'food_menus.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,

}
