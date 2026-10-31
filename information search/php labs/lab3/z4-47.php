<?php
declare(strict_types=1);

$params = $_SERVER['REQUEST_METHOD'] === 'POST' ? $_POST : $_GET;
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Листинг 10-7</title>
</head>
<body>
    <h2>Определение метода передачи данных</h2>
    <p>Использован метод: <?= htmlspecialchars($_SERVER['REQUEST_METHOD'], ENT_QUOTES, 'UTF-8') ?></p>
    <?php foreach ($params as $key => $value): ?>
        <?php if (is_array($value)): ?>
            <p><strong><?= htmlspecialchars((string) $key, ENT_QUOTES, 'UTF-8') ?>:</strong></p>
            <ul>
                <?php foreach ($value as $item): ?>
                    <li><?= htmlspecialchars((string) $item, ENT_QUOTES, 'UTF-8') ?></li>
                <?php endforeach; ?>
            </ul>
        <?php else: ?>
            <p><strong><?= htmlspecialchars((string) $key, ENT_QUOTES, 'UTF-8') ?>:</strong>
                <?= htmlspecialchars((string) $value, ENT_QUOTES, 'UTF-8') ?></p>
        <?php endif; ?>
    <?php endforeach; ?>
    <form action="z4-47.php" method="get">
        <input type="text" name="user" value="guest">
        <label><input type="checkbox" name="hobby[]" value="чтение" checked> чтение</label>
        <label><input type="checkbox" name="hobby[]" value="спорт"> спорт</label>
        <button type="submit">Отправить GET</button>
    </form>
    <form action="z4-47.php" method="post">
        <input type="text" name="user" value="guest">
        <label><input type="checkbox" name="hobby[]" value="музыка" checked> музыка</label>
        <label><input type="checkbox" name="hobby[]" value="туризм"> туризм</label>
        <button type="submit">Отправить POST</button>
    </form>
</body>
</html>
