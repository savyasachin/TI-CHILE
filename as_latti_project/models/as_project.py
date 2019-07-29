# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from datetime import datetime, timedelta

class Task(models.Model):
    _inherit = 'project.task'

    stage_time_ids = fields.One2many('project.task.stage.time','task_id', string='Tiempo por etapa')

    @api.model
    def create(self, vals):
        project = super(Task, self).create(vals)
        project.stage_time_ids.create({
            'task_id': project.id,
            'stage_id':project.stage_id.id,
            'last_time': fields.Datetime.now(),
            })
        return project

    @api.multi
    def write(self, vals):
        if 'stage_id' in vals:
            if self.stage_id.id != vals['stage_id']:
                obj_stage_time_dest =  self.env['project.task.stage.time'].search([('stage_id','=',vals['stage_id']),('task_id','=',self.id)])
                if not obj_stage_time_dest:
                    obj_stage_time_dest.create({
                        'task_id': self.id,
                        'stage_id':vals['stage_id'],
                        'last_time': fields.Datetime.now(),
                        })
                elif obj_stage_time_dest:
                    obj_stage_time_dest.last_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                obj_stage_time =  self.env['project.task.stage.time'].search([('stage_id','=',self.stage_id.id),('task_id','=',self.id)])
                if obj_stage_time:
                    obj_stage_time.time += (datetime.now()-datetime.strptime(obj_stage_time.last_time,'%Y-%m-%d %H:%M:%S')).total_seconds()/3600
                    obj_stage_time.last_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


                a=2
        project = super(Task, self).write(vals)        
        return

class project_task_stage_time(models.Model):
    _name = 'project.task.stage.time'

    stage_id = fields.Many2one('project.task.type',string='Etapa')
    time = fields.Float('Tiempo', default=0.0)
    last_time = fields.Datetime(default=fields.Datetime.now)
    task_id = fields.Many2one('project.task', string="Tarea")