#! /usr/bin/python
# -*- coding: utf-8 -*-
import paramiko
import time
import sys,subprocess,os
from datetime import datetime

#####################################################################################################
#
# lista_arquivos(), 
# Recebe os valores da classe processa() e faz a conexão sftp pelo paramiko.
#
#####################################################################################################
def lista_arquivos(ip,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local):
	global ssh
	
	#### Faz a verificação do ultimo caracter do caminho do diretório
	#### para ver se existe ou não a / no fim, caso não tenha ele
	#### atribui ela no final, evitando erro de string
	ultimo_char_dir_remoto = dir_remoto[len(dir_remoto)-1]
	if ultimo_char_dir_remoto != '/':
		dir_remoto = "%s/" % (dir_remoto)
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip, username=usuario, password=senha)
		stdin, stdout, stderr = ssh.exec_command("ls -la %s" % (dir_remoto))
		arq_dir_remoto = stdout.readlines()
		for i in range(len(arq_dir_remoto)):
			val_nome_real = len(arq_dir_remoto[i].split(' '))
			nome_real = arq_dir_remoto[i].split(' ')[val_nome_real-1]
			if prefixo in nome_real and sufixo in nome_real:
				origem = "%s%s" % (dir_remoto,nome_real)
				destino = "%s%s" % (dir_local.replace('ifclick_',''),nome_real)
				baixa_arquivos(origem.strip(),destino.strip(),ip,usuario,senha,dir_mover_remoto,nome_real,dir_local)
			
			#### Ainda estou tratando isso, rsrsrs, logo atribuo alguma
			#### mensagem aqui, caso queira add, fique avonts rsrs	
			elif prefixo is not nome_real and sufixo is nome_real:
				sopranaoficarvazio = "0"
			elif prefixo is nome_real and sufixo is not nome_real:
				sopranaoficarvazio = "0"
			else:
				sopranaoficarvazio = "0"
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

#####################################################################################################
#
# baixa_arquivos(), 
# rece os parametros para baixar o arquivo do servidor e verifica se existe pasta para copiar
# o arquivo remoto ou se pode ser apagado do servidor.
#
#####################################################################################################
def baixa_arquivos(origem,destino,ip,usuario,senha,dir_mover_remoto,nome_real,dir_local):
	print "CHEGUEI ATE AQUI"	
	if os.path.exists(dir_local) == True:
		ftp = ssh.open_sftp() 
		ftp.get(origem, destino)
		ftp.close()
	else:
		os.makedirs(dir_local, 0755)
		ftp = ssh.open_sftp() 
                ftp.get(origem, destino)
                ftp.close()
		
	
	#### Caso exista algum diretório atribuido a variável
	#### dir_mover_remoto que representa o diretório remoto
	#### que queira copiar o arquivo depois de baixado ele
	#### faz a cópia, caso contrário, apaga o arquivo do server
	if dir_mover_remoto != None:
        	ssh.exec_command("mv %s %s%s" % (origem,dir_mover_remoto,nome_real.strip()))
	else:
		ssh.exec_command("rm %s" % (origem))

#####################################################################################################
#
# processa(), 
# recebe valores do manag.py e já faz o controle de tempo estipulado pelo usuario e envia os outros
# dados para a funcao lista_arquivos(). 
#
#####################################################################################################
def processa(ip,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,tempo):
	while True:
                time.sleep(tempo)
                lista_arquivos(ip,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local)


