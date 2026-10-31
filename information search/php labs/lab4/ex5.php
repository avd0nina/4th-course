<?php
require __DIR__ . '/db_sample.php';

$queries = [
    "INSERT INTO notebook (name, city, address, birthday, mail) VALUES ('Анна', 'Москва', 'ул. Ленина, 1', '2000-01-15', 'anna@example.com')",
    "INSERT INTO notebook (name, city, address, birthday, mail) VALUES ('Борис', 'Новосибирск', 'ул. Советская, 2', '1999-05-20', 'boris@example.com')",
    "INSERT INTO notebook (name, city, address, birthday, mail) VALUES ('Вера', 'Омск', 'ул. Мира, 3', '2001-10-10', 'vera@example.com')",
];

$success = true;
foreach ($queries as $query) {
    if (!mysqli_query($conn, $query)) {
        $success = false;
        $error = mysqli_error($conn);
        break;
    }
}
?>
<!doctype html>
<html lang="ru">
<head><meta charset="UTF-8"><title>ex5.php</title></head>
<body>
<?php if ($success): ?>
    <p>Три записи добавлены в таблицу notebook.</p>
<?php else: ?>
    <p>Ошибка добавления записей: <?= htmlspecialchars($error, ENT_QUOTES, 'UTF-8') ?></p>
<?php endif; ?>
<p><a href="ex3.php">Посмотреть таблицу notebook</a></p>
</body>
</html>
<?php mysqli_close($conn); ?>
