# -*- coding: utf-8 -*-

import psutil
import time
import sys,subprocess,os

def printMSGNEGATIVA(string):
	sys.stdout.write("\033[1;33m[-]\033[0m")
	for i in range(len(string)):
		sys.stdout.write("%s" % string[i])
		sys.stdout.flush()
		time.sleep(0.01)

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
                                        printMSGNEGATIVA("Processo MORTO: %s" % (pid))
                                        os.system("python manag.py -s restart --bd %s --id %s &" % (banco, codigo))
                        else:
                                pid = 'iiii'
                                os.system("python manag.py -s restart --bd %s --id %s &" % (banco, codigo ))
                                break
array_pid = []
banco = sys.argv[1]
codigo = sys.argv[2]
monitor(banco, codigo)

