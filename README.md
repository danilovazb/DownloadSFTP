DownloadSFTP
=====

## Descrição ##

Sistema em python para realizar downloads via FTP, SFTP e SCP automáticos em pastas pré-definidas pelo usuário.
Usado para o download automático de arquivos em clientes.

### Atualizações ###
Um sistema simples, mudei algumas coisas no sistema, procurei deixar o código um pouco mais limpo, de fácil entendimento.

## Libs necessárias ##

* paramiko
* flask
* procname
* psycopg2
* pidmon
* psutil
* zipfile
* glob

### Como usar ###

Dentro da pasta SQL, rode o script no banco de dados postgreSQL.
Altere as configurações do banco no arquivo abaixo:

* ~>~/$ dwftp/confs/login_banco.json 

Inicie primeiro o server.py, ele vai dar o start nos processos, a princípio é preciso que já tenha algum processo de download cadastrado no banco para que ele funcione.

```$ python server.py```

Após o servidor inciado, vá até o navegador e entre no link http://localhost:5000/manager/start para iniciar realmente o processo.

Ou caso queira iniciar no terminal, basta seguir o comando abaixo:

```$ python manag.py start```

Ele também funciona da mesma maneira que o webservice.
