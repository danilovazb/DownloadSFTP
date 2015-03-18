#! /usr/bin/python
# -*- coding: utf-8 -*-
import paramiko
import psycopg2
import time
import json
import sys,subprocess,os,hashlib,linecache,requests
from datetime import datetime
#global requests
def PrintException():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

def lista_arquivos(ip,portas,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,banco_dados,json_config,id_tabela):
        global sftp
        ultimo_char_dir_remoto = dir_remoto[len(dir_remoto)-1]
        if ultimo_char_dir_remoto != '/':
                dir_remoto = "%s/" % (dir_remoto)
        try:
		# ~~~~~~ Metodo antigo ~~~~~~ #
                #ssh = paramiko.SSHClient()
                #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                #ssh.connect(ip,port=int(portas), username=usuario, password=senha)
		# ~~~~~~ Metodo antigo ~~~~~~ #
		
		transport = paramiko.Transport((ip, int(portas)))
		transport.connect(username = usuario, password = senha)
		sftp = paramiko.SFTPClient.from_transport(transport)
		list_file= sftp.listdir(dir_remoto)
		#print "\n\nConectando no sftp..."
                #print "  \033[1;32m[+]\033[0m IP: %s" % ip
                #print "  \033[1;32m[+]\033[0m PORTA: %s\n" % portas
		#print "\033[1;32m[+]\033[0m Acessando diretório remoto: %s" % dir_remoto
                #stdin, stdout, stderr = ssh.exec_command("ls -la %s" % (dir_remoto))
                #arq_dir_remoto = stdout.readlines()
		#arq_dir_remoto = list_file

		print "\n\nConectando no sftp..."
		print "  \033[1;32m[+]\033[0m IP: %s" % ip
		print "  \033[1;32m[+]\033[0m PORTA: %s\n" % portas
		print "\033[1;32m[+%s+]\033[0m Acessando diretório remoto: %s" % (banco_dados.replace('ifclick_',''),dir_remoto)
		
		arq_dir_remoto = list_file

                for i in range(len(arq_dir_remoto)):
                        val_nome_real = len(arq_dir_remoto[i].split(' '))
                        nome_real = arq_dir_remoto[i].split(' ')[val_nome_real-1]
                        if prefixo in nome_real and sufixo in nome_real:
                                origem = "%s%s" % (dir_remoto,nome_real)
				origem.replace('\'u','')
				origem.replace('\'','')
                                destino = "%s%s/%s" % (dir_local,usuario,nome_real)
				#print "\033[1;32mDEBUG\033[0m %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (origem.strip(),destino.strip(),ip,usuario,senha,dir_mover_remoto,nome_real,dir_local,banco_dados,json_config,id_tabela)
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
		print ex
                arquivoGrava.write("%s-%s-%s %s:%s:%s Log Excetion: Cliente - %s --> ERRO - %s\n" % (str(now.day),\
                                                                                                        str(now.month),\
                                                                                                        str(now.year),\
                                                                                                        str(now.hour),\
                                                                                                        str(now.minute),\
                                                                                                        str(now.second),\
                                                                                                        dir_local,\
                                                                                                        str(ex)))
                raw_credenciais = open('confs/login_banco.json').read()
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
        #print "baixa_arquivos"
        dir_local = "%s%s" % (dir_local, usuario)
        now = datetime.now()
        raw_credenciais = open('confs/login_banco.json').read()
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
                #ftp = ssh.open_sftp() 
                sftp.get(origem, destino)
                #sftp.close()
                dtime = datetime.now()
                dtinicio = "%s-%s-%s %s:%s:%s" % (str(dtime.day),str(dtime.month),str(dtime.year),str(dtime.hour),str(dtime.minute),str(dtime.second))
                ############ Envio POST json_config ANTIGO
                #arquivo = destino
                #data = json.loads(json_config)
                #url = data['arquivo_post']
                #f = {data['tipo_arquivo']: open(arquivo,'rb')}
                #v = data['posts']
                #r = requests.post(url = url, files = f, data = v)
                ##print r.status_code
                ##print r.headers
                ##print r.text
                #dtimefim = datetime.now()
                #dtfim = "%s-%s-%s %s:%s:%s" % (str(dtimefim.day),str(dtimefim.month),str(dtimefim.year),str(dtimefim.hour),str(dtimefim.minute),str(dtimefim.second))

		############ Envio POST
                print "\033[1;34m[+%s+]\033[0m Download do arquivo: %s" % (banco_dados.replace('ifclick_',''),destino)
                arquivo = destino
                data = json.loads(json_config)
                url = data['arquivo_post']
                f = {data['tipo_arquivo']: open(arquivo,'rb')}
                v = data['posts']
                print "\033[1;34m[+%s+]\033[0m Fazendo POST na URL: %s" % (banco_dados.replace('ifclick_',''),url)
                r = requests.post(url = url, files = f, data = v)
                print "\033[1;34m[+%s+]\033[0m Status POST: %s" % (banco_dados.replace('ifclick_',''),r.status_code)
                print "\033[1;34m[+%s+]\033[0m HEADER da pagina de POST: %s" % (banco_dados.replace('ifclick_',''),r.headers)
                print "\033[1;34m[+%s+]\033[0m Retorno da pagina: %s" % (banco_dados.replace('ifclick_',''),r.text)
                dtimefim = datetime.now()
                dtfim = "%s-%s-%s %s:%s:%s" % (str(dtimefim.day),str(dtimefim.month),str(dtimefim.year),str(dtimefim.hour),str(dtimefim.minute),str(dtimefim.second))

                ############ Fim Envio POST


                hasher = hashlib.md5()
                tam_arquivo = os.path.getsize(destino)
                with open(destino, 'rb') as afile:
                        buf = afile.read()
                        hasher.update(buf)
                md5 = hasher.hexdigest()
                tamanho = "%i" % (tam_arquivo)
                #print tamanho
                query.execute("INSERT INTO log_servidor_arquivo (cod_servidor_arquivo,nome, tamanho, md5, dtinicio, dtfim) values ('%s','%s',%s,'%s','%s','%s')" % (id_tabela,nome_real,tamanho,md5,dtinicio,dtfim))
                conecta.commit()
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>> CHEGUEI ATÉ AQUI %s<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" % banco_dados

        else:
                os.makedirs(dir_local, 0755)
                #ftp = ssh.open_sftp() 
                sftp.get(origem, destino)
                #sftp.close()
                ############ Envio POST
                #dtime = datetime.now()
                #dtinicio = "%s-%s-%s %s:%s:%s" % (str(dtime.day),str(dtime.month),str(dtime.year),str(dtime.hour),str(dtime.minute),str(dtime.second))
                #arquivo = destino
                #data = json.loads(json_config)
                #url = data['arquivo_post']
                #f = {data['tipo_arquivo']: open(arquivo,'rb')}
                #v = data['posts']
                #r = requests.post(url = url, files = f, data = v)
                #print r.status_code
                #print r.headers
                #print r.text
                #dtimefim = datetime.now()
                #dtfim = "%s-%s-%s %s:%s:%s" % (str(dtimefim.day),str(dtimefim.month),str(dtimefim.year),str(dtimefim.hour),str(dtimefim.minute),str(dtimefim.second))
                ############ Fim Envio POST

		############ Envio POST
        	print "\033[1;34m[+%s+]\033[0m Download do arquivo: %s" % (banco_dados.replace('ifclick_',''),destino)
                arquivo = destino
                data = json.loads(json_config)
                url = data['arquivo_post']
                f = {data['tipo_arquivo']: open(arquivo,'rb')}
                v = data['posts']
                print "\033[1;34m[+%s+]\033[0m Fazendo POST na URL: %s" % (banco_dados.replace('ifclick_',''),url)
                r = requests.post(url = url, files = f, data = v)
                print "\033[1;34m[+%s+]\033[0m Status POST: %s" % (banco_dados.replace('ifclick_',''),r.status_code)
                print "\033[1;34m[+%s+]\033[0m HEADER da pagina de POST: %s" % (banco_dados.replace('ifclick_',''),r.headers)
                print "\033[1;34m[+%s+]\033[0m Retorno da pagina: %s" % (banco_dados.replace('ifclick_',''),r.text)
                dtimefim = datetime.now()
                dtfim = "%s-%s-%s %s:%s:%s" % (str(dtimefim.day),str(dtimefim.month),str(dtimefim.year),str(dtimefim.hour),str(dtimefim.minute),str(dtimefim.second))
                ############ Fim Envio POST


                hasher = hashlib.md5()
                tam_arquivo = os.path.getsize(destino)
                with open(destino, 'rb') as afile:
                        buf = afile.read()
                        hasher.update(buf)
                md5 = hasher.hexdigest()
                tamanho = "%i" % (tam_arquivo)
                #print tamanho
		query.execute("INSERT INTO log_servidor_arquivo (cod_servidor_arquivo,nome, tamanho, md5, dtinicio, dtfim) values ('%s','%s',%s,'%s','%s','%s')" % (id_tabela,nome_real,tamanho,md5,dtinicio,dtfim))
                conecta.commit()

	try:
        	if dir_mover_remoto == None or dir_mover_remoto == '':
			print "Removendo: %s" % origem
			sftp.remove(origem)
	        else:
			dir_mover_remoto = "%s%s" % (dir_mover_remoto,destino.split('/')[2])
			print "\033[5;31mDIRETORIO PARA MOVER>>> %s >>>>\033[0m %s" % (banco_dados,dir_mover_remoto)
			sftp.rename(origem,dir_mover_remoto)
	except Exception as ex:
		print ex
			
def processa(ip,portas,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,tempo,banco_dados,json_config,id_tabela):
        while True:
                time.sleep(tempo)
                lista_arquivos(ip,portas,usuario,senha,prefixo,sufixo,dir_remoto,dir_mover_remoto,dir_local,banco_dados,json_config,id_tabela)



