# -*- coding: utf-8 -*-

import logging
import json
import re
from dateutil import parser
from datetime import datetime,timedelta

from odoo import _, api, fields, models, exceptions

_logger = logging.getLogger(__name__)


class AsLogCalendar(models.Model):
    _name = 'as.log.calendar'

    date = fields.Datetime("Fecha", default=datetime.now())
    send = fields.Text("Enviado")
    response = fields.Text("Recibido")