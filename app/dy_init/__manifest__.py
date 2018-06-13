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
    'name': 'FBB DYINIT',
    'summary': '初始化模块',
    'version': '1.0',
    'category': 'FBBAPPLICATION',
    'sequence': 1,
    'author': 'YiDaTang',
    'website': 'http://www.fbb.com',
    'images': [],
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        "views/lang_data.xml",
        "views/base_view.xml",
        # "views/mail_data.xml",
        "views/templates.xml",
        "views/main_company.xml",
        "views/view_culture.xml",
        "views/view_culture_category.xml",
        "views/culture_data.xml",
        "views/menus.xml",
    ],
    'qweb': [
        "static/src/xml/base.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': u"""
        初始化安装模块
        1、安装系统MAIL消息基础模块
        2、设置主体公司基本信息
        3、设置应用系统名字
        4、设置中文语言和日期格式
        5、设置Logo和版权信息
        注意：修改views/templates.xml中的【应用系统名字】，main_company.xml中的公司主体信息
    """,
}
