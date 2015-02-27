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

def proc_filho(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,protocolo,banco_dados,codigo):
	if protocolo == 'ftp' or protocolo == 'FTP':
		if portas != None:
			ftp_format.processa(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,banco_dados,codigo)
		else:
			portas = '21'
			ftp_format.processa(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,banco_dados,codigo)

	elif protocolo == 'sftp' or protocolo == 'SFTP' or protocolo == 'scp' or protocolo == 'SCP':
		if portas != None:
			sftp_format.processa(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,banco_dados,codigo)
		else:
			portas = '22'
                	sftp_format.processa(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,banco_dados,codigo)

	else:
		print "Falta o protocolo correto\nProtocolo atual: %s" % protocolo

def proc_pai(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,codigo,banco_dados,protocolo):
	arquivoGrava = open('.pid.fhs','a')
	pid_filho = os.fork()
	if pid_filho == 0:
		proc_filho(ips,portas,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,protocolo,banco_dados,codigo)
		os.waitpid(pid_filho, 0)
	arquivoGrava.write("%s;%s;%s\n" % (banco_dados,codigo,pid_filho))
	#print pid_filho

def restart(nome_banco,id_tabela,resultado):
        #print("%s - %s" % (nome_banco,id_tabela))
	raw_credenciais = open('login_banco.json').read()
	credencial = json.loads(raw_credenciais)
        usuario = credencial['login']
        senha = credencial['pass']
        servidor = credencial['address']
	#dir_local = 'Download/'
        conecta = psycopg2.connect(dbname=nome_banco, user=usuario, host=servidor, password=senha)
        query = conecta.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query.execute("SELECT * from servidor_arquivo WHERE codigo = %s" % (id_tabela))
	rows = cur2.fetchall()
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
                                dir_local = "%s/" % (banco_dados)
                                nome_processo = "%s%s" % (banco_dados,codigo)
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
                                        banco_dados,\
                                        protocolo)
                                os.system("python mon.py %s %s &" % (banco_dados,codigo))
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
                                dir_local = "%s/" % (banco_dados)
                                nome_processo = "%s%s" % (banco_dados,codigo)
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
                                        banco_dados,\
                                        protocolo)
                                os.system("python mon.py %s %s &" % (banco_dados,codigo))
                else: 
                                print "Tabela vazia"

def verifica_inicio():
	#os.system("rm .pid.fhs")
	raw_credenciais = open('login_banco.json').read()
        credencial = json.loads(raw_credenciais)
        usuario = credencial['login']
        senha = credencial['pass']
        servidor = credencial['address']
	banco = credencial['database']
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
							dir_local = "%s/" % (banco_dados)
							nome_processo = "%s%s" % (banco_dados,codigo)
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
								banco_dados,\
								protocolo)
							os.system("python mon.py %s %s &" % (banco_dados,codigo))
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
							dir_local = "%s/" % (banco_dados)
							nome_processo = "%s%s" % (banco_dados,codigo)
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
								banco_dados,\
								protocolo)
							os.system("python mon.py %s %s &" % (banco_dados,codigo))
					else: 
							print "Tabela vazia"	
					
					 


if __name__ == '__main__':
	argumento = sys.argv[1]
	if 'start' == argumento:
		verifica_inicio()
	elif 'restart' == argumento:
		nome_banco = sys.argv[2]
		id_tabela = sys.argv[3]
		resultado = [4]
		restart(nome_banco,id_tabela,resultado)

