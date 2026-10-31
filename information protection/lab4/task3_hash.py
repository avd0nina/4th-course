#!/usr/bin/env python3

from task2_rc5 import BLOCK_SIZE, encrypt_block

# Начальное значение хеша (Initialization Vector), 8 байт
INITIAL_VECTOR = b"Lab4Hash"

def davies_meyer(message: bytes) -> bytes:
    # Хеш-функция по схеме Дэвиса–Мейера
    # Идея: H_i = RC5_encrypt(ключ = блок_сообщения, данные = H_{i-1})  XOR  H_{i-1}
    # Сообщение дополняется так, чтобы его длина была кратна размеру блока,
    # и в конец записывается длина исходного сообщения в битах

    # Длина исходного сообщения в битах (8 байт)
    length = (len(message) * 8).to_bytes(8, "big")
    # Дополнение: добавляем байт 0x80, потом нули, потом длину
    padded = message + b"\x80"
    # Выравниваем так, чтобы после добавления длины длина стала кратна BLOCK_SIZE
    padded += b"\0" * ((BLOCK_SIZE - (len(padded) + 8) % BLOCK_SIZE) % BLOCK_SIZE)
    padded += length
    # Начинаем с фиксированного начального значения
    state = INITIAL_VECTOR
    # Обрабатываем сообщение по блокам
    for offset in range(0, len(padded), BLOCK_SIZE):
        message_block = padded[offset:offset + BLOCK_SIZE]
        # Дэвис–Мейер: шифруем текущий state, используя блок сообщения как ключ
        encrypted = encrypt_block(state, message_block)
        # XOR с предыдущим значением state
        state = bytes(a ^ b for a, b in zip(encrypted, state))
    return state   # итоговый хеш (8 байт)

def hamming_distance(first: bytes, second: bytes) -> int:
    # Расстояние Хэмминга - количество различающихся бит между двумя хешами
    return sum((a ^ b).bit_count() for a, b in zip(first, second))

def main() -> None:
    text = input("Введите сообщение: ")
    message = text.encode("utf-8")
    # Хеш исходного сообщения
    digest = davies_meyer(message)
    print(f"\nСообщение: {text}")
    print(f"Хеш (hex): {digest.hex()}")
    print("№ | измененный бит | расстояние Хэмминга")
    distances = []
    # 20 экспериментов: каждый раз меняем один бит в разных позициях
    for number in range(1, 21):
        changed = bytearray(message or b"\0")   # на случай пустого сообщения
        # Выбираем позицию бита (разные позиции в разных экспериментах)
        bit_index = (number * 7) % (len(changed) * 8)
        # Инвертируем один бит
        changed[bit_index // 8] ^= 1 << (bit_index % 8)
        # Считаем хеш измененного сообщения и расстояние Хэмминга
        distance = hamming_distance(digest, davies_meyer(bytes(changed)))
        distances.append(distance)
        print(f"{number:2d} | {bit_index:14d} | {distance:21d}")
    average = sum(distances) / len(distances)
    print(f"Среднее расстояние: {average:.2f} из 64 бит")
    # Вывод о наличии лавинного эффекта
    if 28 <= average <= 36:
        print("Вывод: лавинный эффект наблюдается (примерно половина бит изменяется).")
    else:
        print("Вывод: лавинный эффект выражен слабо или отсутствует.")

if __name__ == "__main__":
    main()