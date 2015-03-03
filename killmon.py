#!/usr/bin/python
import subprocess,os,sys

process = sys.argv[1]
#cmm = "ps -ef | grep '%s' | grep -v 'grep' | awk '{ print $2 }'" % (process)
cmm = "ps -ef | grep '%s' | grep -v 'grep' | grep -v 'killmon.py' | awk '{ print $2 }'" % (process)
resultado = subprocess.check_output(cmm, shell=True)
resultado = resultado.strip()
lista = resultado.split('\n')
for i in range(len(lista)):
        os.kill(int(lista[i]),9)

