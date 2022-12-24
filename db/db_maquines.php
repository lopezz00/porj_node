<?php

include_once('db_config.php');
$name_new_machine=$_POST['name_new_machine'];
$description_machine=$_POST['description_machine'];
$name_lab=$_POST['name_lab'];

    $conectar=conn();
    $sql="INSERT INTO MAQUINES (nom_maquina,descripcio,nom_lab) VALUES ('$name_new_machine','$description_machine','$name_lab')";
    $resul = mysqli_query($conectar, $sql) or trigger_error("Query fallada! SQL - Error: ".mysqli_error($conectar), E_USER_ERROR);

mysqli_close($conectar)
?>