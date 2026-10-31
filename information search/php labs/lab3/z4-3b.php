<?php
declare(strict_types=1);

$correctAnswers = ['6', '9', '4', '1', '3', '2', '5', '8', '7'];
$monumentKeys = [
    'prado', 'reichstag', 'scala', 'horseman', 'wailing_wall',
    'tretyakov', 'arc', 'liberty', 'tower',
];
$user = trim((string) ($_POST['user'] ?? ''));
$answers = $_POST['answers'] ?? [];
$score = 0;

foreach ($monumentKeys as $index => $key) {
    if ((string) ($answers[$key] ?? '') === $correctAnswers[$index]) {
        $score++;
    }
}

switch ($score) {
    case 9:
        $result = 'великолепно знаете географию';
        break;
    case 8:
        $result = 'отлично знаете географию';
        break;
    case 7:
        $result = 'очень хорошо знаете географию';
        break;
    case 6:
        $result = 'хорошо знаете географию';
        break;
    case 5:
        $result = 'удовлетворительно знаете географию';
        break;
    case 4:
        $result = 'терпимо знаете географию';
        break;
    case 3:
        $result = 'плохо знаете географию';
        break;
    case 2:
        $result = 'очень плохо знаете географию';
        break;
    default:
        $result = 'вообще не знаете географию';
        break;
}
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Результат теста</title>
</head>
<body>
    <h2>Результат тестирования</h2>
    <p><?= htmlspecialchars($user !== '' ? $user : 'Тестируемый', ENT_QUOTES, 'UTF-8') ?>, вы набрали
        <?= $score ?> из <?= count($correctAnswers) ?> правильных ответов.</p>
    <p><?= $result ?>.</p>
    <p><a href="z4-3a.htm">Пройти тест ещё раз</a></p>
</body>
</html>
