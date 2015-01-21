#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import psycopg2
import sftp_format
import os,sys
import procname

global guarda_pid
global lista_thread
guarda_pid = {}
lista_threads = []

def proc_filho(ips,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia):
	sftp_format.processa(ips,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia)
	#os._exit(0)

def proc_pai(ips,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,codigo,banco_dados):
	arquivoGrava = open('.pid.fhs','a')
	pid_filho = os.fork()
	if pid_filho == 0:
		proc_filho(ips,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia)
		os.waitpid(pid_filho, 0)
	arquivoGrava.write("%s;%s;%s\n" % (banco_dados,codigo,pid_filho))
	print pid_filho

def restart(nome_banco,id_tabela,resultado):
        #os.kill(int(resultado.strip().split('\n')[0]),9)
        print("%s - %s" % (nome_banco,id_tabela))
        usuario = 'danilo'
        senha = 'danilo123'
        servidor = 'localhost'
	dir_local = 'Download/'
        conecta = psycopg2.connect(dbname=nome_banco, user=usuario, host=servidor, password=senha)
        query = conecta.cursor()
        query.execute("SELECT * from servidor_arquivo WHERE codigo = %s" % (id_tabela))
        linhas = query.fetchall()
        for row in linhas:
                print row
                codigo = row[0]
                dtcadastro = row[1]
                cod_template = row[2]
                ips = row[3]
                login = row[4]
                senha = row[5]
                protocolo = row[6]
                diretorio_remoto = row[7]
                diretorio_mover_remoto = row[8]
                frequencia = row[9]
                prefixo = row[10]
                sufixo = row[11]
                situacao = row[12]
                desc_situacao = row[13]
                observacao = row[14]
                dtapagou = row[15]
                login_apagou = row[16]
                nome_processo = "%s%s" % (nome_banco,codigo)
                procname.setprocname(nome_processo)
                print nome_processo
                proc_pai(ips,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,codigo,nome_banco)

def verifica_inicio():
	os.system("rm .pid.fhs")
        banco = "todos"
        usuario = "danilo"
        servidor = "localhost"
        senha = "danilo123"
        dir_local = "Download/"
        conn = psycopg2.connect(dbname=banco, user=usuario, host=servidor, password=senha)
        cur = conn.cursor()
        cur.execute("""SELECT * from pg_database WHERE datname NOT IN ('postgres','template0','template1')""")
        linhas_database = cur.fetchall()
        for linha_db in linhas_database:
                banco_dados = linha_db[0]
                conn2 = psycopg2.connect(dbname=banco_dados, user=usuario, host=servidor, password='danilo123')
                cur2 = conn2.cursor()
                cur2.execute("SELECT * FROM pg_catalog.pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema', 'pg_toast')")
                lista_tabelas = cur2.fetchall()
                for lista_tb in lista_tabelas:
                        if lista_tb[1].strip() == 'servidor_arquivo':
                                cur2.execute("SELECT * FROM servidor_arquivo")
                                rows = cur2.fetchall()
                                for row in rows:
                                        codigo = row[0]
                                        dtcadastro = row[1]
                                        cod_template = row[2]
                                        ips = row[3]
                                        login = row[4]
                                        senha = row[5]
                                        protocolo = row[6]
                                        diretorio_remoto = row[7]
                                        diretorio_mover_remoto = row[8]
                                        frequencia = row[9]
                                        prefixo = row[10]
                                        sufixo = row[11]
                                        situacao = row[12]
                                        desc_situacao = row[13]
                                        observacao = row[14]
                                        dtapagou = row[15]
                                        login_apagou = row[16]
                                        nome_processo = "%s%s" % (banco_dados,codigo)
                                        procname.setprocname(nome_processo)
                                        proc_pai(ips,login,senha,prefixo,sufixo,diretorio_remoto,diretorio_mover_remoto,dir_local,frequencia,codigo,banco_dados)


if __name__ == '__main__':
	argumento = sys.argv[1]
	if 'start' == argumento:
		verifica_inicio()
	elif 'restart' == argumento:
		nome_banco = sys.argv[2]
		id_tabela = sys.argv[3]
		resultado = [4]
		restart(nome_banco,id_tabela,resultado)

