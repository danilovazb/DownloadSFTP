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
from datetime import datetime
import psycopg2
import json
import psycopg2.extras
# ~~~~~~~~~~~~~~ #

class saveLogs(object):

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Define as variaveis que serao usadas								 #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	
	def __init__(self,erro,id_tabela,banco_dados,tipoErro,nome_real,tamanho,md5,dtinicio,dtfim):
		self.erro = erro
		self.id_tabela = id_tabela
		self.banco_dados = banco_dados
		self.tipoErro = tipoErro
		self.nome_real = nome_real
		self.tamanho = tamanho
		self.md5 = md5
		self.dtinicio = dtinicio
		self.dtfim = dtfim

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Faz a conexao com o banco de banco_dados 							 #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	def conBanco(self):
		raw_credenciais = open('confs/login_banco.json').read()
		credencial = json.loads(raw_credenciais)
		usuario = credencial['login']
		senha = credencial['pass']
		servidor = credencial['address']
		conecta = psycopg2.connect(dbname=self.banco_dados, user=usuario, host=servidor, password=senha)
		return conecta

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Realiza o upload na tabela com os dados da situacao e descricao      #
	#   da situacao com erro na tabela servidor_arquivo						 #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	def errorlog(self):
		now = datetime.now()
		conecta = self.conBanco()
		query = conecta.cursor()
		#query.execute("UPDATE servidor_arquivo SET situacao = '%s', desc_situacao = 'ERROR %s-%s-%s %s:%s:%s Log: %s' WHERE codigo = %s" % \
		#(self.tipoErro,str(now.day),str(now.month),str(now.year),str(now.hour),str(now.minute),str(now.second),str(self.erro),self.id_tabela))
		#conecta.commit()

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Controla o tempo de processo, o tempo que sera executado o download  #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
		
	def gravalog(self):
		now = datetime.now()
		conecta = self.conBanco()
		query = conecta.cursor()
		query.execute("INSERT INTO log_servidor_arquivo (nome, tamanho, md5, dtinicio, dtfim, cod_servidor_arquivo) values ('%s',%s,'%s','%s','%s','%s')" % \
		(self.nome_real,self.tamanho,self.md5,self.dtinicio,self.dtfim,self.id_tabela))
		conecta.commit()
		query.execute("UPDATE servidor_arquivo SET situacao = 'ONLINE', desc_situacao = '%s-%s-%s %s:%s:%s ARQ_BAIXADO: %s' WHERE codigo = %s" % \
		(str(now.day),str(now.month),str(now.year),str(now.hour),str(now.minute),str(now.second),self.nome_real,self.id_tabela))
		conecta.commit()
