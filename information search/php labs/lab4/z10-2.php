<?php
$structure = $_GET['structure'] ?? [];
$content = $_GET['content'] ?? [];
$structure = is_array($structure) ? $structure : [$structure];
$content = is_array($content) ? $content : [$content];

require __DIR__ . '/z10-4.inc';
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Результаты поиска по базе study</title>
<?php require __DIR__ . '/z10-3.inc'; ?>
<h2>Поиск по базе данных study</h2>
<?php
require __DIR__ . '/z10-5.inc';

if (!empty($structure)) {
    foreach ($structure as $table) {
        vid_structure($conn, (string) $table);
    }
}

if (!empty($content)) {
    foreach ($content as $table) {
        vid_content($conn, (string) $table);
    }
}

require __DIR__ . '/z10-6.inc';
?>
</body>
</html>
