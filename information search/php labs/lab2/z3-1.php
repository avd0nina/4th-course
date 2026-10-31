<?php
declare(strict_types=1);

$color = 'silver';
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Задание 3</title>
</head>
<body>
    <h2>Таблица Пифагора 10 × 10</h2>
    <table border="1" cellpadding="5">
        <?php $row = 1; while ($row <= 10): ?>
            <tr>
                <?php $column = 1; while ($column <= 10): ?>
                    <?php $isDiagonal = $row === $column; ?>
                    <td<?= $isDiagonal
                        ? ' style="background-color: ' . htmlspecialchars($color, ENT_QUOTES, 'UTF-8') . ';"'
                        : '' ?>><?= $row * $column ?></td>
                <?php $column++; endwhile; ?>
            </tr>
        <?php $row++; endwhile; ?>
    </table>
</body>
</html>
