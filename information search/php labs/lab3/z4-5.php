<?php
declare(strict_types=1);

$list_sites = [
    'https://www.google.com/',
    'https://www.bing.com/',
    'https://duckduckgo.com/',
];
$site = $_POST['site'] ?? null;

if (isset($site) && in_array($site, $list_sites, true)) {
    header('Location: ' . $site);
    exit;
}
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Выбор поисковой системы</title>
</head>
<body>
    <h2>Выберите поисковую систему</h2>
    <form action="<?= htmlspecialchars($_SERVER['PHP_SELF'], ENT_QUOTES, 'UTF-8') ?>" method="post">
        <select name="site">
            <?php $i = 0; while ($i < count($list_sites)): ?>
                <option value="<?= htmlspecialchars($list_sites[$i], ENT_QUOTES, 'UTF-8') ?>">
                    <?= htmlspecialchars($list_sites[$i], ENT_QUOTES, 'UTF-8') ?>
                </option>
            <?php $i++; endwhile; ?>
        </select>
        <button type="submit">Перейти</button>
    </form>
</body>
</html>
