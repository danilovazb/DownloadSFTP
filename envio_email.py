# -*- coding: utf-8 -*-

__author__ = "Danilo Vaz"
__copyright__ = "Copyright 2015, DWrobot"
__credits__ = ["Danilo Vaz"]
__license__ = "GPL"
__version__ = "1.2"
__maintainer__ = "Danilo Vaz"
__email__ = "danilovazb@gmail.com"
__status__ = "Beta"

import smtplib
import sys
import commands
from email.MIMEText import MIMEText

class enviaEmail(object):
	def __init__(self,erro,email):
		self.erro = erro
		self.email = email

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Faz o envio do email de erro com o HTML abaixo						 #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	def envia_email(self):
		try :
			serv=smtplib.SMTP()
			smtpserver="SERVER_SMTP"
			serv.connect(smtpserver,587)
			serv.login("SEU_EMAIL","SUA_SENHA")
			html = """HEAD/BODY HTML DE ERRO"""
			html2 = """FOOTER HTML ERRO"""
			html_tudo = str(html) + str(self.erro) + str(html2)
			msg1 = MIMEText(str(html_tudo),'html')
			msg1['Subject']='ERRO Processo de download XML'
			msg1['From']=""
			msg1['To']=""
			serv.sendmail("EMAIL ENVIO","EMAIL RECEBE", msg1.as_string())
			serv.quit()
		except Exception, e:
			print "Erro : %s" % e
		else:
			print "Concluido"
