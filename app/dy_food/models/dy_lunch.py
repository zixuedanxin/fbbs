# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import OrderedDict

import json
import datetime

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, ValidationError
from odoo.addons import decimal_precision as dp


class LunchOrder(models.Model):
    """
    A lunch order contains one or more lunch order line(s). It is associated to a user for a given
    date. When creating a lunch order, applicable lunch alerts are displayed.
    """
    _name = 'lunch.order'
    _description = u'用餐订单'
    _order = 'date desc'

    def _default_previous_order_ids(self):
        prev_order = self.env['lunch.order.line'].search([('user_id', '=', self.env.uid), ('product_id.active', '!=', False)], limit=20, order='id desc')
        # If we return return prev_order.ids, we will have duplicates (identical orders).
        # Therefore, this following part removes duplicates based on product_id and note.
        return list({
            (order.product_id, order.note): order.id
            for order in prev_order
        }.values())

    user_id = fields.Many2one('res.users', u'用户', readonly=True,
                              states={'new': [('readonly', False)]},
                              default=lambda self: self.env.uid)
    date = fields.Date(u'日期', required=True, readonly=True,
                       states={'new': [('readonly', False)]},
                       default=fields.Date.context_today)
    order_line_ids = fields.One2many('lunch.order.line', 'order_id', u'食物',
                                     readonly=True, copy=True,
                                     states={'new': [('readonly', False)], False: [('readonly', False)]})
    total = fields.Float(compute='_compute_total', string="Total", store=True)
    state = fields.Selection([('new', u'新建'),
                              ('confirmed', u'确认'),
                              ('cancelled', u'取消')],
                             u'状态', readonly=True, index=True, copy=False,
                             compute='_compute_order_state', store=True)
    alerts = fields.Text(compute='_compute_alerts_get', string=u"提示")
    company_id = fields.Many2one('res.company', related='user_id.company_id', store=True, string=u'公司')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id',
                                  readonly=True, store=True, string=u'币别')
    cash_move_balance = fields.Monetary(compute='_compute_cash_move_balance', multi='cash_move_balance')
    balance_visible = fields.Boolean(compute='_compute_cash_move_balance', multi='cash_move_balance')
    previous_order_ids = fields.Many2many('lunch.order.line', compute='_compute_previous_order')
    previous_order_widget = fields.Text(compute='_compute_previous_order')

    @api.one
    @api.depends('order_line_ids')
    def _compute_total(self):
        """
        get and sum the order lines' price
        """
        self.total = sum(
            orderline.price for orderline in self.order_line_ids)

    @api.multi
    def name_get(self):
        return [(order.id, '%s %s' % (_('Lunch Order'), '#%d' % order.id)) for order in self]

    @api.depends('state')
    def _compute_alerts_get(self):
        """
        get the alerts to display on the order form
        """
        alert_msg = [alert.message
                     for alert in self.env['lunch.alert'].search([])
                     if alert.display]

        if self.state == 'new':
            self.alerts = alert_msg and '\n'.join(alert_msg) or False

    @api.multi
    @api.depends('user_id', 'state')
    def _compute_previous_order(self):
        self.ensure_one()
        self.previous_order_widget = json.dumps(False)

        prev_order = self.env['lunch.order.line'].search([('user_id', '=', self.env.uid), ('product_id.active', '!=', False)], limit=20, order='date desc, id desc')
        # If we use prev_order.ids, we will have duplicates (identical orders).
        # Therefore, this following part removes duplicates based on product_id and note.
        self.previous_order_ids = list({
            (order.product_id, order.note): order.id
            for order in prev_order
        }.values())

        if self.previous_order_ids:
            lunch_data = {}
            for line in self.previous_order_ids:
                lunch_data[line.id] = {
                    'line_id': line.id,
                    'product_id': line.product_id.id,
                    'product_name': line.product_id.name,
                    'supplier': line.supplier.name,
                    'note': line.note,
                    'price': line.price,
                    'date': line.date,
                    'currency_id': line.currency_id.id,
                }
            # sort the old lunch orders by (date, id)
            lunch_data = OrderedDict(sorted(lunch_data.items(), key=lambda t: (t[1]['date'], t[0]), reverse=True))
            self.previous_order_widget = json.dumps(lunch_data)

    @api.one
    @api.depends('user_id')
    def _compute_cash_move_balance(self):
        domain = [('user_id', '=', self.user_id.id)]
        lunch_cash = self.env['lunch.cashmove'].read_group(domain, ['amount', 'user_id'], ['user_id'])
        if len(lunch_cash):
            self.cash_move_balance = lunch_cash[0]['amount']
        self.balance_visible = (self.user_id == self.env.user) or self.user_has_groups('lunch.group_lunch_manager')

    @api.one
    @api.constrains('date')
    def _check_date(self):
        """
        Prevents the user to create an order in the past
        """
        date_order = datetime.datetime.strptime(self.date, '%Y-%m-%d')
        date_today = datetime.datetime.strptime(fields.Date.context_today(self), '%Y-%m-%d')
        if (date_order < date_today):
            raise ValidationError(_('The date of your order is in the past.'))

    @api.one
    @api.depends('order_line_ids.state')
    def _compute_order_state(self):
        """
        Update the state of lunch.order based on its orderlines. Here is the logic:
        - if at least one order line is cancelled, the order is set as cancelled
        - if no line is cancelled but at least one line is not confirmed, the order is set as new
        - if all lines are confirmed, the order is set as confirmed
        """
        if not self.order_line_ids:
            self.state = 'new'
        else:
            isConfirmed = True
            for orderline in self.order_line_ids:
                if orderline.state == 'cancelled':
                    self.state = 'cancelled'
                    return
                elif orderline.state == 'confirmed':
                    continue
                else:
                    isConfirmed = False

            if isConfirmed:
                self.state = 'confirmed'
            else:
                self.state = 'new'
        return


