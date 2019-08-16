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

    #as_start_time = fields.Datetime(default=lambda self: fields.Date.context_today(self) + " 09:00:00", string='Comenzando en')
    as_start_time = fields.Datetime(string='Comenzando en',default=lambda self: fields.Date.context_today(self) + " 12:00:00")
    as_partner_ids = fields.Many2many('res.partner','res_partner_mail_activity_rel', string='Asistentes')
    as_location = fields.Char('Ubicación')
    as_alarm_ids = fields.Many2many('calendar.alarm', 'calendar_alarm_mail_activity_rel', string='Recordatorio', ondelete="restrict", copy=False)
    as_duration = fields.Float('Duración', default=0.50)

    @api.model
    def create(self, values):
        activity = super(MailActivity, self).create(values)
        _logger.debug("\n\n\n CREATE MAIL: %s\n\n\n"%(activity.activity_type_id.display_name))
        #a = [(0,0,{'mail_activity_id':activity.id,'calendar_alarm_id':id.id}) for id in activity.as_alarm_ids]
        event_obj = self.as_create_event(activity)        
        return activity

    @api.multi
    def write(self, values):
        _logger.debug("\n\n\n WRITE MAIL\n\n\n")
        if 'as_start_time' in values:
            values['date_deadline'] = values['as_start_time'][:10]
        #date_deadline
        res = super(MailActivity, self).write(values)
        if self.calendar_event_id:
            res_event = self.as_write_event()
        else:
            event_obj = self.as_create_event(self)
        return res

    def as_create_event(self,activity):
        event_obj = self.env['calendar.event'].sudo().create(dict(
            name=(str(activity.activity_type_id.display_name) + ' - ' + str(activity.summary)),
            start=activity.as_start_time,
            duration=activity.as_duration,
            stop=datetime.strftime((datetime.strptime(activity.as_start_time, "%Y-%m-%d %H:%M:%S")+ timedelta(hours=activity.as_duration)),"%Y-%m-%d %H:%M:%S"),
            description=activity.note,
            user_id=activity.user_id.id,
            res_model_id=activity.res_model_id.id,
            res_model=activity.res_model,
            activity_ids=[(4,activity.id)],
        ))
        if activity.activity_type_id.name == 'Meeting':
            event_obj.location = activity.as_location
            event_obj.alarm_ids = activity.as_alarm_ids
            event_obj.partner_ids = activity.as_partner_ids.ids + [activity.user_id.id] + event_obj.partner_ids.ids
        return event_obj
    
    def as_write_event(self):
        event_obj = self.env['calendar.event'].sudo().search([('id','=',self.id)])
        if event_obj:
            event_obj.name = (str(activity.activity_type_id.display_name) + ' - ' + str(activity.summary))
            event_obj.start = activity.as_start_time
            event_obj.duration = activity.as_duration
            event_obj.stop = datetime.strftime((datetime.strptime(activity.as_start_time, "%Y-%m-%d %H:%M:%S")+ timedelta(hours=activity.as_duration)),"%Y-%m-%d %H:%M:%S")
            event_obj.description = activity.note
            event_obj.location = activity.as_location
            event_obj.alarm_ids = activity.as_alarm_ids
            event_obj.partner_ids = activity.as_partner_ids.ids + [activity.user_id.id] + event_obj.partner_ids.ids
            return True
        return False