# -*- coding: utf-8 -*-

import psutil
import time
import sys,subprocess,os

def monitor(banco, codigo):
        while True:
		while True:
			time.sleep(15)
			nome = "%s%s" % (banco,codigo)
			cmm = "ps -ef | grep '%s' | grep -v 'grep' | awk '{ print $2 }'" % (nome)
			resultado = subprocess.check_output(cmm, shell=True)
			resultado = resultado.strip()
			if resultado != '':
				pid = int(resultado)
				if psutil.pid_exists(pid) == True:
					p = psutil.Process(pid)
					if p.status() == psutil.STATUS_ZOMBIE:
						print("Processo ZOMBIE: %s" % (pid))
					else:
						#print("Existe: %s" % (pid))
						sopranaoficarvazio = '1'
				else:
					print("Processo MORTO: %s" % (pid))
					os.system("python manag.py restart %s %s %s &" % (banco, codigo, pid))
			else:
				pid = 'iiii'
				os.system("python manag.py restart %s %s %s &" % (banco, codigo, pid))
				break
array_pid = []
banco = sys.argv[1]
codigo = sys.argv[2]
monitor(banco, codigo)
