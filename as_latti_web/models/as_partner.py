# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from datetime import datetime, timedelta

class Partner(models.Model):
    _inherit = 'res.partner'

    as_empresa = fields.Char(string="Empresa")
    as_tipo_soporte = fields.Selection(selection=[('free','Gratis'),('paid','Pagado')], string="Tipo soporte")

Partner()