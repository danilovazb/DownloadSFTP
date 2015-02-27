import requests,sys,json
json_data = open('json.json','r').read()
data = json.loads(json_data)
url = data['arquivo_post']
arquivo = "ENVIA.csv"
f = {data['tipo_arquivo']: open(arquivo,'rb')}
v = data['posts']
r = requests.post(url = url, files = f, data = v)
print r.status_code
print r.headers
print r.text

