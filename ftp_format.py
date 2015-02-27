#! /usr/bin/python
# -*- coding: utf-8 -*-
from ftplib import FTP
from datetime import datetime
import psycopg2
import time
import sys,subprocess,os,hashlib,json,linecache

def PrintException():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)



def lista_arquivos(ip,portas,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,banco_dados,id_tabela):
	ultimo_char_dir_remoto = dir_remoto[len(dir_remoto)-1]
	dir_local = "%s%s/" % (dir_local, usuario)
	if ultimo_char_dir_remoto != '/':
		dir_remoto = "%s/" % (dir_remoto)
	try:
		lista_arquivos = []
		ftp = FTP()
		ftp.connect(ip,portas)
		ftp.login(usuario,senha)
		#ftp.set_pasv(False)
		ftp.cwd(dir_remoto)
		ftp.retrlines('NLST', lista_arquivos.append)
		if os.path.exists(dir_local) == True:
			for i in range(len(lista_arquivos)):
				nome_real = lista_arquivos[i].strip()
				nome_local = nome_real.split('/')[len(nome_real.split('/'))-1]
				destino = "%s%s" % (dir_local,nome_local)
				if prefixo in nome_local and sufixo in nome_local:
					ftp.retrbinary('RETR %s' % nome_real, open('%s%s' % (dir_local,nome_local), 'wb').write)
					print "DIRETORIO REMOTO: %s" % dir_mover_remoto
					if dir_mover_remoto != None:
				                ftp.delete(nome_real)
        				else:
						nome_rename = "%s%s" % (dir_mover_removo,nome_local)
						ftp.rename(nome_local,nome_rename)
					now = datetime.now()
					raw_credenciais = open('login_banco.json').read()
			                credencial = json.loads(raw_credenciais)
			                usuario = credencial['login']
			                senha = credencial['pass']
                			servidor = credencial['address']
					conecta = psycopg2.connect(dbname=banco_dados, user=usuario, host=servidor, password=senha)
					query = conecta.cursor()
					query.execute("UPDATE servidor_arquivo SET situacao = 'ONLINE', desc_situacao = '%s-%s-%s %s:%s:%s ARQ_BAIXADO: %s' WHERE codigo = %s" % (str(now.day),\
																					str(now.month),\
																					str(now.year),\
																					str(now.hour),\
																					str(now.minute),\
																					str(now.second),\
																					nome_local,\
																					id_tabela))
					conecta.commit()
					hasher = hashlib.md5()
					tam_arquivo = os.path.getsize(destino)
					with open(destino, 'rb') as afile:
						buf = afile.read()
						hasher.update(buf)
					md5 = hasher.hexdigest()
					tamanho = "%i" % (tam_arquivo)
					query.execute("INSERT INTO log_servidor_arquivo (nome, tamanho, md5) values ('%s',%s,'%s')" % (nome_real,tamanho,md5))
					conecta.commit()

				else:
					print "%s" % nome_real
		else:
			os.makedirs(dir_local, 0755)
			for i in range(len(lista_arquivos)):
				nome_real = lista_arquivos[i].strip()
				nome_local = nome_real.split('/')[len(nome_real.split('/'))-1]
				destino = "%s%s" % (dir_local,nome_local)
				if prefixo in nome_local and sufixo in nome_local:
					ftp.retrbinary('RETR %s' % nome_real, open('%s%s' % (dir_local,nome_local), 'wb').write)
					now = datetime.now()
					raw_credenciais = open('login_banco.json').read()
			                credencial = json.loads(raw_credenciais)
			                usuario = credencial['login']
			                senha = credencial['pass']
			                servidor = credencial['address']
					conecta = psycopg2.connect(dbname=banco_dados, user=usuario, host=servidor, password=senha)
                                        query = conecta.cursor()
                                        query.execute("UPDATE servidor_arquivo SET situacao = 'ONLINE', desc_situacao = '%s-%s-%s %s:%s:%s ARQ_BAIXADO: %s' WHERE codigo = %s" % (str(now.day),\
                                                                                                                                                                        str(now.month),\
                                                                                                                                                                        str(now.year),\
                                                                                                                                                                        str(now.hour),\
                                                                                                                                                                        str(now.minute),\
                                                                                                                                                                        str(now.second),\
                                                                                                                                                                        nome_local,\
                                                                                                                                                                        id_tabela))
                                        conecta.commit()
					hasher = hashlib.md5()
                                        tam_arquivo = os.path.getsize(destino)
                                        with open(destino, 'rb') as afile:
                                                buf = afile.read()
                                                hasher.update(buf)
                                        md5 = hasher.hexdigest()
                                        tamanho = "%i" % (tam_arquivo)
                                        query.execute("INSERT INTO log_servidor_arquivo (nome, tamanho, md5) values ('%s',%s,'%s')" % (nome_real,tamanho,md5))
                                        conecta.commit()
				else:
					print "%s" % nome_real

	except Exception as ex:
		PrintException()
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

		raw_credenciais = open('login_banco.json').read()
                credencial = json.loads(raw_credenciais)
                usuario = credencial['login']
                senha = credencial['pass']
                servidor = credencial['address']
                conecta = psycopg2.connect(dbname=banco_dados, user=usuario, host=servidor, password=senha)
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
                        query.execute("UPDATE servidor_arquivo SET situacao = 'FALHA_LOGIN', desc_situacao = '%s-%s-%s %s:%s:%s Log: %s' WHERE codigo = %s" % (str(now.day),\
                                                                                                                                                        str(now.month),\
                                                                                                                                                        str(now.year),\
                                                                                                                                                        str(now.hour),\
                                                                                                                                                        str(now.minute),\
                                                                                                                                                        str(now.second),\
                                                                                                                                                        str(ex),\
                                                                                                                                                        id_tabela))
                        conecta.commit()
		pass

def processa(ip,portas,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,tempo,banco_dados,id_tabela):
	while True:
                time.sleep(tempo)
                lista_arquivos(ip,portas,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,banco_dados,id_tabela)


