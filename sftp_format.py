#! /usr/bin/python
# -*- coding: utf-8 -*-
import paramiko
import psycopg2
import time
import json
import sys,subprocess,os,hashlib,linecache
from datetime import datetime

def PrintException():
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

def lista_arquivos(ip,portas,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,banco_dados,json_config,id_tabela):
	global ssh
	ultimo_char_dir_remoto = dir_remoto[len(dir_remoto)-1]
	if ultimo_char_dir_remoto != '/':
		dir_remoto = "%s/" % (dir_remoto)
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip,port=int(portas), username=usuario, password=senha)
		stdin, stdout, stderr = ssh.exec_command("ls -la %s" % (dir_remoto))
		arq_dir_remoto = stdout.readlines()
		for i in range(len(arq_dir_remoto)):
			val_nome_real = len(arq_dir_remoto[i].split(' '))
			nome_real = arq_dir_remoto[i].split(' ')[val_nome_real-1]
			if prefixo in nome_real and sufixo in nome_real:
				origem = "%s%s" % (dir_remoto,nome_real)
				destino = "%s%s/%s" % (dir_local.replace('ifclick_',''),usuario,nome_real)
				baixa_arquivos(origem.strip(),destino.strip(),ip,usuario,senha,dir_mover_remoto,nome_real,dir_local,banco_dados,json_config,id_tabela)
				
			elif prefixo is not nome_real and sufixo is nome_real:
				sopranaoficarvazio = "0"
			elif prefixo is nome_real and sufixo is not nome_real:
				sopranaoficarvazio = "0"
			else:
				sopranaoficarvazio = "0"
	except Exception as ex:
		now = datetime.now()
		arquivoGrava = open('log_erro.log','a')
		PrintException()
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
		

def baixa_arquivos(origem,destino,ip,usuario,senha,dir_mover_remoto,nome_real,dir_local,banco_dados,json_config,id_tabela):
	print "baixa_arquivos"
	dir_local = "%s%s" % (dir_local, usuario)
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
                                                                                                                                                nome_real,\
                                                                                                                                                id_tabela))
        conecta.commit()

	if os.path.exists(dir_local) == True:
		ftp = ssh.open_sftp() 
		ftp.get(origem, destino)
		ftp.close()
		############ Envio POST json_config
                arquivo = destino
		data = json.loads(json_config)
		url = data['arquivo_post']
		f = {data['tipo_arquivo']: open(arquivo,'rb')}
		v = data['posts']
		r = requests.post(url = url, files = f, data = v)
		#print r.status_code
		#print r.headers
		#print r.text

                ############ Fim Envio POST
		hasher = hashlib.md5()
		tam_arquivo = os.path.getsize(destino)
		with open(destino, 'rb') as afile:
			buf = afile.read()
			hasher.update(buf)
		md5 = hasher.hexdigest()
		tamanho = "%i" % (tam_arquivo)
		print tamanho
		query.execute("INSERT INTO log_servidor_arquivo (nome, tamanho, md5) values ('%s',%s,'%s')" % (nome_real,tamanho,md5))
	        conecta.commit()
		
	else:
		os.makedirs(dir_local, 0755)
		ftp = ssh.open_sftp() 
                ftp.get(origem, destino)
                ftp.close()
		############ Envio POST
		arquivo = destino
                data = json.loads(json_config)
                url = data['arquivo_post']
                f = {data['tipo_arquivo']: open(arquivo,'rb')}
                v = data['posts']
                r = requests.post(url = url, files = f, data = v)
                #print r.status_code
                #print r.headers
                #print r.text
                ############ Fim Envio POST
		hasher = hashlib.md5()
                tam_arquivo = os.path.getsize(destino)
                with open(destino, 'rb') as afile:
                        buf = afile.read()
                        hasher.update(buf)
                md5 = hasher.hexdigest()
                tamanho = "%i" % (tam_arquivo)
		print tamanho
                query.execute("INSERT INTO log_servidor_arquivo (nome, tamanho, md5) values ('%s',%s,'%s')" % (nome_real,tamanho,md5))
                conecta.commit()

		
	
	if dir_mover_remoto != None:
        	ssh.exec_command("mv %s %s%s" % (origem,dir_mover_remoto,nome_real.strip()))
	else:
		ssh.exec_command("rm %s" % (origem))

def processa(ip,portas,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,tempo,banco_dados,json_config,id_tabela):
	while True:
                time.sleep(tempo)
                lista_arquivos(ip,portas,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,banco_dados,json_config,id_tabela)


