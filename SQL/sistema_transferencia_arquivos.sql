CREATE TABLE servidor_arquivo
(
        codigo serial NOT NULL PRIMARY KEY,
	dtcadastro timestamp DEFAULT current_timestamp NOT NULL,
	cod_template integer, -- REFERENCES template(codigo),
	ips varchar(100) NOT NULL,
	login varchar(20) NOT NULL, 
	pass varchar(20) NOT NULL, 
	protocolo varchar(20) NOT NULL DEFAULT 'ftp', --sftp,ftp
	diretorio_remoto varchar(255) NOT NULL DEFAULT '', 
	diretorio_mover_remoto varchar(255), 
	frequencia integer NOT NULL DEFAULT 1,--Minuto 
	prefixo varchar(20),--.xml|.csv
	sufixo varchar(20),--.xml|.csv
	situacao varchar(50) NOT NULL DEFAULT 'OFFLINE', 
	desc_situacao varchar(255), 
	observacao text,
	dtapagou timestamp NOT NULL DEFAULT '1970-01-01 00:00:00',
	login_apagou varchar(20)
);
CREATE TABLE log_servidor_arquivo
(
        codigo serial NOT NULL PRIMARY KEY,
	cod_servidor_arquivo integer NOT NULL REFERENCES servidor_arquivo(codigo),
	dtcadastro timestamp DEFAULT current_timestamp NOT NULL,
	dtinicio timestamp NOT NULL,
	dtfim timestamp NOT NULL,
        nome varchar(255) NOT NULL,
        tamanho integer NOT NULL,
	md5 varchar(50) NOT NULL, 
	total_registros integer NOT NULL DEFAULT 0,
	total_processados integer NOT NULL DEFAULT 0,
	qtd_email integer NOT NULL DEFAULT 0, 
	qtd_sms integer NOT NULL DEFAULT 0,  
	qtd_fax integer NOT NULL DEFAULT 0
);
