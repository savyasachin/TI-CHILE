# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import datetime
import time
import traceback

from collections import Counter
from dateutil.relativedelta import relativedelta
from uuid import uuid4

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import format_date

from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    @api.onchange('recurring_next_date')
    def onchange_recurring_next_date(self):
        self.date = self.recurring_next_date

    @api.model
    def create(self, vals):
        if not vals.get('date') and vals.get('recurring_next_date'):
            vals['date'] = vals.get('recurring_next_date')
        res = super(SaleSubscription, self).create(vals)
        return res
    
    def write(self, vals):
        if 'date' in vals and not vals.get('date'):
            vals['date'] = self.recurring_next_date
        res = super(SaleSubscription, self).write(vals)
        return res