# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from datetime import datetime, timedelta

class Partner(models.Model):
    _inherit = 'res.partner'

    as_empresa = fields.Many2one('as.empresa',string="Empresa")
    as_tipo_soporte = fields.Selection(selection=[('free','Gratis'),('paid','Pagado')], string="Tipo soporte")

class as_empresa(models.Model):
    _name = 'as.empresa'

    name = fields.Char(string="Empresa")