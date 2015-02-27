import requests,sys
arquivo = sys.argv[1]
#url = "http://192.168.2.52/ifclick/teste.php"
url = sys.argv[2]
f = {'ARQUIVO': open(arquivo,'rb')}
v = {'author': 'Danilo'}
r = requests.post(url = url, files = f, data = v)
print r.status_code
print r.headers   
print r.text 
