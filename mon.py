# -*- coding: utf-8 -*-

import psutil
import time
import sys,subprocess,os

#####################################################################################################
#
# monitor()
# recebe o nome do banco de dados e o codigo da tabela, monta o nome e monitora para ver se
# o processo foi encerrado inesperadamente ou continua ativo. Caso ele tenha sido encerrado
# ele reativa o processo.
#
#####################################################################################################
def monitor(banco, codigo):
        while True:
		while True:
			#### Tempo de espera para consulta se processo está ativo
			time.sleep(15)

			nome = "%s%s" % (banco,codigo)
			#### Pega o PID do processo através do comando ps.
			cmm = "ps -ef | grep '%s' | grep -v 'grep' | awk '{ print $2 }'" % (nome)
			resultado = subprocess.check_output(cmm, shell=True)
			resultado = resultado.strip()
			if resultado != '':
				pid = int(resultado)
				if psutil.pid_exists(pid) == True:
					p = psutil.Process(pid)
					#### Verifica se processo é zumbi ou se ele existe.
					if p.status() == psutil.STATUS_ZOMBIE:
						print("Processo ZOMBIE: %s" % (pid))
					else:
						print("Existe: %s" % (pid))
				else:
					#### Caso ele não exista, ele inicia  novamente o processo.
					print("Processo MORTO: %s" % (pid))
					os.system("python manag.py restart %s %s %s &" % (banco, codigo, pid))
					#break
			else:
				pid = 'iiii'
				os.system("python manag.py restart %s %s %s &" % (banco, codigo, pid))
				break
array_pid = []
banco = sys.argv[1]
codigo = sys.argv[2]
monitor(banco, codigo)
