<?php
function validStudyTable(string $table): bool
{
    return in_array($table, ['sal', 'cust', 'ord'], true);
}

function vid_structure(mysqli $conn, string $table): void
{
    if (!validStudyTable($table)) {
        return;
    }

    echo '<h4>Структура таблицы ' . htmlspecialchars($table, ENT_QUOTES, 'UTF-8') . '</h4>';
    $result = mysqli_query($conn, 'DESCRIBE `' . $table . '`');
    if (!$result) {
        echo '<p>Ошибка получения структуры таблицы.</p>';
        return;
    }

    echo '<table border="1" cellpadding="5">';
    echo '<tr><th>Field</th><th>Type</th><th>Null</th><th>Key</th><th>Default</th><th>Extra</th></tr>';
    while ($row = mysqli_fetch_assoc($result)) {
        echo '<tr>';
        foreach ($row as $value) {
            echo '<td>' . htmlspecialchars((string) ($value ?? ''), ENT_QUOTES, 'UTF-8') . '</td>';
        }
        echo '</tr>';
    }
    echo '</table>';
    mysqli_free_result($result);
}

function vid_content(mysqli $conn, string $table): void
{
    if (!validStudyTable($table)) {
        return;
    }

    $rus_name = [
        'snum' => 'Номер продавца',
        'sname' => 'Имя продавца',
        'city' => 'Город',
        'comm' => 'Комиссионные',
        'cnum' => 'Номер покупателя',
        'cname' => 'Имя покупателя',
        'rating' => 'Рейтинг',
        'onum' => 'Номер заказа',
        'amt' => 'Сумма заказа',
        'odate' => 'Дата заказа',
    ];

    echo '<h4>Содержимое таблицы ' . htmlspecialchars($table, ENT_QUOTES, 'UTF-8') . '</h4>';
    $result = mysqli_query($conn, 'SELECT * FROM `' . $table . '`');
    if (!$result) {
        echo '<p>Ошибка получения содержимого таблицы.</p>';
        return;
    }

    $fields = mysqli_fetch_fields($result);
    echo '<table border="1" cellpadding="5"><tr>';
    foreach ($fields as $field) {
        $name = $field->name;
        echo '<th>' . htmlspecialchars($rus_name[$name] ?? $name, ENT_QUOTES, 'UTF-8')
            . '<br>' . htmlspecialchars($name, ENT_QUOTES, 'UTF-8') . '</th>';
    }
    echo '</tr>';

    while ($row = mysqli_fetch_assoc($result)) {
        echo '<tr>';
        foreach ($fields as $field) {
            echo '<td>' . htmlspecialchars((string) ($row[$field->name] ?? ''), ENT_QUOTES, 'UTF-8') . '</td>';
        }
        echo '</tr>';
    }
    echo '</table>';
    mysqli_free_result($result);
}
?>
<p><a href="z10-1.htm">Возврат к выбору таблицы</a></p>
