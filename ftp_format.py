#! /usr/bin/python
# -*- coding: utf-8 -*-
from ftplib import FTP
from datetime import datetime
import psycopg2
import time
import sys,subprocess,os

#####################################################################################################
#
# lista_arquivos(), 
# Recebe os valores da classe processa() e faz a conexão ftp.
#
#####################################################################################################
def lista_arquivos(ip,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,banco_dados,id_tabela):
	#global ssh

	#### Faz a verificação do ultimo caracter do caminho do diretório
	#### para ver se existe ou não a / no fim, caso não tenha ele
	#### atribui ela no final, evitando erro de string
	ultimo_char_dir_remoto = dir_remoto[len(dir_remoto)-1]
	if ultimo_char_dir_remoto != '/':
		dir_remoto = "%s/" % (dir_remoto)
	####
	try:
		lista_arquivos = []
		ftp = FTP(ip)
		ftp.login(usuario,senha)
		ftp.cwd(dir_remoto)
		ftp.retrlines('NLST', lista_arquivos.append)
		if os.path.exists(dir_local) == True:
			for i in range(len(lista_arquivos)):
				nome_real = lista_arquivos[i].strip()
				nome_local = nome_real.split('/')[len(nome_real.split('/'))-1]
				if prefixo in nome_local and sufixo in nome_local:
					ftp.retrbinary('RETR %s' % nome_real, open('%s%s' % (dir_local,nome_local), 'wb').write)
					if dir_mover_remoto != None:
				                ftp.delete(nome_real)
        				else:
         				        #ssh.exec_command("rm %s" % (origem))
						print "LLL"
					now = datetime.now()
					conecta = psycopg2.connect(dbname=banco_dados, user='danilo', host='127.0.0.1', password='danilo123')
					query = conecta.cursor()
					query.execute("UPDATE servidor_arquivo SET situacao = 'ONLINE', desc_situacao = '%s-%s-%s %s:%s:%s ARQ_BAIXADO: %s' WHERE codigo = %s" % (str(now.day),\
																					str(now.month),\
																					str(now.year),\
																					str(now.hour),\
																					str(now.minute),\
																					str(now.second),\
																					nome_real,\
																					id_tabela))
					conecta.commit()

				else:
					print "%s" % nome_real
		else:
			os.makedirs(dir_local, 0755)
			for i in range(len(lista_arquivos)):
				nome_real = lista_arquivos[i].strip()
				nome_local = nome_real.split('/')[len(nome_real.split('/'))-1]
				if prefixo in nome_local and sufixo in nome_local:
					ftp.retrbinary('RETR %s' % nome_real, open('%s%s' % (dir_local,nome_local), 'wb').write)
					now = datetime.now()
					conecta = psycopg2.connect(dbname=banco_dados, user='danilo', host='127.0.0.1', password='danilo123')
                                        query = conecta.cursor()
                                        query.execute("UPDATE servidor_arquivo SET situacao = 'ONLINE', desc_situacao = '%s-%s-%s %s:%s:%s ARQ_BAIXADO: %s' WHERE codigo = %s" % (str(now.day),\
                                                                                                                                                                        str(now.month),\
                                                                                                                                                                        str(now.year),\
                                                                                                                                                                        str(now.hour),\
                                                                                                                                                                        str(now.minute),\
                                                                                                                                                                        str(now.second),\
                                                                                                                                                                        nome_real,\
                                                                                                                                                                        id_tabela))
                                        conecta.commit()
				else:
					print "%s" % nome_real

	except Exception as ex:
		now = datetime.now()
                arquivoGrava = open('log_erro.log','a')
                arquivoGrava.write("%s-%s-%s %s:%s:%s Log Excetion: Cliente - %s --> ERRO - %s\n" % (str(now.day),\
                                                                                                        str(now.month),\
                                                                                                        str(now.year),\
                                                                                                        str(now.hour),\
                                                                                                        str(now.minute),\
                                                                                                        str(now.second),\
                                                                                                        dir_local,\
                                                                                                        str(ex)))

                conecta = psycopg2.connect(dbname=banco_dados, user='danilo', host='127.0.0.1', password='danilo123')
                query = conecta.cursor()
                if 'Errno 113' in str(ex):
                        query.execute("UPDATE servidor_arquivo SET situacao = 'OFFLINE', desc_situacao = '%s-%s-%s %s:%s:%s Log: %s' WHERE codigo = %s" % (str(now.day),\
                                                                                                                                                        str(now.month),\
                                                                                                                                                        str(now.year),\
                                                                                                                                                        str(now.hour),\
                                                                                                                                                        str(now.minute),\
                                                                                                                                                        str(now.second),\
                                                                                                                                                        str(ex),\
                                                                                                                                                        id_tabela))
			conecta.commit()
		elif '530 Login incorrect' in str(ex) or 'Authentication failed' in str(ex):
                        query.execute("UPDATE servidor_arquivo SET situacao = 'ONLINE', desc_situacao = '%s-%s-%s %s:%s:%s Log: %s' WHERE codigo = %s" % (str(now.day),\
                                                                                                                                                        str(now.month),\
                                                                                                                                                        str(now.year),\
                                                                                                                                                        str(now.hour),\
                                                                                                                                                        str(now.minute),\
                                                                                                                                                        str(now.second),\
                                                                                                                                                        str(ex),\
                                                                                                                                                        id_tabela))
                        conecta.commit()

	####

######################################################################################################
#def baixa_arquivos(origem,destino,ip,usuario,senha,dir_mover_remoto,nome_real):
#	#### que queira copiar o arquivo depois de baixado ele
#####################################################################################################
def processa(ip,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,tempo,banco_dados,id_tabela):
	while True:
                time.sleep(tempo)
                lista_arquivos(ip,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,banco_dados,id_tabela)


