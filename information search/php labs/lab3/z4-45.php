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
    <title>Листинг 10-5</title>
</head>
<body>
    <h2>Обработка данных формы</h2>
    <?php if ($_SERVER['REQUEST_METHOD'] === 'POST'): ?>
        <p><?= htmlspecialchars($user !== '' ? $user : 'Гость', ENT_QUOTES, 'UTF-8') ?>, вы увлекаетесь:</p>
        <ul>
            <?php foreach ($hobby as $value): ?>
                <li><?= htmlspecialchars((string) $value, ENT_QUOTES, 'UTF-8') ?></li>
            <?php endforeach; ?>
        </ul>
    <?php endif; ?>
    <form action="z4-45.php" method="post">
        <p>Ваше имя: <input type="text" name="user" required></p>
        <p>Ваши увлечения:</p>
        <label><input type="checkbox" name="hobby[]" value="чтение"> чтение</label>
        <label><input type="checkbox" name="hobby[]" value="спорт"> спорт</label>
        <label><input type="checkbox" name="hobby[]" value="музыка"> музыка</label>
        <label><input type="checkbox" name="hobby[]" value="туризм"> туризм</label>
        <p><button type="submit">Показать</button></p>
    </form>
</body>
</html>
