# -*- coding: utf-8 -*-
# 项目: wens-o2o-agent
# 文件: main
# 模块: 
# Copyright 2017 WENS <www.wens.com.cn>
# Created by HHL at 2017/6/9 下午10:52 with PyCharm
import uuid
import logging

import werkzeug
import simplejson

from odoo.addons.web.controllers.main import DataSet
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class DataSetEx(DataSet):
    @http.route('/mapp/auth/get_token', type='http', auth='public', ip_name='token_ips')
    def auth_get_access_token(self, **kwargs):
        '''
        根据用户账户获取访问的token.
        参数: l (账户)
        返回值: {'code':0, 'token': 'xxxx', 'msg': 'ok'}, 成功的话，code为0， 其他值就要看msg的提示。
        '''
        login = kwargs.get('l')
        token = str(uuid.uuid4()).replace("-", "")
        model_obj = http.request.env['user.access.token']
        model_obj.sudo().create({'login': login, 'token': token})
        return simplejson.dumps({'code': 0, 'token': token, 'msg': 'ok'})

    @http.route('/mapp/auth/access', type='http', auth="none")
    def auth_access_redirect(self, **kw):
        '''
        用token进行登录。
        参数：token /mapp/auth/get_token获取到的token， redirect: 登录成功后，重定向到的页面。
        '''
        redirect = kw.get('redirect', '/web')
        token = kw.get('token', None)
        if token:
            token_model = request.env['user.access.token']
            token_obj = token_model.sudo().search([('token', '=', token), ('active', '=', True)])
            if token_obj and token_obj.login:
                login = token_obj.login
                uid = request.session.authenticate(request.session.db, login, 'token-%s' % token)
                if uid is not False:
                    _logger.info('login success')
                    request.params['login_success'] = True
                    token_obj.write({'active': False})
                    return http.redirect_with_hash(redirect)
                else:
                    _logger.info('token login fail, redirect to /web/login')
                    return werkzeug.utils.redirect('/web/login', 303)
            else:
                _logger.warning('token object is empty. redirect to /web/login')
                return werkzeug.utils.redirect('/web/login', 303)
        else:
            _logger.warning('token params is empty, redirect to /web/login')
            return werkzeug.utils.redirect('/web/login', 303)

    '''
    把外部数据源的请求，重新定向到对应的数据接口
    '''

    @http.route('/web/dataset/search_read', type='json', auth="user")
    def search_read(self, model, fields=False, offset=0, limit=False, domain=None, sort=None):
        '''
        重新写search read 方法，避免微服务多次读取search_count
        :param model:
        :param fields:
        :param offset:
        :param limit:
        :param domain:
        :param sort:
        :return:
        '''
        return self._do_search_read_ex(model, fields, offset, limit, domain, sort)

    def _do_search_read_ex(self, model, fields=False, offset=0, limit=False, domain=None
                           , sort=None):
        """
        数据源不是数据库时，数据长度直接从search_read里来。
        """
        model_obj = http.request.env[model]
        records = model_obj.with_context({'need_length': True}).search_read(domain, fields, offset or 0, limit or False,
                                                                            sort or False)
        if not records:
            return {
                'length': 0,
                'records': []
            }
        elif isinstance(records, dict):
            length = records['length']
            final_records = records['records']
            return {
                'length': length,
                'records': final_records
            }
        else:
            if limit and len(records) == limit:
                length = model_obj.search_count(domain)
            else:
                length = len(records) + (offset or 0)
            return {
                'length': length,
                'records': records
            }
