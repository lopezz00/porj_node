<?php

include_once('db_config.php');
$correu_new_user=$_POST['correu_new_user'];
$name_new_user=$_POST['name_new_user'];
$surname_new_user=$_POST['surname_new_user'];
$second_surname_new_user=$_POST['second_surname_new_user'];
$password=$_POST['password'];
$rol=$_POST['rol'];
$rfid_value=$_POST['rfid_value'];

echo "Les dades son: <br>";
echo "$correu_new_user,$name_new_user,$rfid_value";

    $conectar=conn();
    $sql="INSERT INTO USUARIS (email,nom,cognom1,cognom2,password,rol,rfid_value) VALUES ('$correu_new_user','$name_new_user', '$surname_new_user', '$second_surname_new_user', '$password', '$rol', '$rfid_value')";
    $resul = mysqli_query($conectar, $sql) or trigger_error("Query fallada! SQL - Error: ".mysqli_error($conectar), E_USER_ERROR);
    echo "$sql";
?>