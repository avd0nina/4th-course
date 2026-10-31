#!/usr/bin/env python3

import secrets
from pathlib import Path

# Константы RC5
WORD_MASK = 0xFFFFFFFF          # Маска для 32-битных слов (обрезаем до 32 бит)
ROUNDS = 12                     # Количество раундов (стандартное значение)
BLOCK_SIZE = 8                  # Размер блока = 8 байт (два слова по 4 байта)

def rotate_left(value: int, amount: int) -> int:
    # Циклический сдвиг влево на amount бит (в пределах 32 бит)
    amount &= 31                # Сдвиг больше 31 бессмысленен
    if amount == 0:
        return value
    return ((value << amount) | (value >> (32 - amount))) & WORD_MASK

def rotate_right(value: int, amount: int) -> int:
    # Циклический сдвиг вправо на amount бит
    amount &= 31
    if amount == 0:
        return value
    return ((value >> amount) | (value << (32 - amount))) & WORD_MASK

def expand_key(key: bytes) -> list[int]:
    # Расширение ключа
    # Из короткого ключа пользователя создает длинный массив подключей (S),
    # который потом используется в каждом раунде шифрования/расшифрования
    if not key:
        raise ValueError("Ключ не должен быть пустым.")
    # Преобразуем байты ключа в массив 32-битных слов
    word_count = max(1, (len(key) + 3) // 4)
    words = [0] * word_count
    for index, value in enumerate(key):
        words[index // 4] |= value << (8 * (index % 4))
    # Создаем массив подключей
    subkey_count = 2 * (ROUNDS + 1)     # Для 12 раундов нужно 26 подключей
    subkeys = [0] * subkey_count
    # Инициализация "магическими" константами
    subkeys[0] = 0xB7E15163             # Pw (для 32-бит)
    for index in range(1, subkey_count):
        subkeys[index] = (subkeys[index - 1] + 0x9E3779B9) & WORD_MASK  # Qw
    # Перемешивание подключей с ключом пользователя
    a = b = i = j = 0
    for _ in range(3 * max(word_count, subkey_count)):
        a = subkeys[i] = rotate_left((subkeys[i] + a + b) & WORD_MASK, 3)
        b = words[j] = rotate_left(
            (words[j] + a + b) & WORD_MASK, (a + b) & 31
        )
        i = (i + 1) % subkey_count
        j = (j + 1) % word_count
    return subkeys

def encrypt_block(block: bytes, key: bytes) -> bytes:
    # Шифрование одного 8-байтового блока
    subkeys = expand_key(key)
    # Делим блок на две 32-битные половинки
    left = int.from_bytes(block[:4], "little")
    right = int.from_bytes(block[4:], "little")
    # Начальное добавление подключей
    left = (left + subkeys[0]) & WORD_MASK
    right = (right + subkeys[1]) & WORD_MASK
    # 12 раундов основного преобразования
    for round_number in range(1, ROUNDS + 1):
        left = (rotate_left(left ^ right, right) + subkeys[2 * round_number]) & WORD_MASK
        right = (rotate_left(right ^ left, left) + subkeys[2 * round_number + 1]) & WORD_MASK
    return left.to_bytes(4, "little") + right.to_bytes(4, "little")

def decrypt_block(block: bytes, key: bytes) -> bytes:
    # Расшифрование одного 8-байтового блока (операции в обратном порядке)
    subkeys = expand_key(key)
    left = int.from_bytes(block[:4], "little")
    right = int.from_bytes(block[4:], "little")
    # Раунды в обратном порядке
    for round_number in range(ROUNDS, 0, -1):
        right = rotate_right((right - subkeys[2 * round_number + 1]) & WORD_MASK, left) ^ left
        left = rotate_right((left - subkeys[2 * round_number]) & WORD_MASK, right) ^ right
    # Вычитаем начальные подключи
    left = (left - subkeys[0]) & WORD_MASK
    right = (right - subkeys[1]) & WORD_MASK
    return left.to_bytes(4, "little") + right.to_bytes(4, "little")

def pad(data: bytes) -> bytes:
    # Дополнение PKCS#7
    # Добавляет в конец столько байт, чтобы длина стала кратна 8
    # Каждый добавленный байт равен количеству добавленных байт
    count = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([count]) * count

def unpad(data: bytes) -> bytes:
    # Удаление дополнения PKCS#7
    count = data[-1]
    if not 1 <= count <= BLOCK_SIZE or data[-count:] != bytes([count]) * count:
        raise ValueError("Некорректное дополнение PKCS#7.")
    return data[:-count]

def encrypt_file(source: Path, destination: Path, key: bytes) -> None:
    # Шифрование файла в режиме CBC
    # - Генерируется случайный IV (8 байт)
    # - Каждый блок XOR-ится с предыдущим шифрблоком (или с IV)
    # - Затем шифруется
    iv = secrets.token_bytes(BLOCK_SIZE)   # Случайный вектор инициализации
    previous = iv
    encrypted = bytearray(iv)              # IV пишем в начало файла
    data = pad(source.read_bytes())        # Дополняем данные до кратности 8
    for offset in range(0, len(data), BLOCK_SIZE):
        # XOR текущего блока с предыдущим шифрблоком (CBC)
        block = bytes(a ^ b for a, b in zip(data[offset:offset + BLOCK_SIZE], previous))
        previous = encrypt_block(block, key)
        encrypted.extend(previous)
    destination.write_bytes(encrypted)

def decrypt_file(source: Path, destination: Path, key: bytes) -> None:
    # Расшифрование файла в режиме CBC
    data = source.read_bytes()
    if len(data) < 16 or len(data) % BLOCK_SIZE:
        raise ValueError("Некорректный размер зашифрованного файла.")
    previous = data[:BLOCK_SIZE]           # Первый блок - это IV
    result = bytearray()
    for offset in range(BLOCK_SIZE, len(data), BLOCK_SIZE):
        current = data[offset:offset + BLOCK_SIZE]
        decrypted = decrypt_block(current, key)
        # XOR с предыдущим шифрблоком, чтобы получить исходный блок
        result.extend(bytes(a ^ b for a, b in zip(decrypted, previous)))
        previous = current
    destination.write_bytes(unpad(bytes(result)))

def main() -> None:
    print("1 - зашифровать файл")
    print("2 - расшифровать файл")
    mode = input("Выберите операцию (1/2): ").strip()
    source = Path(input("Введите путь к исходному файлу: ").strip())
    destination = Path(input("Введите путь для результата: ").strip())
    key = input("Введите ключ: ").encode("utf-8")
    if mode == "1":
        encrypt_file(source, destination, key)
        print(f"\nФайл зашифрован: {source} -> {destination}")
    elif mode == "2":
        decrypt_file(source, destination, key)
        print(f"\nФайл расшифрован: {source} -> {destination}")
    else:
        raise ValueError("Нужно выбрать 1 или 2.")

if __name__ == "__main__":
    main()