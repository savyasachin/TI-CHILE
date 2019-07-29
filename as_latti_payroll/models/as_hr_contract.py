# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

from odoo.exceptions import UserError, ValidationError

class hr_contract(models.Model):
    _inherit = 'hr.contract'    

    gratificacion_porcentage = fields.Integer('Gratificación Porcentage', default=25)

    #constraint
    @api.constrains('gratificacion_porcentage')
    @api.one
    def _check_gratificacion_porcentage(self):
        porcentage = self.gratificacion_porcentage
        if porcentage > 100 or porcentage < 0:
            raise ValidationError(_('El valor de porcentage debe ser entre 0 y 100'))