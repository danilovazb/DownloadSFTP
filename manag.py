# -*- coding: utf-8 -*-

__author__ = "Danilo Vaz"
__copyright__ = "Copyright 2015, DWrobot"
__credits__ = ["Danilo Vaz"]
__license__ = "GPL"
__version__ = "1.2"
__maintainer__ = "Danilo Vaz"
__email__ = "danilovazb@gmail.com"
__status__ = "Beta"

import psycopg2
from ftp_format import Ftp_download
from sftp_format import Sftp_download
import psycopg2.extras
import os,sys,time,psutil,json
from datetime import datetime
import procname
from optparse import OptionParser

def carregaCredenciaisBanco():
	raw_credenciais = open('confs/login_banco.json').read()
	credencial = json.loads(raw_credenciais)
	usuario = credencial['login']
	senha = credencial['pass']
	servidor = credencial['address']
	banco = credencial['database']
	return (usuario,senha,banco,servidor)

def conectaBanco():
	usuario,senha,banco,servidor = carregaCredenciaisBanco()
	conecta = psycopg2.connect(dbname=banco, user=usuario, host=servidor, password=senha)
	query = conecta.cursor(cursor_factory=psycopg2.extras.DictCursor)
	return query

def conectaBancoCliente(banco_dados):
	usuario,senha,banco,servidor = carregaCredenciaisBanco()
	conecta = psycopg2.connect(dbname=banco_dados, user=usuario, host=servidor, password=senha)
	query = conecta.cursor(cursor_factory=psycopg2.extras.DictCursor)
	return query

def carregaInfoClientes(query):
	query.execute("""SELECT * 
	FROM pg_catalog.pg_tables 
	WHERE schemaname NOT IN ('pg_catalog', 'information_schema', 'pg_toast')""")
	lista_tabelas = query.fetchall()
	for lista_tb in lista_tabelas:
		if lista_tb[1].strip() == 'servidor_arquivo':
			query.execute("SELECT * FROM servidor_arquivo")
			linhas = query.fetchall()
			return linhas

def proc_filho(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,protocolo,banco_dados,json_config,codigo):

	if protocolo == 'ftp' or protocolo == 'FTP':
		if portas != None or portas == '':
			ftp_download = Ftp_download(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,banco_dados,json_config,codigo)
			ftp_download.time_control()
		else:
			portas = '21'
			ftp_download = Ftp_download(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,banco_dados,json_config,codigo)
			ftp_download.time_control()

	elif protocolo == 'sftp' or protocolo == 'SFTP' or protocolo == 'scp' or protocolo == 'SCP':
		if portas != None or portas == '':
			sftp_download = Sftp_download(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,banco_dados,json_config,codigo)
			sftp_download.time_control()
		else:
			portas = '22'
			sftp_download = Sftp_download(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,banco_dados,json_config,codigo)
			sftp_download.time_control()

	else:
		txt = " PROTOCOLO NÃO LOCALIZADO, PROTOCOLO USADO: %s\n" % protocolo
		printMSGNEGATIVA(txt)

def processoPai(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,codigo,banco_dados,json_config,protocolo):
	pid_filho = os.fork()
	if pid_filho == 0:
		proc_filho(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,protocolo,banco_dados,json_config,codigo)
		os.waitpid(pid_filho, 0)
	printMSGPOSITIVA(" PID FILHO: %s\n" % pid_filho)

