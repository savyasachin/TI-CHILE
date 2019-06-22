# -*- coding: utf-8 -*-
##############################################################################
import time
from datetime import datetime
from datetime import time as datetime_time
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import json

import logging
_logger = logging.getLogger(__name__)

class as_hr_indicadores_previsionales(models.Model):
    _inherit = 'hr.indicadores'


    def get_previred(self,month_year):
        urlData = "https://api.gael.cl/general/public/previred/"+month_year
        webURL = urlopen(urlData)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        return json.loads(data.decode(encoding))
    
    def month_year(self):
        month=''
        if self.month == '1':
            month='01'
        elif self.month == '2':
            month='02'
        elif self.month == '3':
            month='03'
        elif self.month == '4':
            month='04'
        elif self.month == '5':
            month='05'
        elif self.month == '6':
            month='06'
        elif self.month == '7':
            month='07'
        elif self.month == '8':
            month='08'
        elif self.month == '9':
            month='09'
        elif self.month == '10':
            month='10'
        elif self.month == '11':
            month='11'
        elif self.month == '12':
            month='12'
        return month+str(self.year)

    @api.one
    def as_update_document(self):
        try:
            month_year = self.month_year()
            # month_year = self.year + str(self.year)
            obj_json = self.get_previred(month_year)
            
            # UF
            self.uf = float(obj_json['UFValPeriodo'].replace(',','.'))

            # 1 UTM
            self.utm = float(obj_json['UTMVal'].replace(',','.'))

            # 1 UTA
            self.uta = float(obj_json['UTAVal'].replace(',','.'))

            # 3 RENTAS TOPES IMPONIBLES UF
            self.tope_imponible_afp = float(obj_json['RTIAfpUF'].replace(',','.'))
            self.tope_imponible_ips = float(obj_json['RTIIpsUF'].replace(',','.'))
            self.tope_imponible_seguro_cesantia = float(obj_json['RTISegCesUF'].replace(',','.'))

            # 4 RENTAS TOPES IMPONIBLES
            self.sueldo_minimo = float(obj_json['RMITrabDepeInd'].replace(',','.'))
            self.sueldo_minimo_otro = float(obj_json['RMIMen18May65'].replace(',','.'))

            # Ahorro Previsional Voluntario
            self.tope_mensual_apv = float(obj_json['APVTopeMensUF'].replace(',','.'))
            self.tope_anual_apv = float(obj_json['APVTopeAnuUF'].replace(',','.'))

            # 5 DEPÓSITO CONVENIDO
            self.deposito_convenido = float(obj_json['DepConvenidoUF'].replace(',','.'))

            # 6 RENTAS TOPES IMPONIBLES
            self.contrato_plazo_indefinido_empleador = float(obj_json['AFCCpiEmpleador'].replace(',','.'))
            self.contrato_plazo_indefinido_trabajador = float(obj_json['AFCCpiTrabajador'].replace(',','.'))
            self.contrato_plazo_fijo_empleador = float(obj_json['AFCCpfEmpleador'].replace(',','.'))
            self.contrato_plazo_indefinido_empleador_otro = float(obj_json['AFCCpi11Empleador'].replace(',','.'))

            # 7 ASIGNACIÓN FAMILIAR
            self.asignacion_familiar_monto_a = float(obj_json['AFamTramoAMonto'].replace(',','.'))
            self.asignacion_familiar_monto_b = float(obj_json['AFamTramoBMonto'].replace(',','.'))
            self.asignacion_familiar_monto_c = float(obj_json['AFamTramoCMonto'].replace(',','.'))

            self.asignacion_familiar_primer = float(obj_json['AFamTramoAHasta'].replace(',','.'))
            self.asignacion_familiar_segundo = float(obj_json['AFamTramoBHasta'].replace(',','.'))
            self.asignacion_familiar_tercer = float(obj_json['AFamTramoCDesde'].replace(',','.'))

            # 8 TASA COTIZACIÓN OBLIGATORIO AFP
            self.tasa_afp_capital = float(obj_json['AFPCapitalTasaDep'].replace(',','.'))
            self.tasa_sis_capital = float(obj_json['AFPCapitalTasaSIS'].replace(',','.'))

            self.tasa_afp_cuprum = float(obj_json['AFPCuprumTasaDep'].replace(',','.'))
            self.tasa_sis_cuprum = float(obj_json['AFPCuprumTasaSIS'].replace(',','.'))

            self.tasa_afp_habitat = float(obj_json['AFPHabitatTasaDep'].replace(',','.'))
            self.tasa_sis_habitat = float(obj_json['AFPHabitatTasaSIS'].replace(',','.'))

            self.tasa_afp_planvital = float(obj_json['AFPPlanVitalTasaDep'].replace(',','.'))
            self.tasa_sis_planvital = float(obj_json['AFPPlanVitalTasaSIS'].replace(',','.'))

            self.tasa_afp_provida = float(obj_json['AFPProVidaTasaDep'].replace(',','.'))
            self.tasa_sis_provida = float(obj_json['AFPProVidaTasaSIS'].replace(',','.'))

            self.tasa_afp_modelo = float(obj_json['AFPModeloTasaDep'].replace(',','.'))
            self.tasa_sis_modelo = float(obj_json['AFPModeloTasaSIS'].replace(',','.'))

            self.tasa_independiente_capital = float(obj_json['AFPCapitalTasaInd'].replace(',','.'))
            self.tasa_independiente_cuprum = float(obj_json['AFPCuprumTasaInd'].replace(',','.'))
            self.tasa_independiente_habitat = float(obj_json['AFPHabitatTasaInd'].replace(',','.'))
            self.tasa_independiente_planvital = float(obj_json['AFPPlanVitalTasaInd'].replace(',','.'))
            self.tasa_independiente_provida = float(obj_json['AFPProVidaTasaInd'].replace(',','.'))
            self.tasa_independiente_modelo = float(obj_json['AFPModeloTasaInd'].replace(',','.'))

        except ValueError:
            return ""