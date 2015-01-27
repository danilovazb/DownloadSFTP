<?php

$ip = $_POST['ip'];
$login = $_POST['login'];
$senha = $_POST['senha'];
$protocolo = $_POST['protocolo'];
$diretorio_remoto = $_POST['diretorio_remoto'];
$diretorio_mover_remoto = $_POST['diretorio_mover_remoto'];
$frequencia = $_POST['frequencia'];
$prefixo = $_POST['prefixo'];
$sufixo = $_POST['sufixo'];
$situacao = $_POST['situacao'];
$descricao = $_POST['descricao'];
$observacao = $_POST['observacao'];
$banco_dados = $_POST['banco_dados'];
//perform the insert using pg_query
$conexao = pg_connect("host=localhost port=5432 dbname=$banco_dados user=postgres password=danilo123") or die ("Não foi possivel conectar ao servidor PostGreSQL\n\n");
$result = pg_query($conexao, "INSERT INTO servidor_arquivo (ips, login, pass, protocolo, diretorio_remoto, diretorio_mover_remoto, frequencia, prefixo, sufixo, situacao, desc_situacao, observacao ) 
VALUES('$ip', '$login','$senha','$protocolo','$diretorio_remoto','$diretorio_mover_remoto','$frequencia','$prefixo','$sufixo','$situacao','$descricao','$observacao');");

header("Location: http://127.0.0.1/OLD/insert-select-PostgreSQL/");
die();

?>
