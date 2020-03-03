# # -*- coding: utf-8 -*-

import datetime
from datetime import datetime
import pytz
from odoo import models,fields
from datetime import datetime, timedelta
from time import mktime

class as_kardex_productos_excel(models.AbstractModel):
    _name = 'report.as_latti_project.tickets_soporte.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):        
        dict_almacen = []
        dict_aux = []
        filtro = ''
        if data['form']['stage_id']:
            filtro+= ' and hs.id in '+ str(data['form']['stage_id']).replace('[','(').replace(']',')')
        if data['form']['partner_id']:
            filtro+= ' and rp.id in '+ str(data['form']['partner_id']).replace('[','(').replace(']',')')

        sheet = workbook.add_worksheet('Detalle de Movimientos')
        titulo1 = workbook.add_format({'font_size': 16, 'align': 'center', 'text_wrap': True, 'bold':True })
        titulo2 = workbook.add_format({'font_size': 14, 'align': 'center', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True })
        titulo3 = workbook.add_format({'font_size': 12, 'align': 'left', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True })
        titulo3_number = workbook.add_format({'font_size': 14, 'align': 'right', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True, 'num_format': '#,##0.00' })
        titulo4 = workbook.add_format({'font_size': 12, 'align': 'center', 'text_wrap': True, 'bottom': True, 'top': True, 'left': True, 'right': True, 'bold':True })

        number_left = workbook.add_format({'font_size': 12, 'align': 'left', 'num_format': '#,##0.00'})
        number_right = workbook.add_format({'font_size': 12, 'align': 'right', 'num_format': '#,##0.00'})
        number_right_bold = workbook.add_format({'font_size': 12, 'align': 'right', 'num_format': '#,##0.00', 'bold':True})
        number_right_col = workbook.add_format({'font_size': 12, 'align': 'right', 'num_format': '#,##0.00','bg_color': 'silver'})
        number_center = workbook.add_format({'font_size': 12, 'align': 'center', 'num_format': '#,##0.00'})
        number_right_col.set_locked(False)

        letter12 = workbook.add_format({'font_size': 12, 'align': 'center', 'text_wrap': True, 'bold':True})
        letter11 = workbook.add_format({'font_size': 12, 'align': 'center', 'text_wrap': True})
        letter1 = workbook.add_format({'font_size': 12, 'align': 'left', 'text_wrap': True})
        letter2 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold':False})
        letter3 = workbook.add_format({'font_size': 12, 'align': 'right', 'text_wrap': True})
        letter4 = workbook.add_format({'font_size': 12, 'align': 'left', 'text_wrap': True, 'bold': True})
        letter5 = workbook.add_format({'font_size': 12, 'align': 'right', 'text_wrap': True, 'bold': True})
        letter_locked = letter3
        letter_locked.set_locked(False)

        # Aqui definimos en los anchos de columna
        sheet.set_column('A:A',35, letter1)
        sheet.set_column('B:B',30, letter1)
        sheet.set_column('C:C',12, letter1)
        sheet.set_column('D:D',24, letter1)
        sheet.set_column('E:E',15, letter1)
        sheet.set_column('F:F',15, letter1)
        sheet.set_column('G:G',15, letter1)
        sheet.set_column('H:H',20, letter1)
        sheet.set_column('I:I',15, letter1)
        sheet.set_column('J:J',15, letter1)
        sheet.set_column('K:K',15, letter1)

        fecha_inicial = datetime.strptime(data['form']['start_date'], '%Y-%m-%d').strftime('%d/%m/%Y')
        fecha_final = datetime.strptime(data['form']['end_date'], '%Y-%m-%d').strftime('%d/%m/%Y')
        # Titulos, subtitulos, filtros y campos del reporte
        fecha = (datetime.now() - timedelta(hours=4)).strftime('%d/%m/%Y %H:%M:%S')
        sheet.merge_range('A1:D1', 'Nombre Empresa: '+self.env.user.company_id.name, letter1)
        sheet.merge_range('A2:D2', 'Dirección: '+self.env.user.company_id.street, letter1)
        sheet.merge_range('A3:D3', 'Telefono: '+self.env.user.company_id.phone, letter1)
        sheet.merge_range('A4:D4', self.env.user.company_id.city+'-'+self.env.user.company_id.country_id.name)
        sheet.merge_range('F1:I1', 'Usuario Impresión: '+self.env.user.name, letter1)
        sheet.merge_range('F2:I2', 'Fecha y Hora Impresión: '+fecha, letter1)
         
        sheet.merge_range('A5:I5', 'REPORTE DE TICKETS SOPORTE', titulo1)
        sheet.set_row(4, 40)
        sheet.merge_range('A6:I6', 'DEL '+fecha_inicial+' AL '+fecha_final, letter11)
        filas = 7
        sheet.write(filas, 0, 'CLIENTE',titulo4) #cliente/proveedor
        sheet.write(filas, 1, 'EMPRESA',titulo4) #cliente/proveedor
        sheet.write(filas, 2, 'NRO TICKET',titulo4) #cliente/proveedor
        sheet.write(filas, 3, 'ASUNTO',titulo4) #cliente/proveedor
        sheet.write(filas, 4, 'FECHA DE CREACION',titulo4) #cliente/proveedor
        sheet.write(filas, 5, 'FECHA FINALIZACION',titulo4) #cliente/proveedor
        sheet.write(filas, 6, 'ESTADO',titulo4) #cliente/proveedor
        sheet.write(filas, 7, 'ASIGNADO A',titulo4) #cliente/proveedor
        sheet.write(filas, 8, 'TIEMPO DE ATENCION',titulo4) #cliente/proveedor
        filas += 1

        query_movements = ("""
            SELECT
                rp.name as name
                ,rp.as_empresa as empresa
                ,hd.id as numero
                ,hd.name as asunto
                ,hd.create_date as fecha_creacion
                ,hd.write_date as fecha_fin
                ,hs.name as estado
                ,rp2.name as asignado
                FROM
                    helpdesk_ticket hd
                    INNER JOIN res_partner rp on rp.id=hd.partner_id
                    INNER JOIN helpdesk_stage hs on hs.id=hd.stage_id
                    INNER JOIN res_users ru on ru.id=hd.user_id
                    INNER JOIN res_partner rp2 on rp2.id=ru.partner_id
                WHERE
                    hd.create_date BETWEEN '"""+str(data['form']['start_date'])+"""' AND  '"""+str(data['form']['end_date'])+"""'"""+filtro+"""
                ORDER BY fecha_creacion
            """)
        #_logger.debug(query_movements)
        self.env.cr.execute(query_movements)
        tickes_cargados = [k for k in self.env.cr.fetchall()]
        cantidad = 0 
        for ticket in tickes_cargados:
            cantidad+=1
            fechai = datetime.strptime(ticket[4], '%Y-%m-%d %H:%M:%S.%f')
            fechaf = datetime.strptime(ticket[5], '%Y-%m-%d %H:%M:%S.%f')
            fecha_dias = fechaf - fechai
            sheet.write(filas, 0, ticket[0]) 
            sheet.write(filas, 1, ticket[1]) 
            sheet.write(filas, 2, ticket[2]) 
            sheet.write(filas, 3, ticket[3]) 
            sheet.write(filas, 4,  datetime.strptime(ticket[4], '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y'))
            if ticket[6] == 'Finalizado':
                sheet.write(filas, 5,  datetime.strptime(ticket[5], '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y')) 
            else:
                sheet.write(filas, 5,  '') 
            sheet.write(filas, 6, ticket[6]) 
            sheet.write(filas, 7, ticket[7]) 
            sheet.write(filas, 8, str(fecha_dias.days)+'dias') 
            filas += 1

        sheet.merge_range('A'+str(filas+1)+':B'+str(filas+1),'TOTAL TICKETS', letter12)
        sheet.write(filas, 2, cantidad, letter12) 