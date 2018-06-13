# -*- encoding: utf-8 -*-
# ===================================================
# phone: 10086
# email: tangdayi520@126.com
# projectname: FBBFood
# file_name: mail.py
# author: tangdayi
# data: 2018年01月14日 23时29分
# ===================================================


from odoo import api, models
from odoo.tools import config
import logging
_logger = logging.getLogger(__name__)


config['publisher_warranty_url'] = ''

#不收集系统信息
class PublisherWarrantyContract(models.AbstractModel):
    _inherit = "publisher_warranty.contract"
    _description = "Languages"

    @api.model
    def _get_message(self):
        msg = "NO WARRANTY"
        _logger.debug("NO WARRANTY")
        return msg


    @api.model
    def _get_sys_logs(self):
        """
        Utility method to send a publisher warranty get logs messages.
        """
        pass

    @api.multi
    def update_notification(self, cron_mode=True):
        """
        Send a message to OpenERP's publisher warranty server to check the
        validity of the contracts, get notifications, etc...

        @param cron_mode: If true, catch all exceptions (appropriate for usage in a cron).
        @type cron_mode: boolean
        """
        _logger.debug("NO WARRANTY")
        return True