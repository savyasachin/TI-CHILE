# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from datetime import datetime, timedelta

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    stage_time_ids = fields.One2many('helpdesk.ticket.stage.time','ticket_id', string='Tiempo por etapa')

    @api.model
    def create(self, vals):
        helpdesk = super(HelpdeskTicket, self).create(vals)
        helpdesk.stage_time_ids.create({
            'ticket_id': helpdesk.id,
            'stage_id':helpdesk.stage_id.id,
            'last_time': fields.Datetime.now(),
            })
        return helpdesk

    @api.multi
    def write(self, vals):
        if 'stage_id' in vals:
            if self.stage_id.id != vals['stage_id']:
                obj_stage_time_dest =  self.env['helpdesk.ticket.stage.time'].search([('stage_id','=',vals['stage_id']),('ticket_id','=',self.id)])
                if not obj_stage_time_dest:
                    obj_stage_time_dest.create({
                        'ticket_id': self.id,
                        'stage_id':vals['stage_id'],
                        'last_time': fields.Datetime.now(),
                        })
                elif obj_stage_time_dest:
                    obj_stage_time_dest.last_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                obj_stage_time =  self.env['helpdesk.ticket.stage.time'].search([('stage_id','=',self.stage_id.id),('ticket_id','=',self.id)])
                if obj_stage_time:
                    obj_stage_time.time += (datetime.now()-datetime.strptime(obj_stage_time.last_time,'%Y-%m-%d %H:%M:%S')).total_seconds()/3600
                    obj_stage_time.last_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


                a=2
        helpdesk = super(HelpdeskTicket, self).write(vals)        
        return

class helpdesk_ticket_stage_time(models.Model):
    _name = 'helpdesk.ticket.stage.time'

    stage_id = fields.Many2one('helpdesk.ticket.type',string='Etapa')
    time = fields.Float('Tiempo', default=0.0)
    last_time = fields.Datetime(default=fields.Datetime.now)
    ticket_id = fields.Many2one('helpdesk.ticket', string="Tarea")