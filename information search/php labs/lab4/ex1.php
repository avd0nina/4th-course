<?php
require __DIR__ . '/db_sample.php';

mysqli_query($conn, 'DROP TABLE IF EXISTS notebook');
$query = <<<'SQL'
CREATE TABLE notebook (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    city VARCHAR(50),
    address VARCHAR(50),
    birthday DATE,
    mail VARCHAR(20),
    PRIMARY KEY (id)
)
SQL;

$created = mysqli_query($conn, $query);
?>
<!doctype html>
<html lang="ru">
<head><meta charset="UTF-8"><title>ex1.php</title></head>
<body>
<?php if (!$created): ?>
    <p>Нельзя создать таблицу notebook</p>
    <p><?= htmlspecialchars(mysqli_error($conn), ENT_QUOTES, 'UTF-8') ?></p>
<?php else: ?>
    <p>Таблица notebook создана.</p>
<?php endif; ?>
<p><a href="ex2.php">Перейти к заполнению</a></p>
</body>
</html>
<?php mysqli_close($conn); ?>