def infosClientes(linhas,banco_dados):
	if linhas != None:
		for i in range(len(linhas)):
			try:
				printMSGPOSITIVA("INICIANDO CONFIGURAÇÕES DO BANCO DE DADOS: %s\n" % banco_dados)
				codigo = linhas[i]['codigo']
				dtcadastro = linhas[i]['dtcadastro']
				cod_template = linhas[i]['cod_template']
				ips = linhas[i]['ips']
				portas = linhas[i]['portas']
				login = linhas[i]['login']
				senha = linhas[i]['pass']
				protocolo = linhas[i]['protocolo']
				diretorio_remoto = linhas[i]['diretorio_remoto']
				diretorio_mover_remoto = linhas[i]['diretorio_mover_remoto']
				frequencia = linhas[i]['frequencia']
				prefixo = linhas[i]['prefixo']
				sufixo = linhas[i]['sufixo']
				situacao = linhas[i]['situacao']
				desc_situacao = linhas[i]['desc_situacao']
				observacao = linhas[i]['observacao']
				dtapagou = linhas[i]['dtapagou']
				login_apagou = linhas[i]['login_apagou']
				json_config = linhas[i]['json_config']
				dir_local = "%s/" % (banco_dados)
				nome_processo = "%s%s" % (banco_dados,codigo)
				procname.setprocname(nome_processo)
				printMSG("\033[1;34mCODIGO\033[0m: %s\n" % codigo)
				printMSG("\033[1;34mIP\033[0m: %s\n" % ips)
				printMSG("\033[1;34mPORTA\033[0m: %s\n" % portas)
				printMSG("\033[1;34mLOGIN\033[0m: %s\n" % login)
				printMSG("\033[1;34mSENHA\033[0m: **********\n")
				printMSG("\033[1;34mPROTOCOLO\033[0m: %s\n" % protocolo)
				printMSG("\033[1;34mNOME_PROCESSO\033[0m: %s\n\n" % nome_processo)
				if login_apagou == None:
					processoPai(ips,\
					portas,\
					login,\
					senha,\
					prefixo,\
					sufixo,\
					diretorio_remoto,\
					diretorio_mover_remoto,\
					dir_local,\
					frequencia,\
					codigo,\
					banco_dados,\
					json_config,\
					protocolo)
					os.system("python mon.py %s %s &" % (banco_dados,codigo))
				else:
					printMSGNEGATIVA("LOGIN EXCLUIDO DO BANCO DE DADOS: %s" % banco_dados)

			except KeyError:
				printMSGPOSITIVA("INICIANDO CONFIGURAÇÕES DO BANCO DE DADOS: %s\n" % banco_dados)
				codigo = linhas[i]['codigo']
				dtcadastro = linhas[i]['dtcadastro']
				cod_template = linhas[i]['cod_template']
				ips = linhas[i]['ips']
				portas = None
				login = linhas[i]['login']
				senha = linhas[i]['pass']
				protocolo = linhas[i]['protocolo']
				diretorio_remoto = linhas[i]['diretorio_remoto']
				diretorio_mover_remoto = linhas[i]['diretorio_mover_remoto']
				frequencia = linhas[i]['frequencia']
				prefixo = linhas[i]['prefixo']
				sufixo = linhas[i]['sufixo']
				situacao = linhas[i]['situacao']
				desc_situacao = linhas[i]['desc_situacao']
				observacao = linhas[i]['observacao']
				dtapagou = linhas[i]['dtapagou']
				login_apagou = linhas[i]['login_apagou']
				json_config = linhas[i]['json_config']
				dir_local = "%s/" % (banco_dados)
				nome_processo = "%s%s" % (banco_dados,codigo)
				procname.setprocname(nome_processo)
				printMSG("\033[1;34mCODIGO\033[0m: %s\n" % codigo)
				printMSG("\033[1;34mIP\033[0m: %s\n" % ips)
				printMSG("\033[1;34mPORTA\033[0m: %s\n" % portas)
				printMSG("\033[1;34mLOGIN\033[0m: %s\n" % login)
				printMSG("\033[1;34mSENHA\033[0m: **********\n")
				printMSG("\033[1;34mPROTOCOLO\033[0m: %s\n" % protocolo)
				printMSG("\033[1;34mNOME_PROCESSO\033[0m: %s\n\n" % nome_processo)
				if login_apagou == None:
					processoPai(ips,\
					portas,\
					login,\
					senha,\
					prefixo,\
					sufixo,\
					diretorio_remoto,\
					diretorio_mover_remoto,\
					dir_local,\
					frequencia,\
					codigo,\
					banco_dados,\
					json_config,\
					protocolo)
					os.system("python mon.py %s %s &" % (banco_dados,codigo))
				else:
					printMSGNEGATIVA("LOGIN EXCLUIDO DO BANCO DE DADOS: %s" % banco_dados)
	else:
		printMSGNEGATIVA("TABELA VAZIA: BANCO DE DADOS %s NÃO SERÁ INICIADO\n" % banco_dados)

