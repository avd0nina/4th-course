<?php
require __DIR__ . '/db_sample.php';
$result = mysqli_query($conn, 'SELECT id, name, city, address, birthday, mail FROM notebook ORDER BY id');
?>
<!doctype html>
<html lang="ru">
<head><meta charset="UTF-8"><title>ex3.php</title></head>
<body>
<h2>Все записи таблицы notebook</h2>
<table border="1" cellpadding="5">
    <tr><th>id</th><th>name</th><th>city</th><th>address</th><th>birthday</th><th>mail</th></tr>
    <?php while ($row = mysqli_fetch_assoc($result)): ?>
        <tr>
            <?php foreach ($row as $value): ?>
                <td><?= htmlspecialchars((string) ($value ?? ''), ENT_QUOTES, 'UTF-8') ?></td>
            <?php endforeach; ?>
        </tr>
    <?php endwhile; ?>
</table>
<p><a href="ex2.php">Добавить запись</a> | <a href="ex4.php">Изменить запись</a></p>
</body>
</html>
<?php mysqli_free_result($result); mysqli_close($conn); ?>
