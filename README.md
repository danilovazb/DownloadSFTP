DownloadSFTP
=====

## Descrição ##

Sistema em python e PHP para realizar downloads via FTP, SFTP e SCP automáticos em pastas pré-definidas pelo usuário.

## Libs necessárias ##

* paramiko
* flask
* procname
* psycopg2
* pidmon
* psutil

### Como usar ###

Dentro da pasta SQL, rode o script no banco de dados postgreSQL.
Altere as configurações do banco nos arquivos abaixo:

* ~> ftp_format.py - Linhas: 43, 65, 91
* ~> Interface/index.php - Linha: 166
* ~> Interface/class/conect.php - Linhas: 2, 3, 4, 6
* ~> Interface/class/delete.php - Linha: 7
* ~> Interface/class/insert.php - Linha: 17
* ~> manag.py - Linhas: 37-39, 89-92
* ~> sftp_format.py - Linhas: 55, 89

Inicie primeiro o server.py, ele vai dar o start nos processos, a princípio é preciso que já tenha algum processo de download cadastrado no banco para que ele funcione.

```$ python server.py```

Após o servidor inciado, vá até o navegador e entre no link http://localhost:5000/manager/start para iniciar realmente o processo.
