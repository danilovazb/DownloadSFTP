#! /usr/bin/python
# -*- coding: utf-8 -*-
import paramiko
import time
import sys

def lista_arquivos(ip,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local):
	global ssh
	ultimo_char_dir_remoto = dir_remoto[len(dir_remoto)-1]
	if ultimo_char_dir_remoto != '/':
		dir_remoto = "%s/" % (dir_remoto)
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
			destino = "%s%s" % (dir_local,nome_real)
			baixa_arquivos(origem.strip(),destino.strip(),ip,usuario,senha,dir_mover_remoto,nome_real)
			
  		elif prefixo is not nome_real and sufixo is nome_real:
			sopranaoficarvazio = "0"
  		elif prefixo is nome_real and sufixo is not nome_real:
			sopranaoficarvazio = "0"
  		else:
			sopranaoficarvazio = "0"

#####################################################################################################
#
# baixa_arquivos, 
# recebe valores do manager e já faz o controle de tempo estipulado pelo usuario
#
#####################################################################################################
def baixa_arquivos(origem,destino,ip,usuario,senha,dir_mover_remoto,nome_real):
	ftp = ssh.open_sftp() 
	ftp.get(origem, destino)
	ftp.close()
	if dir_mover_remoto != None:
        	ssh.exec_command("mv %s %s%s" % (origem,dir_mover_remoto,nome_real.strip()))
	else:
		ssh.exec_command("rm %s" % (origem))

#####################################################################################################
#
# processa, 
# recebe valores do manager e já faz o controle de tempo estipulado pelo usuario e envia os outros
# dados para a funcao 
#
#####################################################################################################
def processa(ip,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,tempo):
	while True:
                time.sleep(tempo)
                lista_arquivos(ip,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local)