def carregaBancoDados(query):
	query.execute("""SELECT * 
	from pg_database 
	WHERE datname NOT IN ('postgres','template0','template1')""")
	linhas_database = query.fetchall()
	print("\n")
	for linha_db in linhas_database:
		banco_dados = linha_db[0]
		query = conectaBancoCliente(banco_dados)
		linhas = carregaInfoClientes(query)
		infosClientes(linhas,banco_dados)


def verifica_inicio():
	string = " CARREGANDO CONFIGURAÇÕES \n"
	printMSGPOSITIVA(string)
	printPORCENT()
	query = conectaBanco()
	carregaBancoDados(query)

def printMSG(string):
	for i in range(len(string)):
		sys.stdout.write("%s" % string[i])
		sys.stdout.flush()
		time.sleep(0.01)

def printMSGPOSITIVA(string):
	sys.stdout.write("\033[1;32m[+]\033[0m")
	for i in range(len(string)):
		sys.stdout.write("%s" % string[i])
		sys.stdout.flush()
		time.sleep(0.01)

def printMSGNEGATIVA(string):
	sys.stdout.write("\033[1;33m[-]\033[0m")
	for i in range(len(string)):
		sys.stdout.write("%s" % string[i])
		sys.stdout.flush()
		time.sleep(0.01)

def printPORCENT():
	lin = 1
	string = "----------------------------------------------------------------------------------------------------"

	for i in range(len(string)):
		porcent = lin*100/int(len(string))
		sys.stdout.write('\r{0}> {1}%'.format('='*(porcent/3), porcent))
		sys.stdout.flush()
		time.sleep(0.008)
		lin += 1

def verfStatus(status_prog,bd_prog,id_prog):
	if 'start' == status_prog:
		os.system("clear")
		print(""" 

			██████╗ ██╗    ██╗███████╗████████╗██████╗     
			██╔══██╗██║    ██║██╔════╝╚══██╔══╝██╔══██╗    
			██║  ██║██║ █╗ ██║█████╗     ██║   ██████╔╝    
			██║  ██║██║███╗██║██╔══╝     ██║   ██╔═══╝     
			██████╔╝╚███╔███╔╝██║        ██║   ██║         
			╚═════╝  ╚══╝╚══╝ ╚═╝        ╚═╝   ╚═╝   v1.2

			""")
		string = " INICIANDO GERENCIADOR DE DOWNLOADS\n"
		printMSGPOSITIVA(string)
		time.sleep(2)
		verifica_inicio()
	elif 'restart' == status_prog:
		query = conectaBancoCliente(bd_prog)
		linhas = carregaInfoClientes(query)
		infosClientes(linhas,bd_prog)


if __name__ == '__main__':
	parser=OptionParser("python manager.py -s start/stop/restart")
	parser.add_option('-s',dest='status_prog',type='string',help='Passar um parametro para o programa de start | stop | restart.')
	parser.add_option('--bd',dest='bd_prog',type='string',help='Digite o banco de dados que vai restartar')
	parser.add_option('--id',dest='id_prog',type='string',help='Digite o ID do banco de dados que vai restartar')
	(option,args)=parser.parse_args()
	if(option.status_prog==None):
		print parser.usage
		exit(0)
	elif(option.bd_prog==None and option.id_prog==None):
		bd_prog = '';
		id_prog = '';
		status_prog = option.status_prog
		verfStatus(status_prog,bd_prog,id_prog)
	else:
		status_prog = option.status_prog
		bd_prog = option.bd_prog
		id_prog = option.id_prog
		verfStatus(status_prog,bd_prog,id_prog)

