#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import psycopg2
import psycopg2.extras
import sftp_format,ftp_format
import os,sys,time,psutil,json
from datetime import datetime
import procname

global guarda_pid
global lista_thread
guarda_pid = {}
lista_threads = []

def proc_filho(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,protocolo,banco_dados,json_config,codigo):

	if protocolo == 'ftp' or protocolo == 'FTP':
		if portas != None or portas == '':
			ftp_format.processa(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,banco_dados,json_config,codigo)
		else:
			portas = '21'
			ftp_format.processa(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,banco_dados,json_config,codigo)

	elif protocolo == 'sftp' or protocolo == 'SFTP' or protocolo == 'scp' or protocolo == 'SCP':
		if portas != None or portas == '':
			sftp_format.processa(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,banco_dados,json_config,codigo)
		else:
			portas = '22'
                	sftp_format.processa(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,banco_dados,json_config,codigo)

	else:
		print "\033[1;31m[-]\033[0m Falta o protocolo correto\nProtocolo atual: %s\n" % protocolo

def proc_pai(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,codigo,banco_dados,json_config,protocolo):
	arquivoGrava = open('.pid.fhs','a')
	pid_filho = os.fork()
	if pid_filho == 0:
		proc_filho(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,protocolo,banco_dados,json_config,codigo)
		os.waitpid(pid_filho, 0)
	arquivoGrava.write("%s;%s;%s\n" % (banco_dados,codigo,pid_filho))
	print "\033[1;32m[+]\033[0m PID Filho iniciado: %s" % pid_filho

def restart(nome_banco,id_tabela,resultado):
        #print("%s - %s" % (nome_banco,id_tabela))
	raw_credenciais = open('confs/login_banco.json').read()
	credencial = json.loads(raw_credenciais)
        usuario = credencial['login']
        senha = credencial['pass']
        servidor = credencial['address']
	print "~~> Carregando configurações:\n"
        print "  \033[1;32m[+]\033[0m Usuário: %s" % usuario
        print "  \033[1;32m[+]\033[0m Senha: %s" % senha
        print "  \033[1;32m[+]\033[0m Servidor: %s" % servidor
        print "  \033[1;32m[+]\033[0m BD: %s\n\n" % banco_dados
	#dir_local = 'Download/'
        conecta = psycopg2.connect(dbname=nome_banco, user=usuario, host=servidor, password=senha)
        query = conecta.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query.execute("SELECT * from servidor_arquivo WHERE codigo = %s" % (id_tabela))
	rows = query.fetchall()
        for i in range(len(rows)):
                if rows != None:
                        try:
                                #for row in rows:
                                codigo = rows[i]['codigo']
                                dtcadastro = rows[i]['dtcadastro']
                                cod_template = rows[i]['cod_template']
                                ips = rows[i]['ips']
                                portas = rows[i]['portas']
                                login = rows[i]['login']
                                senha = rows[i]['pass']
                                protocolo = rows[i]['protocolo']
                                diretorio_remoto = rows[i]['diretorio_remoto']
                                diretorio_mover_remoto = rows[i]['diretorio_mover_remoto']
                                frequencia = rows[i]['frequencia']
                                prefixo = rows[i]['prefixo']
                                sufixo = rows[i]['sufixo']
                                situacao = rows[i]['situacao']
                                desc_situacao = rows[i]['desc_situacao']
                                observacao = rows[i]['observacao']
                                dtapagou = rows[i]['dtapagou']
                                login_apagou = rows[i]['login_apagou']
				json_config = rows[i]['json_config']
                                dir_local = "%s/" % (nome_banco)
                                nome_processo = "%s%s" % (nome_banco,codigo)
                                procname.setprocname(nome_processo)
                                proc_pai(ips,\
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
                                        nome_banco,\
					json_config,\
                                        protocolo)
                                os.system("python mon.py %s %s &" % (nome_banco,codigo))
                        except KeyError:
                                codigo = rows[i]['codigo']
                                dtcadastro = rows[i]['dtcadastro']
                                cod_template = rows[i]['cod_template']
                                ips = rows[i]['ips']
                                portas = None
                                login = rows[i]['login']
                                senha = rows[i]['pass']
                                protocolo = rows[i]['protocolo']
                                diretorio_remoto = rows[i]['diretorio_remoto']
                                diretorio_mover_remoto = rows[i]['diretorio_mover_remoto']
                                frequencia = rows[i]['frequencia']
                                prefixo = rows[i]['prefixo']
                                sufixo = rows[i]['sufixo']
                                situacao = rows[i]['situacao']
                                desc_situacao = rows[i]['desc_situacao']
                                observacao = rows[i]['observacao']
                                dtapagou = rows[i]['dtapagou']
                                login_apagou = rows[i]['login_apagou']
				json_config = rows[i]['json_config']
                                dir_local = "%s/" % (nome_banco)
                                nome_processo = "%s%s" % (nome_banco,codigo)
                                procname.setprocname(nome_processo)
                                proc_pai(ips,\
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
                                        nome_banco,\
					json_config,\
                                        protocolo)
                                os.system("python mon.py %s %s &" % (nome_banco,codigo))
                else: 
                                print "\033[1;31m[-]\033[0m Tabela vazia\n"

