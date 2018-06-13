# -*- coding: utf-8 -*-
# 项目: wens-o2o-agent
# 文件: outer
# 模块:
# Copyright 2017 WENS <www.wens.com.cn>
# Created by HHL at 2017/6/9 下午11:12 with PyCharm
import werkzeug
import simplejson

from odoo import http
from odoo.api import call_kw
from odoo.http import request
from odoo.models import MetaModel
from odoo import fields

class OuterRequestController(http.Controller):

    @http.route('/outer/web/demo')
    def out_demo(self, **kwargs):
        a = request.eas_cr
        b = request.io_cr
        return 'ok'

    @http.route('/outer/web/dataset/search_read', type='http', auth="public", ip_name='trust_ips')
    def outer_search_read(self, model, fields=False, offset=0, limit=False, domain=None, sort=None):
        return self.outer_do_search_read(model, fields, offset, limit, domain, sort)

    def outer_do_search_read(self, model, fields=False, offset=0, limit=False, domain=None
                             , sort=None):
        """ Performs a search() followed by a read() (if needed) using the
        provided search criteria

        :param str model: the name of the model to search on
        :param fields: a list of the fields to return in the result records
        :type fields: [str]
        :param int offset: from which index should the results start being returned
        :param int limit: the maximum number of records to return
        :param list domain: the search domain for the query
        :param list sort: sorting directives
        :returns: A structure (dict) with two keys: ids (all the ids matching
                  the (domain, context) pair) and records (paginated records
                  matching fields selection set)
        :rtype: list
        """
        Model = request.env[model].sudo()

        records = Model.search_read(domain, fields,
                                    offset=offset or 0, limit=limit or False, order=sort or False)
        if not records:
            return {
                'length': 0,
                'records': []
            }
        if limit and len(records) == limit:
            length = Model.search_count(domain)
        else:
            length = len(records) + (offset or 0)
        return {
            'length': length,
            'records': records
        }

    @http.route('/outer/web/dataset/load', type='http', auth="public", ip_name='trust_ips')
    def outer_load(self, model, id, fields):
        value = {}
        r = request.env[model].sudo().browse([id]).read()
        if r:
            value = r[0]
        return {'value': value}

    def outer_call_common(self, model, method, args, domain_id=None, context_id=None):
        return self._outer_call_kw(model, method, args, {})

    def _outer_call_kw(self, model, method, args, kwargs):
        # if not kwargs:
        #     kwargs = {}

        sudo_model = request.env[model].sudo()
        # if self._is_outer_db(sudo_model):
        #     outer_cr = request.env.cr
        #     sudo_model = sudo_model.with_context({'outer_cr': outer_cr})
        #     kwargs.update({'outer_cr': outer_cr})
        return call_kw(sudo_model, method, args, kwargs)

    @http.route('/outer/web/dataset/call', type='http', auth="public", ip_name='trust_ips')
    def outer_call(self, model, method, args, domain_id=None, context_id=None):
        return self._outer_call_kw(model, method, args, {})

    @http.route(['/outer/web/dataset/call_kw', '/outer/web/dataset/call_kw/<path:path>'], type='json', auth="public", ip_name='trust_ips')
    def outer_call_kw(self, model, method, args, kwargs, path=None):
        if method == '_search' or method == 'search':  # json中()被转成了list,这里要变回来
            domain = []
            for item in args[0]:
                if isinstance(item, list):  # domain
                    new_item = tuple(item)
                    domain.append(new_item)
                else:  # '\' 或者 '&'符号
                    domain.append(item)
            args[0] = domain
        result = self._outer_call_kw(model, method, args, kwargs)

        if self._is_odoo_model(result):
            result = self._convert_to_json(result)
        return result

    def _convert_to_json(self, result):
        def _convert_each(each_value):
            val = {}
            for field in each_value._fields.keys():
                field_value = each_value[field]
                if self._is_odoo_model(field_value) and isinstance(each_value._fields[field], fields.Many2one):
                    val.update({field: [each_value[field].id, each_value[field].name_get()]})
                elif isinstance(each_value._fields[field], fields.One2many) or isinstance(each_value._fields[field],
                                                                                          fields.Many2many):
                    pass
                else:
                    val.update({field: each_value[field]})
                val.update({'id': each_value.id})
            return val

        if result:
            list_result = []
            if len(result):
                for each_val in result:
                    val = _convert_each(each_val)
                    list_result.append(val)
            else:
                val = _convert_each(result)
                list_result.append(val)
            return list_result
        else:
            return []

    def _is_odoo_model(self, value):
        if hasattr(value, '__metaclass__'):
            if getattr(value, '__metaclass__') is MetaModel:
                return True
        return False

    @http.route('/outer/web/dataset/call_button', type='http', auth="public", ip_name='trust_ips')
    def outer_call_button(self, model, method, args, domain_id=None, context_id=None):
        action = self._outer_call_kw(model, method, args, {})
        if isinstance(action, dict) and action.get('type') != '':
            return clean_action(action)
        return False

    @http.route('/outer/web/dataset/exec_workflow', type='http', auth="public", ip_name='trust_ips')
    def outer_exec_workflow(self, model, id, signal):
        request.session.check_security()
        return request.env[model].browse(id).signal_workflow(signal)[id]

    @http.route('/outer/web/dataset/resequence', type='http', auth="public", ip_name='trust_ips')
    def outer_resequence(self, model, ids, field='sequence', offset=0):
        """ Re-sequences a number of records in the model, by their ids

        The re-sequencing starts at the first model of ``ids``, the sequence
        number is incremented by one after each record and starts at ``offset``

        :param ids: identifiers of the records to resequence, in the new sequence order
        :type ids: list(id)
        :param str field: field used for sequence specification, defaults to
                          "sequence"
        :param int offset: sequence number for first record in ``ids``, allows
                           starting the resequencing from an arbitrary number,
                           defaults to ``0``
        """
        m = request.env[model]
        if not m.fields_get([field]):
            return False
        # python 2.6 has no start parameter
        for i, record in enumerate(m.browse(ids)):
            record.write({field: i + offset})
        return True

    @http.route('/outer/web/dataset/model_fields', type='http', auth="public", ip_name='trust_ips')
    def outer_get_model_fields(self, model):
        result = []
        for field in request.env[model]._fields.keys():
            field_type = request.env[model]._fields[field]
            if isinstance(field_type, fields.Char):
                result.append({'type': 'char', 'name': field, 'string': field_type.string})
            elif isinstance(field_type, fields.Integer):
                result.append({'type': 'integer', 'name': field, 'string': field_type.string})
            elif isinstance(field_type, fields.Boolean):
                result.append({'type': 'boolean', 'name': field, 'string': field_type.string})
            elif isinstance(field_type, fields.Date):
                result.append({'type': 'date', 'name': field, 'string': field_type.string})
            elif isinstance(field_type, fields.Datetime):
                result.append({'type': 'datetime', 'name': field, 'string': field_type.string})
            elif isinstance(field_type, fields.Float):
                result.append({'type': 'float', 'name': field, 'string': field_type.string})
            elif isinstance(field_type, fields.Text):
                result.append({'type': 'text', 'name': field, 'string': field_type.string})
        return simplejson.dumps(result)

    def _is_outer_db(self, model):
        pass


