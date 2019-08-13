# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date, datetime, timedelta
import pytz

from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import format_date
from odoo.addons import decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    # @api.model
    # def create(self, values):
    #     _logger.debug("\n\n\n CREATE MAIL\n\n\n")
    #     activity = super(MailActivity, self).create(values)
    #     return activity_user
     # continue as sudo because activities are somewhat protected

    @api.model
    def create(self, values):
        # event_vals = {
        #             'vame': 'hola',
        #             'start': values['date_deadline']+' 12:00:00',
        #             'stop': values['date_deadline']+' 13:00:00',
        #         }

        # values['calendar_event_id'] = [(0, 0, event_vals)]
        # if 'date_deadline' in values:
        #     event = self.env['calendar.event'].create(dict(
        #         name= 'hola',
        #         start= values['date_deadline']+' 12:00:00',
        #         stop= values['date_deadline']+' 13:00:00',
        #         description= values['note'],
        #     ))
        # values['calendar_event_id'] = {
        #     'name': 'asdasd' 
        # }
        activity = super(MailActivity, self).create(values)
        _logger.debug("\n\n\n CREATE MAIL\n\n\n")
        #envent_obj = self.env['calendar.event']
        #Se agrega 4 horas mas por ZONA HORARIA chilena
        #activity.calendar_event_id.
        self.env['calendar.event'].create(dict(
            name=(str(activity.activity_type_id.display_name) + ' - ' + str(activity.summary)),
        #     start_datetime=activity.date_deadline+' 12:00:00',
            start=activity.date_deadline+' 12:00:00',
            stop=activity.date_deadline+' 13:00:00',
            description=activity.note,
            user_id=activity.user_id.id,
            res_model_id=356,
            res_model='sale.subscription',
            activity_ids=[(4,activity.id)],
        ))
        #activity.
        return activity

    @api.multi
    def write(self, values):
        _logger.debug("\n\n\n WRITE MAIL\n\n\n")
        res = super(MailActivity, self).write(values)
        return res