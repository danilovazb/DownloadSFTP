#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
import manag,os,subprocess

app = Flask(__name__)

@app.route('/manager/<status>')
def receita_consultar(status):
	pid = {}
	if status == "start":
		os.system("python manag.py start")
	
        elif "stop" in status:
                stats = []
                stats = status.split(',')
                process = "%s%s" % (stats[1],stats[2])
		cmm = "ps -ef | grep '%s' | grep -v 'grep' | awk '{ print $2 }'" % (process)
		resultado = subprocess.check_output(cmm, shell=True)
		resultado = resultado.strip()
		os.kill(int(resultado.split('\n')[0]),9)
		cmm = "ps -ef | grep 'mon.py %s' | grep -v 'grep' | awk '{ print $2 }'" % (stats[1])
		resultado = subprocess.check_output(cmm, shell=True)
                resultado = resultado.strip()
                os.kill(int(resultado.split('\n')[0]),9)

	elif "restart" in status:
		stats = []
		stats = status.split(',')
		process = "%s%s" % (stats[1],stats[2])
		cmm = "ps -auxf | grep '%s*' | grep -v 'grep' | awk '{ print $2 }'" % (process)
                resultado = subprocess.check_output(cmm, shell=True)
		result = []
		result = resultado.strip().split('\n')
                os.kill(int(result[len(result)-1]),9)
	else:
		print "Comando errado no navegador"

@app.errorhandler(500)
def internal_error(error):
        return "500 error"

@app.errorhandler(404)
def internal_error(error):
        return "404 Not Found"

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000,debug=False)