def verifica_inicio():
	#os.system("rm .pid.fhs")
	raw_credenciais = open('confs/login_banco.json').read()
        credencial = json.loads(raw_credenciais)
        usuario = credencial['login']
        senha = credencial['pass']
        servidor = credencial['address']
	banco = credencial['database']
	print "~~> Carregando configurações:\n"
	print "  \033[1;32m[+]\033[0m Usuario: %s" % usuario
	print "  \033[1;32m[+]\033[0m Senha: %s" % senha
	print "  \033[1;32m[+]\033[0m Servidor: %s\n" % servidor
        conn = psycopg2.connect(dbname=banco, user=usuario, host=servidor, password=senha)
        cur = conn.cursor()
        cur.execute("""SELECT * from pg_database WHERE datname NOT IN ('postgres','template0','template1')""")
        linhas_database = cur.fetchall()
        for linha_db in linhas_database:
                banco_dados = linha_db[0]
                conn2 = psycopg2.connect(dbname=banco_dados, user=usuario, host=servidor, password=credencial['pass'])
                cur2 = conn2.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cur2.execute("SELECT * FROM pg_catalog.pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema', 'pg_toast')")
                lista_tabelas = cur2.fetchall()
                for lista_tb in lista_tabelas:
                        if lista_tb[1].strip() == 'servidor_arquivo':
                                cur2.execute("SELECT * FROM servidor_arquivo")
                                rows = cur2.fetchall()
				for i in range(len(rows)):
					if rows != None:
						try:
							print "\033[1;32m[+]\033[0m Carregando configurações de: %s" % banco_dados
							#for row in rows:
							codigo = rows[i]['codigo']
							dtcadastro = rows[i]['dtcadastro']
							cod_template = rows[i]['cod_template']
							ips = rows[i]['ips']
							portas = rows[i]['portas']
							login = rows[i]['login']
							senha = rows[i]['pass']
							protocolo = rows[i]['protocolo']
							diretorio_remoto = rows[i]['diretorio_remoto']
							diretorio_mover_remoto = rows[i]['diretorio_mover_remoto']
							frequencia = rows[i]['frequencia']
							prefixo = rows[i]['prefixo']
							sufixo = rows[i]['sufixo']
							situacao = rows[i]['situacao']
							desc_situacao = rows[i]['desc_situacao']
							observacao = rows[i]['observacao']
							dtapagou = rows[i]['dtapagou']
							login_apagou = rows[i]['login_apagou']
							json_config = rows[i]['json_config']
							dir_local = "%s/" % (banco_dados)
							nome_processo = "%s%s" % (banco_dados,codigo)
							procname.setprocname(nome_processo)
							if login_apagou == None:
								proc_pai(ips,\
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
								lol = 'sopranaoficarvazio'
						except KeyError:
							codigo = rows[i]['codigo']
							dtcadastro = rows[i]['dtcadastro']
							cod_template = rows[i]['cod_template']
							ips = rows[i]['ips']
							portas = None
							login = rows[i]['login']
							senha = rows[i]['pass']
							protocolo = rows[i]['protocolo']
							diretorio_remoto = rows[i]['diretorio_remoto']
							diretorio_mover_remoto = rows[i]['diretorio_mover_remoto']
							frequencia = rows[i]['frequencia']
							prefixo = rows[i]['prefixo']
							sufixo = rows[i]['sufixo']
							situacao = rows[i]['situacao']
							desc_situacao = rows[i]['desc_situacao']
							observacao = rows[i]['observacao']
							dtapagou = rows[i]['dtapagou']
							login_apagou = rows[i]['login_apagou']
							json_config = rows[i]['json_config']
							dir_local = "%s/" % (banco_dados)
							nome_processo = "%s%s" % (banco_dados,codigo)
							procname.setprocname(nome_processo)
							if login_apagou == None:
                                                                proc_pai(ips,\
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
                                                                lol = 'sopranaoficarvazio'
					else: 
							print "\033[1;31m[-]\033[0m Tabela vazia\n"	
					
					 


if __name__ == '__main__':
	argumento = sys.argv[1]
	if 'start' == argumento:
		os.system("clear")
		print "\033[1;32m[+]\033[0m Iniciando gerenciamento de downloads...\n\n"
		verifica_inicio()
	elif 'restart' == argumento:
		nome_banco = sys.argv[2]
		id_tabela = sys.argv[3]
		resultado = [4]
		print "\033[1;33m[+]\033[0m Reiniciando %s\n" % nome_banco
		restart(nome_banco,id_tabela,resultado)

