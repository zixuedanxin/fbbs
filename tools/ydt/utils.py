# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086 
# email: tangdayi520@126.com
# projectname: FBBFood
# file_name: utils 
# author: tangdayi
# data: 2018年01月16日 13时27分
# ===================================================



import hashlib

import odoo
from odoo.tools import config


def today(timezone='Asia/Shanghai', str_format=None, **kwargs):
    '''
    :param timezone:
    :param str_format:
    :param kwargs: delay_days
    :return:
    '''
    import datetime
    import pytz

    day_delay = kwargs.get('delay_days', 0)
    tz = pytz.timezone(timezone)
    current = datetime.datetime.now(tz)
    if day_delay != 0:
        current = current + datetime.timedelta(days=day_delay)
    if not str_format:
        str_format = odoo.tools.DEFAULT_SERVER_DATE_FORMAT
    current_date = current.strftime(str_format)
    return current_date


def current_time(timezone='Asia/Shanghai', str_format=None):
    import datetime
    import pytz

    tz = pytz.timezone(timezone)
    current = datetime.datetime.now(tz)
    if not str_format:
        str_format = odoo.tools.DEFAULT_SERVER_TIME_FORMAT
    current_time_str = current.strftime(str_format)
    return current_time_str


def encode_md5(encode_str):
    '''
    生成字符串的md5
    :param encode_str:
    :return:
    '''
    if not encode_str:
        return encode_str
    m = hashlib.md5()
    m.update(encode_str)
    return m.hexdigest()


def is_prod():
    '''
    是否是生产环境
    :return:
    '''
    return config.get('environment', 'dev') == 'prod'