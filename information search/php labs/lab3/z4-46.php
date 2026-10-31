<?php
declare(strict_types=1);

$user = trim((string) ($_POST['user'] ?? ''));
$hobby = $_POST['hobby'] ?? [];
$hobby = is_array($hobby) ? $hobby : [$hobby];
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Листинг 10-6</title>
</head>
<body>
    <h2>Обработка массива POST</h2>
    <form action="z4-46.php" method="post">
        <p>Ваше имя: <input type="text" name="user" required></p>
        <p>Ваши увлечения:</p>
        <label><input type="checkbox" name="hobby[]" value="чтение"> чтение</label>
        <label><input type="checkbox" name="hobby[]" value="спорт"> спорт</label>
        <label><input type="checkbox" name="hobby[]" value="музыка"> музыка</label>
        <label><input type="checkbox" name="hobby[]" value="туризм"> туризм</label>
        <p><button type="submit">Показать POST-массив</button></p>
    </form>
    <?php foreach ($_POST as $key => $value): ?>
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
    <p><a href="z4-46.php">Назад к форме</a></p>
</body>
</html>
