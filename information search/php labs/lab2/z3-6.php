<?php
declare(strict_types=1);

function printAssociativeArray(string $title, array $values): void
{
    echo '<h3>' . htmlspecialchars($title, ENT_QUOTES, 'UTF-8') . '</h3>';
    echo '<pre>';
    foreach ($values as $key => $value) {
        echo htmlspecialchars((string) $key, ENT_QUOTES, 'UTF-8')
            . ' => '
            . htmlspecialchars((string) $value, ENT_QUOTES, 'UTF-8')
            . "\n";
    }
    echo '</pre>';
}

$cust = [
    'cnum' => 2001,
    'cname' => 'Hoffman',
    'city' => 'London',
    'snum' => 1001,
    'rating' => 100,
];

$byValues = $cust;
asort($byValues);

$byKeys = $cust;
ksort($byKeys);

$usingSort = $cust;
sort($usingSort);
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Задание 7</title>
</head>
<body>
    <h2>Ассоциативный массив $cust</h2>
    <?php
    printAssociativeArray('1. Исходный массив с ключами', $cust);
    printAssociativeArray('2. Сортировка по значениям (asort)', $byValues);
    printAssociativeArray('3. Сортировка по ключам (ksort)', $byKeys);
    printAssociativeArray('4. Сортировка функцией sort()', $usingSort);
    ?>
</body>
</html>
