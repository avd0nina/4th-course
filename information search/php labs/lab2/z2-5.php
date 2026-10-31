<?php
declare(strict_types=1);

$lang = strtolower(trim((string) ($_GET['lang'] ?? '')));

if ($lang === 'ru') {
    $languageName = 'русский';
} elseif ($lang === 'en') {
    $languageName = 'английский';
} elseif ($lang === 'fr') {
    $languageName = 'французский';
} elseif ($lang === 'de') {
    $languageName = 'немецкий';
} else {
    $languageName = 'язык неизвестен';
}
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Задание 2</title>
</head>
<body>
    <p>Результат: <?= htmlspecialchars($languageName, ENT_QUOTES, 'UTF-8') ?></p>
    <p>
        Проверка:
        <a href="?lang=ru">ru</a>,
        <a href="?lang=en">en</a>,
        <a href="?lang=fr">fr</a>,
        <a href="?lang=de">de</a>,
        <a href="?lang=xx">xx</a>
    </p>
</body>
</html>
