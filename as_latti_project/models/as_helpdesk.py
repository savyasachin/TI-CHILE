# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from datetime import datetime, timedelta

class as_HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    stage_time_ids = fields.One2many('helpdesk.ticket.stage.time','ticket_id', string='Tiempo por etapa')
    as_notify = fields.Many2one('as.helpdesk.notify', default= lambda self: self.env['as.helpdesk.notify'].search([('name','=','Notificar Usuarios')], limit=1).id )

    @api.model
    def create(self, vals):
        # Se llama al Super           
        helpdesk = super(as_HelpdeskTicket, self).create(vals)
        # Se crea ticket con el color asignado a su grupo
        vals = []
        if 'team_id' in vals:
            team_id = self.env['helpdesk.team'].search([('id','=',vals['team_id'])])
            if team_id:
                # vals.append({'color':team_id.color})
                helpdesk.color = team_id.color
                # if team_id.as_notify_to:
                #     vals.append({'message_follower_ids': team_id.as_notify_to.ids})
        if not 'stage_id' in vals:
            stage_obj = self.env['helpdesk.stage'].search([('sequence','=',1)], limit=1)
            if stage_obj:
                # vals.append({'stage_id':stage_obj.id})
                helpdesk.stage_id = stage_obj.id
                
                
        # helpdesk.write(vals)
        
        #Se crea el record de tiempo
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
                obj_stage_time_dest =  self.env['helpdesk.ticket.stage.time'].search([('stage_id','=',vals['stage_id']),('ticket_id','=',self.id)],limit=1,order="write_date desc")
                if not obj_stage_time_dest:
                    obj_stage_time_dest.create({
                        'ticket_id': self.id,
                        'stage_id':vals['stage_id'],
                        'last_time': fields.Datetime.now(),
                        })
                elif obj_stage_time_dest:
                    obj_stage_time_dest.last_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                obj_stage_time =  self.env['helpdesk.ticket.stage.time'].search([('stage_id','=',self.stage_id.id),('ticket_id','=',self.id)],limit=1,order="write_date desc")
                if obj_stage_time:
                    obj_stage_time.time += (datetime.now()-datetime.strptime(obj_stage_time.last_time,'%Y-%m-%d %H:%M:%S')).total_seconds()/3600
                    obj_stage_time.last_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        helpdesk = super(as_HelpdeskTicket, self).write(vals)
        return helpdesk

class helpdesk_ticket_stage_time(models.Model):
    _name = 'helpdesk.ticket.stage.time'

    stage_id = fields.Many2one('helpdesk.stage',string='Etapa')
    time = fields.Float('Tiempo', default=0.0)
    last_time = fields.Datetime(default=fields.Datetime.now)
    ticket_id = fields.Many2one('helpdesk.ticket', string="Tarea")

# class HelpdeskTeam(models.Model):
#     _inherit = "helpdesk.team"

#     as_notify_to = fields.Many2many('res.users', 'heldesk_team_users_notify_rel','team_id','user_id',  string='Usuarios')
#     member_ids = fields.Many2many('res.users', 'heldesk_team_res_users_rel', string='Team Members', domain=lambda self: [('groups_id', 'in', self.env.ref('helpdesk.group_helpdesk_user').id)])

