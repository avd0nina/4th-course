<?php
declare(strict_types=1);

$color = 'blue';
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Задание 4</title>
</head>
<body>
    <h2>Таблица сложения 1-10</h2>
    <table border="1" cellpadding="5">
        <tr>
            <td style="color: red;">+</td>
            <?php for ($column = 1; $column <= 10; $column++): ?>
                <td style="color: <?= htmlspecialchars($color, ENT_QUOTES, 'UTF-8') ?>;">
                    <?= $column ?>
                </td>
            <?php endfor; ?>
        </tr>
        <?php for ($row = 1; $row <= 10; $row++): ?>
            <tr>
                <td style="color: <?= htmlspecialchars($color, ENT_QUOTES, 'UTF-8') ?>;">
                    <?= $row ?>
                </td>
                <?php for ($column = 1; $column <= 10; $column++): ?>
                    <td><?= $row + $column ?></td>
                <?php endfor; ?>
            </tr>
        <?php endfor; ?>
    </table>
</body>
</html>
