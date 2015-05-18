# -*- coding: utf-8 -*-

__author__ = "Danilo Vaz"
__copyright__ = "Copyright 2015, DWrobot"
__credits__ = ["Danilo Vaz"]
__license__ = "GPL"
__version__ = "1.2"
__maintainer__ = "Danilo Vaz"
__email__ = "danilovazb@gmail.com"
__status__ = "Beta"

# ~~~ Import ~~~ #
from ftplib import FTP
from envio_email import enviaEmail
from datetime import datetime
from saveLogs import saveLogs
import signal
import psycopg2
import traceback
import time
import sys
import subprocess
import os
import hashlib
import json
import linecache
import requests
# ~~~~~~~~~~~~~~ #

class Ftp_download(object):

	def __init__(self,ip,portas,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,tempo,banco_dados,json_config,id_tabela):
		self.ip = ip
		self.portas = portas
		self.usuario = usuario
		self.senha = senha
		self.prefixo = prefixo
		self.sufixo = sufixo
		self.dir_remoto = dir_remoto
		self.dir_mover_remoto = dir_mover_remoto
		self.dir_local = dir_local
		self.tempo = tempo
		self.banco_dados = banco_dados
		self.json_config = json_config
		self.id_tabela = id_tabela
		signal.signal(signal.SIGINT, self.signal_handler)

	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Faz a conexao com o cliente											 #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
		
	def conecta(self):
		ftp = FTP()
		ftp.connect(self.ip,self.portas, 400)
		ftp.login(self.usuario,self.senha)
		txt1 = "CONECTANDO-SE AO FTP:\n"
		#self.printMSGALERTA(txt1)
		print(txt1)
		txt2 = " IP: %s\n" % self.ip
		#self.printMSGALERTA(txt2)
		print(txt2)
		txt3 = " PORTA: %s\n" % self.portas
		#self.printMSGALERTA(txt3)
		print(txt3)
		return ftp

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Entra no diretorio onde contem os arquivos para download e retorna   #
	# o conteudo do diretorio.												 #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	def entra_dir(self, ftp,dir_remoto):
		txt = " ACESSANDO DIRETÓRIO REMOTO: %s %s\n\n" % (self.banco_dados.replace('ifclick_',''),self.dir_remoto)
		#self.printMSGALERTA(txt)
		print(txt)
		ftp.cwd(dir_remoto)
		return ftp

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Lista os arquivos na pasta solicitada								 #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	
	def list_arq(self,ftp):
		lista_arquivos = []
		ftp = self.entra_dir(ftp,self.dir_remoto)
		ftp.retrlines('NLST', lista_arquivos.append)
		return lista_arquivos

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Escreve log de erro do arquivo no banco de dados 					 #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	def LOGErroArquivo(self,erro):
		nome_real = ''
		tamanho = ''
		md5 = ''
		dtinicio = ''
		dtfim = ''
		id_tabela = ''
		now = datetime.now()
		arquivoGrava = open('log_erro.log','a')
		arquivoGrava.write("%s-%s-%s %s:%s:%s Log Excetion: ERRO %s \n" % \
		(str(now.day),str(now.month),str(now.year),str(now.hour),str(now.minute),str(now.second),str(erro)))
		if '530 Login incorrect' in str(erro) or 'Authentication failed' in str(erro):
			if '\'' in erro:
				erro = erro.replace("\'","")
			tipoErro = 'LOGIN_INVALIDO'
			gravaosfuckinglogs = saveLogs(erro,self.id_tabela,self.banco_dados,tipoErro,nome_real,tamanho,md5,dtinicio,dtfim)
			gravaosfuckinglogs.errorlog()
			email = "lol"
			#print "Passando pelo ERRO DE LOGIN" # DEBUG
			envia_email = enviaEmail(erro,email)
			envia_email.envia_email()
		else:
			if '\'' in erro:
				erro = erro.replace("\'","")
			tipoErro = 'OFFLINE'
			gravaosfuckinglogs = saveLogs(erro,self.id_tabela,self.banco_dados,tipoErro,nome_real,tamanho,md5,dtinicio,dtfim)
			gravaosfuckinglogs.errorlog()
			email = "lol"
			envia_email = enviaEmail(erro,email)
			envia_email.envia_email()
			#print "Passando pelo ERRO DE OFFLINE" # DEBUG

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Escreve log de download do arquivo no banco de dados 				 #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	def LOGDownloadArquivo(self,dtinicio,nome_real):
		dtimefim = datetime.now()
		tipoErro = ''
		erro = ''
		dtfim = "%s-%s-%s %s:%s:%s" % (str(dtimefim.day),str(dtimefim.month),str(dtimefim.year),str(dtimefim.hour),str(dtimefim.minute),str(dtimefim.second))
		hasher = hashlib.md5()
		tam_arquivo = os.path.getsize(nome_real)
		with open(nome_real, 'rb') as afile:
			buf = afile.read()
			hasher.update(buf)
		md5 = hasher.hexdigest()
		tamanho = "%i" % (tam_arquivo)
		gravaosfuckinglogs = saveLogs(erro,self.id_tabela,self.banco_dados,tipoErro,nome_real,tamanho,md5,dtinicio,dtfim)
		gravaosfuckinglogs.gravalog()

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Escreve msg na tela de forma positiva([+]) 				 			 #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	def printMSGALERTA(self,string):
		sys.stdout.write("\033[1;34m[+]\033[0m")
		for i in range(len(string)):
			sys.stdout.write("%s" % string[i])
			sys.stdout.flush()
			time.sleep(0.01)

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Recebe lista de arquivos na pasta e faz o download do arquivo        #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	def download_arquivo(self):
		try:
			dtime = datetime.now()
			lista_arquivos = []
			ftp = self.conecta()
			lista_arquivos = self.list_arq(ftp)
			arquivos = self.select_arq(lista_arquivos)
			if self.verifica_dir() is True:
				for i in range(len(arquivos)):
					ftp.retrbinary('RETR %s' % arquivos[i],\
					open('%s%s' % (self.dir_local,arquivos[i]), 'wb').write)
					nome_real = '%s%s' % (self.dir_local,arquivos[i])
					dtinicio = "%s-%s-%s %s:%s:%s" % \
					(str(dtime.day),str(dtime.month),\
					str(dtime.year),str(dtime.hour),\
					str(dtime.minute),str(dtime.second))
					self.envia_post(nome_real)
					self.verifica_mover(arquivos[i],ftp)
					self.LOGDownloadArquivo(dtinicio,nome_real)
		except Exception as erro:
			#print "LOL"
			for frame in traceback.extract_tb(sys.exc_info()[2]):
				fname,lineno,fn,text = frame
			erro = "\n==================\nERRO: %s \nLINHA: %s \nARQUIVO: %s \nTEXTO: %s CLIENTE: %s\n==================\n" % (erro,lineno,fname,text,self.banco_dados)
			self.LOGErroArquivo(erro)

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Verifica se move o arquivo para pastas no servidor do cliente        #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
		
	def verifica_mover(self,nome,ftp):
		if self.dir_mover_remoto == None or self.dir_mover_remoto == '':
			ftp.delete(nome)
		else:
			txt = " - [%s] MOVENDO PARA PASTA REMOTA: %s\n" % (self.banco_dados.replace('ifclick_',''),self.dir_mover_remoto)
			#self.printMSGALERTA(txt)
			print(txt)
			name_rename = "%s%s" % (self.dir_mover_remoto,nome)
			ftp.rename(nome,name_rename)

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Verifica se o diretorio onde guarda os arquivos de download existe   #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	def verifica_dir(self):	
		if os.path.exists(self.dir_local) == True:
			return True
		else:
			os.makedirs(self.dir_local, 0755)
			return True

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Compara os arquivos para ver se tem o prefixo e o sufixo solicitado  #
	# e retorna o nome do arquivo                                            #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	def select_arq(self,lista_arquivos):
		arquivos = []
		for i in range(len(lista_arquivos)):
			nome_arquivo = lista_arquivos[i].strip()
			if self.prefixo in nome_arquivo and self.sufixo in nome_arquivo:
				arquivos.append(nome_arquivo)
		return arquivos

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Envia o arquivo via POST para a pagina de envio de emails			 #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	def envia_post(self,nome_real):
		data = json.loads(self.json_config)
		url = data['arquivo_post']
		f = {data['tipo_arquivo']: open(nome_real,'rb')}
		v = data['posts']
		r = requests.post(url = url, files = f, data = v)
		txt = "[%s] STATUS POST: %s\n" % (self.banco_dados.replace('ifclick_',''),r.status_code)
		#self.printMSGALERTA(txt)
		print(txt)
		txt1 = "[%s] HEADER DA PAGINA DE POST: %s\n" % (self.banco_dados.replace('ifclick_',''),r.headers)
		#self.printMSGALERTA(txt1)
		print(txt1)
		txt2 = "[%s] RETORNO DA PAGINA: %s\n" % (self.banco_dados.replace('ifclick_',''),r.text)
		#self.printMSGALERTA(txt2)
		print(txt2)
	
