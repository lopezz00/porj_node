<?php

include_once('db_config.php');
$name_new_lab=$_POST['name_new_lab'];
$description_lab=$_POST['description_lab'];

echo "Les dades son: <br>";
echo "$name_new_lab,$description_lab";

    $conectar=conn();
    $sql="INSERT INTO LABS (nom_lab,descripcio) VALUES ('$name_new_lab','$description_lab')";
    $resul = mysqli_query($conectar, $sql) or trigger_error("Query fallada! SQL - Error: ".mysqli_error($conectar), E_USER_ERROR);
    echo "$sql";
?>