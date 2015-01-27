<!DOCTYPE html>
<html lang="en">
  <head>

<?php
include('class/conect.php'); 
?>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>Tabela</title>

    <!-- Bootstrap core CSS -->
    <link href="dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="starter-template.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="../../assets/js/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#"></a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>
<br><br><br>
    <div class="container">

      <div class="starter-template">
        <h3>Insert</h3>
	<form class="navbar-form navbar-left" action="class/insert.php" method="post">
	  <div class="form-group">
	    <input name="ip" type="text" class="form-control" placeholder="IP">
	    <input name="login" type="text" class="form-control" placeholder="LOGIN DO SERVIDOR">
	    <input name="senha" type="password" class="form-control" placeholder="SENHA DO SERVIDOR">
	    <input name="protocolo" type="text" class="form-control" placeholder="sftp, ssh, ftp">
	    <input name="diretorio_remoto" type="text" class="form-control" placeholder="DIRETORIO REMOTO">
	    <input name="diretorio_mover_remoto" type="text" class="form-control" placeholder="DIRETORIO PARA MOVER ARQUIVOS">
            <input name="frequencia" type="text" class="form-control" placeholder="TEMPO DE CONSULTA">
            <input name="prefixo" type="text" class="form-control" placeholder="PREFIXO">
            <input name="sufixo" type="text" class="form-control" placeholder="SUFIXO">
            <input name="situacao" type="text" class="form-control" placeholder="SITUACAO">
            <input name="descricao" type="text" class="form-control" placeholder="DESC">
            <input name="observacao" type="text" class="form-control" placeholder="OBSERVACAO">	
   	    <select class="form-control" name="banco_dados">
	    <option selected value="Selecione">Selecione o banco</option>
	<?php
	$result=pg_query($conexao, "SELECT * from pg_database WHERE datname NOT IN ('postgres','template0','template1')");
	  if  (!$result) {
	   echo "Não foi possível executar a consulta";
	  }
	  else
	   {
	    /* Retonar um array associativo correspondente a cada linha da tabela */
	     while($consulta = pg_fetch_assoc($result))
	     { 
		echo "<option value='".$consulta['datname']."'>".$consulta['datname']."</option>";
	     }

	   }

	?>
	</select>
<br><br>
	  </div>
	  <button type="submit" class="btn btn-default">Insert</button>
	</form>

      </div>

    </div><!-- /.container -->

    <div class="container">

      <div class="starter-template">
        <h3>Delete</h3>
        <form class="navbar-form navbar-left" action="class/delete.php" method="post">
          <div class="form-group">
            <input name="id" type="text" class="form-control" placeholder="ID">
	     <select class="form-control" name="banco_dados">
            <option selected value="Selecione">Selecione o banco</option>
        <?php
        $result=pg_query($conexao, "SELECT * from pg_database WHERE datname NOT IN ('postgres','template0','template1')");
          if  (!$result) {
           echo "Não foi possível executar a consulta";
          }
          else
           {
            /* Retonar um array associativo correspondente a cada linha da tabela */
             while($consulta = pg_fetch_assoc($result))
             {
                echo "<option value='".$consulta['datname']."'>".$consulta['datname']."</option>";
             }

           }

        ?>
        </select>
          </div>
          <button type="submit" class="btn btn-default">Delete</button>
        </form>

      </div>

    </div><!-- /.container -->


<div class="bs-example" data-example-id="striped-table">
    <table class="table table-striped">
      <thead>
        <tr>
          <th>#</th>
          <th>IP</th>
          <th>LOGIN</th>
	  <th>SENHA</th>
	  <th>PROTOCOLO</th>
	  <th>DIR REMOTO</th>
	  <th>FREQ</th>
	  <th>SUFIXO</th>
	  <th>PREFIXO</th>
	  <th>BANCO DADOS</th>
        </tr>
      </thead>
      <tbody>
<?php
$result=pg_query($conexao, "SELECT * from pg_database WHERE datname NOT IN ('postgres','template0','template1')");
          if  (!$result) {
           echo "Não foi possível executar a consulta";
          }
          else
           {
            /* Retonar um array associativo correspondente a cada linha da tabela */
             while($consulta = pg_fetch_assoc($result))
             {
$banco_dados = $consulta['datname'];
$vai = pg_connect("host=localhost port=5432 dbname=$banco_dados user=postgres password=danilo123");
$result2=pg_query($vai, "SELECT * FROM servidor_arquivo;");
  if  (!$result2) {
   //echo "Não foi possível executar a consulta $consulta";
  }
  else
   {
    /* Retonar um array associativo correspondente a cada linha da tabela */
     while($consulta2 = pg_fetch_assoc($result2))
     {     
       	echo "<tr>";
       	echo "<th scope='row'>" . $consulta2['codigo'] . "</th>";
       	echo "<td>".$consulta2['ips']."</td>";
       	echo "<td>".$consulta2['login']."</td>";
	echo "<td>".$consulta2['pass']."</td>";
	echo "<td>".$consulta2['protocolo']."</td>";
	echo "<td>".$consulta2['diretorio_remoto']."</td>";
	echo "<td>".$consulta2['frequencia']."</td>";
	echo "<td>".$consulta2['prefixo']."</td>";
	echo "<td>".$consulta2['sufixo']."</td>";
	echo "<td>".$banco_dados."</td>";
       	echo "</tr>";
     }

     pg_close($conexao);
   } 
}}
?>
</tbody>
    </table>
  </div><!-- /example -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="dist/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>

