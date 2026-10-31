<?php
declare(strict_types=1);

function Ru(string $color): string
{
    return '<span style="color: ' . htmlspecialchars($color, ENT_QUOTES, 'UTF-8') . ';">Здравствуйте!</span>';
}

function En(string $color): string
{
    return '<span style="color: ' . htmlspecialchars($color, ENT_QUOTES, 'UTF-8') . ';">Hello!</span>';
}

function Fr(string $color): string
{
    return '<span style="color: ' . htmlspecialchars($color, ENT_QUOTES, 'UTF-8') . ';">Bonjour!</span>';
}

function De(string $color): string
{
    return '<span style="color: ' . htmlspecialchars($color, ENT_QUOTES, 'UTF-8') . ';">Guten Tag!</span>';
}

$language = (string) ($_GET['lang'] ?? 'Ru');
$color = (string) ($_GET['color'] ?? 'blue');
$allowedLanguages = ['Ru', 'En', 'Fr', 'De'];
$allowedColors = ['black', 'red', 'green', 'blue', 'purple', 'orange'];

if (!in_array($language, $allowedLanguages, true)) {
    $language = 'Ru';
}
if (!in_array(strtolower($color), $allowedColors, true)) {
    $color = 'blue';
}

$lang = $language;
$greeting = $lang($color);
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Задание 5</title>
</head>
<body>
    <p>Результат: <?= $greeting ?></p>
    <p>
        Примеры:
        <a href="?lang=Ru&color=red">Ru</a>,
        <a href="?lang=En&color=blue">En</a>,
        <a href="?lang=Fr&color=green">Fr</a>,
        <a href="?lang=De&color=purple">De</a>
    </p>
</body>
</html>
