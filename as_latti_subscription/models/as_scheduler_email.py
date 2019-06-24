# -*- coding: utf-8 -*-
##############################################################################
import time
from datetime import datetime, date
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

import smtplib
from email.mime.text import MIMEText
from email.parser import Parser
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText
# from email.MIMEImage import MIMEImage

import logging
_logger = logging.getLogger(__name__)

class as_scheduler_email(models.Model):
	_name = 'as.scheduler.email'

	name = fields.Char(required=True)
	numberOfUpdates = fields.Integer('Number of updates', help='The number of times the scheduler has run and updated this field')
	lastModified = fields.Date('Last updated')

	def get_days_to_end(self,date_end):
		days = (datetime.strptime(date_end,'%Y-%m-%d').date()-date.today()).days
		#days = 30
		if days in (90,60,30,253):
			return days		
		return 0

	def send_email(self,id_email_tmpl,res_id):
		subs = subscription_ids = self.env['sale.subscription'].sudo().search([('id','=',res_id)],limit=1)
		template_browse = self.env['mail.template'].browse(id_email_tmpl)

		
		if template_browse:
			values = template_browse.generate_email(subs.id, fields=None)
			# values['email_to'] = email_to
			# values['email_from'] = su_id.email
			# values['res_id'] = False
			# if not values['email_to'] and not values['email_from']:
			# 	pass
			email_followers = ''
			for follower in subs.message_partner_ids:
				if follower.email:
					email_followers += follower.email + ","
			if email_followers != "":
				values['email_cc'] = email_followers[:-1]
			mail_mail_obj = self.env['mail.mail']
			msg_id = mail_mail_obj.create(values)
			if msg_id:
				mail_mail_obj.send(msg_id)
			return True
		# subs = subscription_ids = self.env['sale.subscription'].sudo().search([('id','=',res_id)],limit=1)
		# mail_server = self.env['ir.mail_server'].sudo().search([('active','=',True)],limit=1)
		# if mail_server:
		# 	sender = subs.company_id.name
		# 	receivers = 'srgr89@gmail.com'
		# 	subjetc = 'aaaaaa'
		# 	msg = MIMEMultipart('alternative')
		# 	msg['Subject'] = "Renovación suscripción - " + subs.partner_id.name
		# 	msg['From'] = mail_server.smtp_user
		# 	html = '<html><body><p>Hi, I have the following alerts for you!</p></body></html>'
		# 	part2 = MIMEText(html, 'html')
		# 	msg.attach(part2)
		# 	if sub.partner_id.email:
		# 		msg['To'] = receivers				
		# 		#smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=465)
		# 		smtpObj = smtplib.SMTP_SSL('smtp.gmail.com')
		# 		# smtpObj.ehlo()
		# 		# smtpObj.starttls()
		# 		# smtpObj.ehlo()
		# 		smtpObj.login(user=mail_server.smtp_user, password=mail_server.smtp_pass)
		# 		smtpObj.sendmail(mail_server.smtp_user, receivers, msg.as_string())
		# 		#smtpObj.sendmail(sender, receivers, message.encode('utf-8'))
		# 		smtpObj.quit()
		# 		_logger.debug("\n\nSuccessfully sent email\n\n")
		# 	if sub.user_id.email:
		# 		msg['To'] = receivers

		# 		smtpObj = smtplib.SMTP_SSL('smtp.gmail.com')
		# 		smtpObj.login(user=mail_server.smtp_user, password=mail_server.smtp_pass)
		# 		smtpObj.sendmail(mail_server.smtp_user, receivers, msg.as_string())
		# 		smtpObj.quit()
		# 		_logger.debug("\n\nSuccessfully sent email\n\n")

 
	#This function is called when the scheduler goes off
	def as_scheduler_email_do(self):
		get_days_to_end = 0
		aux = ''
		subscription_ids = self.env['sale.subscription'].sudo().search([])
		for sub in subscription_ids:
			if sub.state not in ('close','cancel') and sub.date:
				get_days_to_end = self.get_days_to_end(sub.date)
				# TODO enviar email a ala subscripcion donde se encuentre los dias 90, 60 30 a terminar la subscripcion
				if get_days_to_end == 90:					
					#aux = 'enviar email de 90 dias'
					id_email_tmpl = self.env['mail.template'].search([('name','=','as_tmp_email_subs90')],limit=1).id
					self.send_email(id_email_tmpl,sub.id)
				if get_days_to_end == 60:
					#aux = 'enviar email de 60 dias'
					id_email_tmpl = self.env['mail.template'].search([('name','=','as_tmp_email_subs60')],limit=1).id
					self.send_email(id_email_tmpl,sub.id)
				if get_days_to_end == 30:
					#aux = 'enviar email de 60 dias'
					id_email_tmpl = self.env['mail.template'].search([('name','=','as_tmp_email_subs30')],limit=1).id
					self.send_email(id_email_tmpl,sub.id)
		#_logger.debug("\n\nPrueba automatica %s - %s\n\n", aux, get_days_to_end)