def login_and_redirect(db, login, key, redirect_url='/web'):
    request.session.authenticate(db, login, key)
    return set_cookie_and_redirect(redirect_url)


def set_cookie_and_redirect(redirect_url):
    redirect = werkzeug.utils.redirect(redirect_url, 303)
    redirect.autocorrect_location_header = False
    return redirect


def load_actions_from_ir_values(action_slot, model, res_id):
    actions = request.env['ir.values'].get_actions(action_slot, model, res_id)
    return [(id, name, clean_action(action)) for id, name, action in actions]


def clean_action(action):
    action.setdefault('flags', {})
    action_type = action.setdefault('type', 'ir.actions.act_window_close')
    if action_type == 'ir.actions.act_window':
        return fix_view_modes(action)
    return action


# I think generate_views,fix_view_modes should go into js ActionManager
def generate_views(action):
    """
    While the server generates a sequence called "views" computing dependencies
    between a bunch of stuff for views coming directly from the database
    (the ``ir.actions.act_window model``), it's also possible for e.g. buttons
    to return custom view dictionaries generated on the fly.

    In that case, there is no ``views`` key available on the action.

    Since the web client relies on ``action['views']``, generate it here from
    ``view_mode`` and ``view_id``.

    Currently handles two different cases:

    * no view_id, multiple view_mode
    * single view_id, single view_mode

    :param dict action: action descriptor dictionary to generate a views key for
    """
    view_id = action.get('view_id') or False
    if isinstance(view_id, (list, tuple)):
        view_id = view_id[0]

    # providing at least one view mode is a requirement, not an option
    view_modes = action['view_mode'].split(',')

    if len(view_modes) > 1:
        if view_id:
            raise ValueError('Non-db action dictionaries should provide '
                             'either multiple view modes or a single view '
                             'mode and an optional view id.\n\n Got view '
                             'modes %r and view id %r for action %r' % (
                                 view_modes, view_id, action))
        action['views'] = [(False, mode) for mode in view_modes]
        return
    action['views'] = [(view_id, view_modes[0])]


def fix_view_modes(action):
    """ For historical reasons, Odoo has weird dealings in relation to
    view_mode and the view_type attribute (on window actions):

    * one of the view modes is ``tree``, which stands for both list views
      and tree views
    * the choice is made by checking ``view_type``, which is either
      ``form`` for a list view or ``tree`` for an actual tree view

    This methods simply folds the view_type into view_mode by adding a
    new view mode ``list`` which is the result of the ``tree`` view_mode
    in conjunction with the ``form`` view_type.

    TODO: this should go into the doc, some kind of "peculiarities" section

    :param dict action: an action descriptor
    :returns: nothing, the action is modified in place
    """
    if not action.get('views'):
        generate_views(action)

    if action.pop('view_type', 'form') != 'form':
        return action

    if 'view_mode' in action:
        action['view_mode'] = ','.join(
            mode if mode != 'tree' else 'list'
            for mode in action['view_mode'].split(','))
    action['views'] = [
        [id, mode if mode != 'tree' else 'list']
        for id, mode in action['views']
        ]

    return action
