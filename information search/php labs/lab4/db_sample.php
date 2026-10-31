<?php
mysqli_report(MYSQLI_REPORT_OFF);

$conn = mysqli_connect('localhost', 'root', 'root', '', 8889);
if (!$conn) {
    die('Нельзя подключиться к MySQL: ' . htmlspecialchars(mysqli_connect_error(), ENT_QUOTES, 'UTF-8'));
}

mysqli_set_charset($conn, 'utf8mb4');
if (!mysqli_query($conn, 'CREATE DATABASE IF NOT EXISTS `sample` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')) {
    die('Нельзя создать базу sample: ' . htmlspecialchars(mysqli_error($conn), ENT_QUOTES, 'UTF-8'));
}
if (!mysqli_select_db($conn, 'sample')) {
    die('Нельзя выбрать базу sample: ' . htmlspecialchars(mysqli_error($conn), ENT_QUOTES, 'UTF-8'));
}
?>
