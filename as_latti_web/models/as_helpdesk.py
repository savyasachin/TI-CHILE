# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from datetime import datetime, timedelta

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    as_empresa = fields.Char(related='partner_id.as_empresa',string="Empresa")
    as_tipo_soporte = fields.Selection(related='partner_id.as_tipo_soporte', string="Tipo soporte")
