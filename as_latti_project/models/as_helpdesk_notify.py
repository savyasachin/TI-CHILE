# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from datetime import datetime, timedelta

class as_helpdesk_notify(models.Model):
    _name = 'as.helpdesk.notify'

    name = fields.Char(string="Notificar Usuarios")
    as_notify_to = fields.Many2many('res.users', string='Usuarios')
    as_stage_id_initial = fields.Many2one('helpdesk.stage', string='Etapa inicial')
    as_stage_id_final = fields.Many2one('helpdesk.stage', string='Etapa final')