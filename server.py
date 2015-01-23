from flask import Flask
import json
from flask import jsonify
import manag,os,subprocess

app = Flask(__name__)

#####################################################################################################
#
# Inicia a configuração e os parametros que sera recebido da pagina web
#
#####################################################################################################
@app.route('/manager/<status>')
def receita_consultar(status):
	pid = {}
	#### Caso receba start, inicia o processo
	if status == "start":
		os.system("python manag.py start")
	
	#### Caso receba stop, pega o processo e dá um kill -9
        elif "stop" in status:
                stats = []
                stats = status.split(',')
                process = "%s%s" % (stats[1],stats[2])
		cmm = "ps -ef | grep '%s' | awk '{ print $2 }'" % (process)
		resultado = subprocess.check_output(cmm, shell=True)
		resultado = resultado.strip()
		os.kill(int(resultado.split('\n')[0]),9)

	#### Praticamente o mesmo que o stop, mas ele restarta o processo todo
	#### pega o pid do processo, mata ele e inicia um novo com base no
	#### anterior.
	elif "restart" in status:
		stats = []
		stats = status.split(',')
		process = "%s%s" % (stats[1],stats[2])
		cmm = "ps -auxf | grep '%s*' | awk '{ print $2 }'" % (process)
                resultado = subprocess.check_output(cmm, shell=True)
		result = []
		result = resultado.strip().split('\n')
                os.kill(int(result[len(result)-1]),9)
		banco = stats[1].strip()
		id_tab = stats[2].strip()
		os.system("python manag.py restart %s %s %s" % (banco, id_tab, resultado.strip()))
	else:
		print "Comando errado no navegador"

#####################################################################################################
#
# Caso tenha erro 500 ele atribui essa página de erro
#
#####################################################################################################
@app.errorhandler(500)
def internal_error(error):
        return "500 error"

#####################################################################################################
# 
# Caso tenha erro 404 ele atribui essa página de erro
#
#####################################################################################################
@app.errorhandler(404)
def internal_error(error):
        return "<img src='http://404-found.ru/wp-content/uploads/2011/02/404-2.png' alt='Smiley face'>"

#####################################################################################################
# 
# Inicia o servidor
#
#####################################################################################################
if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000,debug=False)

