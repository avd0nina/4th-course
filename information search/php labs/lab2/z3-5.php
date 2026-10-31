<?php
declare(strict_types=1);

function printArray(string $name, array $values): void
{
    echo '<p><strong>' . htmlspecialchars($name, ENT_QUOTES, 'UTF-8') . ':</strong> ';
    echo htmlspecialchars(implode('  ', array_map('strval', $values)), ENT_QUOTES, 'UTF-8');
    echo '</p>';
}

$treug = [];
for ($n = 1; $n <= 10; $n++) {
    $treug[] = intdiv($n * ($n + 1), 2);
}

$kvd = [];
for ($n = 1; $n <= 10; $n++) {
    $kvd[] = $n ** 2;
}

$rez = array_merge($treug, $kvd);
$rezSorted = $rez;
sort($rezSorted);
$rezAfterShift = $rezSorted;
array_shift($rezAfterShift);
$rez1 = array_values(array_unique($rezAfterShift));
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Задание 6</title>
</head>
<body>
    <h2>Операции с массивами</h2>
    <?php
    printArray('$treug', $treug);
    printArray('$kvd', $kvd);
    printArray('$rez после объединения', $rez);
    printArray('$rez после сортировки', $rezSorted);
    printArray('$rez после удаления первого элемента', $rezAfterShift);
    printArray('$rez1 после array_unique()', $rez1);
    ?>
</body>
</html>
