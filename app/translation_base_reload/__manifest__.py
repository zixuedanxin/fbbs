# -*- coding: utf-8 -*-
# Copyright 2017 Jarvis (www.odoomod.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'FBB Translation',
    "summary": "翻译",
    "version": "1.0",
    "category": "Localization",
    "website": "http://www.fbb.com/",
    'description': """
使用
1. 激活开发者模式
2. 在菜单/设置/翻译/加载翻译
3. 勾选"重载模块名称"并"加载"

""",
    'author': "TDY",
    'website': 'http://www.fbb.com',
    "depends": [
        'base',
    ],
    "data": [
        'module/wizard/base_language_install_view.xml'
    ],
    'qweb': [
    ],
    'demo': [
    ],
    'css': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