class LunchOrderLine(models.Model):
    _name = 'lunch.order.line'
    _description = 'lunch order line'
    _order = 'date desc, id desc'

    name = fields.Char(related='product_id.name', string=u"名称", readonly=True)
    order_id = fields.Many2one('lunch.order', u'订单', ondelete='cascade', required=True)
    product_id = fields.Many2one('lunch.product', u'食物', required=True)
    category_id = fields.Many2one('lunch.product.category', string=u'食物分类',
                                  related='product_id.category_id', readonly=True, store=True)
    date = fields.Date(string=u'日期', related='order_id.date', readonly=True, store=True)
    supplier = fields.Many2one('res.partner', string=u'供应商', related='product_id.supplier',
                               readonly=True, store=True)
    user_id = fields.Many2one('res.users', string=u'用户', related='order_id.user_id',
                              readonly=True, store=True)
    note = fields.Text(u'备注')
    price = fields.Float(related='product_id.price', readonly=True, store=True,
                         digits=dp.get_precision('Account'), string=u'价格')
    state = fields.Selection([('new', u'新建'),
                              ('confirmed', u'确定'),
                              ('ordered', u'已订购'),
                              ('cancelled', u'取消')],
                             u'状态', readonly=True, index=True, default='new')
    cashmove = fields.One2many('lunch.cashmove', 'order_id', u'现金转移')
    currency_id = fields.Many2one('res.currency', related='order_id.currency_id')

    @api.one
    def order(self):
        """
        The order_line is ordered to the vendor but isn't received yet
        """
        if self.user_has_groups("lunch.group_lunch_manager"):
            self.state = 'ordered'
        else:
            raise AccessError(_(u"警告⚠️！只有用餐管理员可以取消订单，谢谢！"))

    @api.one
    def confirm(self):
        """
        confirm one or more order line, update order status and create new cashmove
        """
        if self.user_has_groups("lunch.group_lunch_manager"):
            if self.state != 'confirmed':
                values = {
                    'user_id': self.user_id.id,
                    'amount': -self.price,
                    'description': self.product_id.name,
                    'order_id': self.id,
                    'state': 'order',
                    'date': self.date,
                }
                self.env['lunch.cashmove'].create(values)
                self.state = 'confirmed'
        else:
            raise AccessError(_(u"只有用餐管理员才可以把订单设置为已接收。"))

    @api.one
    def cancel(self):
        """
        cancel one or more order.line, update order status and unlink existing cashmoves
        """
        if self.user_has_groups("lunch.group_lunch_manager"):
            self.state = 'cancelled'
            self.cashmove.unlink()
        else:
            raise AccessError(_(u"警告⚠️！只有用餐管理员可以取消订单，谢谢！"))


