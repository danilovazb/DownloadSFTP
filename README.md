DownloadSFTP
=====

## Descrição ##

Sistema em python para realizar downloads via FTP, SFTP e SCP automáticos em pastas pré-definidas pelo usuário.
Usado para o download automático de arquivos em clientes.

### Atualizações ###
Um sistema simples, mudei algumas coisas para tentar facilitar ainda mais, procurei deixar o código um pouco mais limpo, de fácil entendimento. Acrescentei também o envio de e-mail caso tenha algum erro, ainda há bugs para arrumar já que esse sistema é meio que feio sob medida para o que uso hoje, mas da pra ser facilmente adaptado para qualquer um que queira um sistema de downloads automaticos.

Se repararem no código do sftp e ftp, eu faço um POST em uma pagina PHP, ele server para enviar os arquivos para um sistema de processamento dos mesmos, basta comentar onde ele faz essa requisição.

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

Iniciar no terminal, basta seguir o comando abaixo:

```$ python manag.py -s start```
