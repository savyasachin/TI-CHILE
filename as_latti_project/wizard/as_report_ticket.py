# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models

class as_kardex_productos_wiz(models.TransientModel):
    _name="as.report.tickets"
    _description = "Warehouse Reports by AhoraSoft"
    
    start_date = fields.Date('Desde la Fecha', default=fields.Date.context_today)
    end_date = fields.Date('Hasta la Fecha', default=fields.Date.context_today)
    stage_id = fields.Many2many('helpdesk.stage',string='Etapa')
    partner_id = fields.Many2many('res.partner', string='Cliente')
    as_empresa = fields.Many2many('as.empresa', string='Empresa')
    
    # as_cliente = fields.Many2many('stock.location', string="Almacen", domain="[('usage', '=', 'internal')]")
    # as_estado = fields.Many2many('stock.location', string="Almacen", domain="[('usage', '=', 'internal')]")
    # as_empresa = fields.Many2many('stock.location', string="Almacen", domain="[('usage', '=', 'internal')]")
   
    @api.multi
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'as.report.tickets'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls_export'):
            return self.env.ref('as_latti_project.tickets_soporte_xlsx').report_action(self, data=datas)