class LunchProduct(models.Model):
    """ Products available to order. A product is linked to a specific vendor. """
    _name = 'lunch.product'
    _description = 'lunch product'

    name = fields.Char(u'名称', required=True)
    category_id = fields.Many2one('lunch.product.category', u'分类', required=True)
    description = fields.Text(u'描述')
    price = fields.Float(u'价格', digits=dp.get_precision('Account'))
    supplier = fields.Many2one('res.partner', u'供应商')
    active = fields.Boolean(default=True)


class LunchProductCategory(models.Model):
    """ Category of the product such as pizza, sandwich, pasta, chinese, burger... """
    _name = 'lunch.product.category'
    _description = 'lunch product category'

    name = fields.Char(u'分类', required=True)
    remark = fields.Char(u'备注')


class LunchCashMove(models.Model):
    """ Two types of cashmoves: payment (credit) or order (debit) """
    _name = 'lunch.cashmove'
    _description = u'现金转移'

    user_id = fields.Many2one('res.users', u'用户',
                              default=lambda self: self.env.uid)
    date = fields.Date(u'日期', required=True, default=fields.Date.context_today)
    amount = fields.Float(u'金额', required=True, help='能主动(支付)或被动(订单或者支付如果用户想要拿回他的钱)')
    description = fields.Text(u'描述', help='可以是一个订单或支付')
    order_id = fields.Many2one('lunch.order.line', u'订单', ondelete='cascade')
    state = fields.Selection([('order', u'订单'), ('payment', u'付款')],
                             u'一个订单或是一个付款', default='payment')

    @api.multi
    def name_get(self):
        return [(cashmove.id, '%s %s' % (_(u'现金转移'), '#%d' % cashmove.id)) for cashmove in self]


class LunchAlert(models.Model):
    """ Alerts to display during a lunch order. An alert can be specific to a
    given day, weekly or daily. The alert is displayed from start to end hour. """
    _name = 'lunch.alert'
    _description = u'提示'

    display = fields.Boolean(compute='_compute_display_get')
    message = fields.Text(u'消息', required=True)
    alert_type = fields.Selection([('specific', u'指定日'),
                                   ('week', u'每周'),
                                   ('days', u'每天')],
                                  string=u'重新提起', required=True, index=True, default='specific')
    specific_day = fields.Date(u'天', default=fields.Date.context_today)
    monday = fields.Boolean(u'周一')
    tuesday = fields.Boolean(u'周二')
    wednesday = fields.Boolean(u'周三')
    thursday = fields.Boolean(u'周岁')
    friday = fields.Boolean(u'周五')
    saturday = fields.Boolean(u'周六')
    sunday = fields.Boolean(u'周日')
    start_hour = fields.Float(u'介于', oldname='active_from', required=True, default=7)
    end_hour = fields.Float(u'并且', oldname='active_to', required=True, default=23)
    active = fields.Boolean(default=True)

    @api.multi
    def name_get(self):
        return [(alert.id, '%s %s' % (_(u'提示'), '#%d' % alert.id)) for alert in self]

    @api.one
    def _compute_display_get(self):
        """
        This method check if the alert can be displayed today
        if alert type is specific : compare specific_day(date) with today's date
        if alert type is week : check today is set as alert (checkbox true) eg. self['monday']
        if alert type is day : True
        return : Message if can_display_alert is True else False
        """

        days_codes = {'0': 'sunday',
                      '1': 'monday',
                      '2': 'tuesday',
                      '3': 'wednesday',
                      '4': 'thursday',
                      '5': 'friday',
                      '6': 'saturday'}
        can_display_alert = {
            'specific': (self.specific_day == fields.Date.context_today(self)),
            'week': self[days_codes[datetime.datetime.now().strftime('%w')]],
            'days': True
        }

        if can_display_alert[self.alert_type]:
            mynow = fields.Datetime.context_timestamp(self, datetime.datetime.now())
            hour_to = int(self.end_hour)
            min_to = int((self.end_hour - hour_to) * 60)
            to_alert = datetime.time(hour_to, min_to)
            hour_from = int(self.start_hour)
            min_from = int((self.start_hour - hour_from) * 60)
            from_alert = datetime.time(hour_from, min_from)

            if from_alert <= mynow.time() <= to_alert:
                self.display = True
            else:
                self.display = False
