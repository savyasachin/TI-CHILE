# -*- coding: utf-8 -*-
import time
from datetime import datetime
from datetime import time as datetime_time
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def compute_sheet(self):
        res = super(HrPayslip, self).compute_sheet()
        return res


class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'
    
    # Se agrega a la linea campos por defecto
    @api.onchange('salary_rule_id')
    def _onchange_salary_rule_id(self):
        if self.salary_rule_id:
            self.name = self.salary_rule_id.name
            self.code = self.salary_rule_id.code
            self.category_id = self.salary_rule_id.category_id.id