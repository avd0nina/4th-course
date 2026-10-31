<?php
mysqli_report(MYSQLI_REPORT_OFF);

$db_host = 'localhost';
$db_user = 'root';
$db_password = 'root';
$db_name = 'study';
$db_port = 8889;

$conn = mysqli_connect($db_host, $db_user, $db_password, $db_name, $db_port);
if (!$conn) {
    die('Нельзя подключиться к базе study: ' . htmlspecialchars(mysqli_connect_error(), ENT_QUOTES, 'UTF-8'));
}

mysqli_set_charset($conn, 'utf8mb4');
?>
