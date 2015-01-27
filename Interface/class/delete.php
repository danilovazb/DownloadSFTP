<?php

//include('conect.php'); // Include the connection to the databank THEN start your SQL Job :)
$id = $_POST['id'];
$banco_dados = $_POST['banco_dados'];
//perform the insert using pg_query
$conexao = pg_connect("host=localhost port=5432 dbname=$banco_dados user=postgres password=danilo123") or die ("Não foi possivel conectar ao servidor PostGreSQL\n\n");
$result = pg_query($conexao, "delete from servidor_arquivo where codigo = $id;");

header("Location: http://127.0.0.1/OLD/insert-select-PostgreSQL/");
die();

?>