#	def envia_post(self,nome_real):
#		data = json.loads(self.json_config)
#		url = data['arquivo_post']
#		f = {data['tipo_arquivo']: open(nome_real,'rb')}
#		v = data['posts']
#		codigo = self.conectaBancoCliente()
#		v = v.update({u'cod_log_servidor_arquivo':u'%s' % codigo})
#		r = requests.post(url = url, files = f, data = v)
#		txt = "[%s] STATUS POST: %s\n" % (self.banco_dados.replace('ifclick_',''),r.status_code)
#		#self.printMSGALERTA(txt)
#		print(txt)
#		txt1 = "[%s] HEADER DA PAGINA DE POST: %s\n" % (self.banco_dados.replace('ifclick_',''),r.headers)
#		#self.printMSGALERTA(txt1)
#		print(txt1)
#		txt2 = "[%s] RETORNO DA PAGINA: %s\n" % (self.banco_dados.replace('ifclick_',''),r.text)
#		#self.printMSGALERTA(txt2)
#		print(txt2)

#############################################################################################################
	
	def carregaCredenciaisBanco(self):
		raw_credenciais = open('confs/login_banco.json').read()
		credencial = json.loads(raw_credenciais)
		usuario = credencial['login']
		senha = credencial['pass']
		servidor = credencial['address']
		banco = credencial['database']
		return (usuario,senha,banco,servidor)

	def conectaBancoCliente(self):
		usuario,senha,banco,servidor = self.carregaCredenciaisBanco()
		conecta = psycopg2.connect(dbname=self.banco_dados, user=usuario, host=servidor, password=senha)
		query = conecta.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query.execute("SELECT currval('cod_log_servidor_arquivo') as codigo")
		linhas = query.fetchall()
		for i in range(len(linhas)):
			codigo = linhas[i]['codigo']
		return codigo

#############################################################################################################	
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Controla o tempo de processo, o tempo que sera executado o download  #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
		
	def time_control(self):
		while True:
			time.sleep(self.tempo)
			self.download_arquivo()
			signal.signal(signal.SIGINT, self.signal_handler)

	def signal_handler(self,signal, frame):
		espaco = " " * 300
		sys.stdout.write('\rBYE BYE \o_ %s\n' % espaco)
		sys.exit(0)
