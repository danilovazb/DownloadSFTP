#! /usr/bin/python
# -*- coding: utf-8 -*-
from ftplib import FTP
import time
import sys,subprocess,os

#####################################################################################################
#
# lista_arquivos(), 
# Recebe os valores da classe processa() e faz a conexão ftp.
#
#####################################################################################################
def lista_arquivos(ip,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local):
	#global ssh

	#### Faz a verificação do ultimo caracter do caminho do diretório
	#### para ver se existe ou não a / no fim, caso não tenha ele
	#### atribui ela no final, evitando erro de string
	ultimo_char_dir_remoto = dir_remoto[len(dir_remoto)-1]
	if ultimo_char_dir_remoto != '/':
		dir_remoto = "%s/" % (dir_remoto)
	####
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
			else:
				print "%s" % nome_real
	else:
                os.makedirs(dir_local, 0755)
		for i in range(len(lista_arquivos)):
                        nome_real = lista_arquivos[i].strip()
                        nome_local = nome_real.split('/')[len(nome_real.split('/'))-1]
                        if prefixo in nome_local and sufixo in nome_local:
                                ftp.retrbinary('RETR %s' % nome_real, open('%s%s' % (dir_local,nome_local), 'wb').write)
                        else:
                                print "%s" % nome_real

	####

######################################################################################################
#def baixa_arquivos(origem,destino,ip,usuario,senha,dir_mover_remoto,nome_real):
#	#### que queira copiar o arquivo depois de baixado ele
#####################################################################################################
def processa(ip,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,tempo):
	while True:
                time.sleep(tempo)
                lista_arquivos(ip,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local)


