<?php
require __DIR__ . '/db_sample.php';

$id = (string) ($_POST['id'] ?? $_GET['id'] ?? '');
$fieldName = (string) ($_POST['field_name'] ?? '');
$fieldValue = (string) ($_POST['field_value'] ?? '');
$allowedFields = ['name', 'city', 'address', 'birthday', 'mail'];
$message = '';

if ($id !== '' && in_array($fieldName, $allowedFields, true)) {
    $query = 'UPDATE notebook SET `' . $fieldName . '` = ? WHERE id = ?';
    $statement = mysqli_prepare($conn, $query);
    mysqli_stmt_bind_param($statement, 'si', $fieldValue, $id);
    $message = mysqli_stmt_execute($statement)
        ? 'Запись изменена.'
        : 'Ошибка изменения записи: ' . mysqli_stmt_error($statement);
    mysqli_stmt_close($statement);
}

$result = mysqli_query($conn, 'SELECT id, name, city, address, birthday, mail FROM notebook ORDER BY id');
$rows = mysqli_fetch_all($result, MYSQLI_ASSOC);
$selectedRow = null;
foreach ($rows as $row) {
    if ((string) $row['id'] === $id) {
        $selectedRow = $row;
        break;
    }
}
?>
<!doctype html>
<html lang="ru">
<head><meta charset="UTF-8"><title>ex4.php</title></head>
<body>
<h2>Изменение записи notebook</h2>
<?php if ($message !== ''): ?><p><?= htmlspecialchars($message, ENT_QUOTES, 'UTF-8') ?></p><?php endif; ?>
<p>1. Выберите радиокнопкой строку, которую нужно изменить.</p>
<form method="post" action="ex4.php">
    <table border="1" cellpadding="5">
        <tr><th>Выбор строки (id)</th><th>id</th><th>name</th><th>city</th><th>address</th><th>birthday</th><th>mail</th></tr>
        <?php foreach ($rows as $row): ?>
            <tr>
                <td><input type="radio" name="id" value="<?= (int) $row['id'] ?>"<?= (string) $row['id'] === $id ? ' checked' : '' ?>></td>
                <?php foreach ($row as $value): ?>
                    <td><?= htmlspecialchars((string) ($value ?? ''), ENT_QUOTES, 'UTF-8') ?></td>
                <?php endforeach; ?>
            </tr>
        <?php endforeach; ?>
    </table>
    <?php if ($rows === []): ?>
        <p>Таблица notebook пока пустая. Сначала добавьте записи через ex2.php.</p>
    <?php else: ?>
        <p><button type="submit">Выбрать запись для изменения</button></p>
    <?php endif; ?>
</form>

<?php if ($selectedRow !== null): ?>
    <h3>2. Изменение выбранной строки с id = <?= (int) $selectedRow['id'] ?></h3>
    <p>Выберите поле в выпадающем списке и введите новое значение.</p>
    <form method="post" action="ex4.php">
        <input type="hidden" name="id" value="<?= (int) $selectedRow['id'] ?>">
        <label>Имя поля:
            <select name="field_name">
                <?php foreach ($allowedFields as $field): ?>
                    <option value="<?= $field ?>"><?= $field ?></option>
                <?php endforeach; ?>
            </select>
        </label>
        <label> Новое значение:
            <input type="text" name="field_value">
        </label>
        <button type="submit">Заменить</button>
    </form>
<?php elseif ($rows !== []): ?>
    <p>После выбора радиокнопки нажмите «Выбрать запись для изменения» — тогда
        появятся выпадающий список поля и поле для нового значения.</p>
<?php endif; ?>
<p><a href="ex3.php">Посмотреть результат в ex3.php</a></p>
</body>
</html>
<?php mysqli_free_result($result); mysqli_close($conn); ?>
