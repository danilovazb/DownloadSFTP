<?php

 include('conect.php'); // Include the connection to the databank THEN start your SQL Job :)

$result=pg_query($conexao, "SELECT * FROM cliente;");
  if  (!$result) {
   echo "Não foi possível executar a consulta";
  }
  else
   {
   #  $query = "select * from cliente";
    
    

   #  $result = pg_query($conexao, $query);

    /* Retonar um array associativo correspondente a cada linha da tabela */
     while($consulta = pg_fetch_assoc($result))
     {
       print "ID: " .$consulta['id'] . " - ";
       print "NOME: ".$consulta['nome']." - ";
       print "EMAIL: ".$consulta['email']."\n";
     }
    
     pg_close($conexao);
   }

?> 
