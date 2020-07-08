# -*- coding: utf-8 -*-

import odoo
from odoo.addons.auth_signup.controllers.main import AuthSignupHome

from odoo.http import request

class AsAuthSignupHome(AuthSignupHome):

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password' , 'as_empresa', 'as_tipo_soporte') }
        #se crea la empresa si no existe y se pasa el id
        if values != {}:
            empresa = request.env['as.empresa'].sudo().search([('name','=',values['as_empresa'])])
            if empresa:
                values['as_empresa']= empresa.id
            else:
                empresa_id = request.env['as.empresa'].sudo().create({'name':values['as_empresa']})
                values['as_empresa']= empresa_id.id
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()