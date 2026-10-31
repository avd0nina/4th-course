<?php
require __DIR__ . '/db_sample.php';

$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim((string) ($_POST['name'] ?? ''));
    $city = trim((string) ($_POST['city'] ?? ''));
    $address = trim((string) ($_POST['address'] ?? ''));
    $birthday = trim((string) ($_POST['birthday'] ?? ''));
    $mail = trim((string) ($_POST['mail'] ?? ''));

    if ($name !== '' && $mail !== '') {
        $statement = mysqli_prepare($conn, 'INSERT INTO notebook (name, city, address, birthday, mail) VALUES (?, ?, ?, ?, ?)');
        mysqli_stmt_bind_param($statement, 'sssss', $name, $city, $address, $birthday, $mail);
        $message = mysqli_stmt_execute($statement)
            ? 'Запись добавлена.'
            : 'Ошибка добавления записи: ' . mysqli_stmt_error($statement);
        mysqli_stmt_close($statement);
    } else {
        $message = 'Поля name и mail обязательны для заполнения.';
    }
}
?>
<!doctype html>
<html lang="ru">
<head><meta charset="UTF-8"><title>ex2.php</title></head>
<body>
<h2>Добавление записи в notebook</h2>
<?php if ($message !== ''): ?><p><?= htmlspecialchars($message, ENT_QUOTES, 'UTF-8') ?></p><?php endif; ?>
<form method="post" action="ex2.php">
    <p>Имя: <input type="text" name="name"></p>
    <p>Город: <input type="text" name="city"></p>
    <p>Адрес: <input type="text" name="address"></p>
    <p>Дата рождения: <input type="text" name="birthday" placeholder="YYYY-MM-DD"></p>
    <p>E-mail: <input type="text" name="mail"></p>
    <button type="submit">Добавить</button>
</form>
<p><a href="ex3.php">Посмотреть все записи</a></p>
</body>
</html>
<?php mysqli_close($conn); ?>
