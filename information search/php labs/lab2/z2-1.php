<?php
declare(strict_types=1);

$color = 'blue';
$size = 24;
$text = 'Это строка текста, выведенная заданными цветом и размером.';
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Задание 1</title>
</head>
<body>
    <p style="color: <?= htmlspecialchars($color, ENT_QUOTES, 'UTF-8') ?>; font-size: <?= $size ?>px;">
        <?= htmlspecialchars($text, ENT_QUOTES, 'UTF-8') ?>
    </p>
</body>
</html>
