<?php
declare(strict_types=1);

$allowedAlign = ['left', 'center', 'right'];
$allowedValign = ['top', 'middle', 'bottom'];
$align = (string) ($_GET['align'] ?? 'left');
$valign = (string) ($_GET['valign'] ?? 'top');

if (!in_array($align, $allowedAlign, true)) {
    $align = 'left';
}
if (!in_array($valign, $allowedValign, true)) {
    $valign = 'top';
}
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Задание 1 - результат</title>
</head>
<body>
    <table border="1" width="100" height="100">
        <tr>
            <td align="<?= htmlspecialchars($align, ENT_QUOTES, 'UTF-8') ?>"
                valign="<?= htmlspecialchars($valign, ENT_QUOTES, 'UTF-8') ?>">
                Текст
            </td>
        </tr>
    </table>
    <p><a href="z4-1a.htm">Назад</a></p>
</body>
</html>
