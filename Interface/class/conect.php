<?php
$servidor = "localhost";
$usuario = "postgres";
$senha ="danilo123";

$conexao = pg_connect("host=localhost port=5432 dbname=todos user=postgres password=danilo123") or die ("Não foi possivel conectar ao servidor PostGreSQL\n\n");
echo "Conexão efetuada com sucesso!!\n\n\n";

?>
