# Copyright 2019 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.http import route, Controller, request
from werkzeug.utils import redirect

import logging
_logger = logging.getLogger(__name__)

class MainController(Controller):
    @route('/office-365-oauth/success', type='http')
    def success(self, **kwargs):
        user = request.env.user
        #token = user.office_365_get_token(request.httprequest.url)
        url = user.office_365_get_url()
        trash_url_index = (request.httprequest.url).find('/office-365-oauth/success')
        trash_url = request.httprequest.url[:trash_url_index]
        #_logger.debug("\n\n URL : %s --- %s  ----- INDEX %s   URL: %s\n\n",url,request.httprequest.url, trash_url,request.httprequest.url[:trash_url])
        rpl_token = str(request.httprequest.url).replace(trash_url,url)
        _logger.debug("\n\nURL : %s\n\n",rpl_token)
        token = user.office_365_get_token(rpl_token)
        user.office_365_persist_token(token)

        return redirect('/')
