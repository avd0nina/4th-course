#!/usr/bin/env python3

def rc4(data: bytes, key: bytes) -> bytes:
    # Поточный шифр RC4
    # Одна и та же функция используется и для шифрования, и для расшифрования,
    # потому что операция XOR обратима: (P ⊕ K) ⊕ K = P
    if not key:
        raise ValueError("Ключ не должен быть пустым.")
    # KSA (Key Scheduling Algorithm)
    # Инициализация S-блока: S[i] = i для i = 0...255
    state = list(range(256))
    j = 0
    for i in range(256):
        # Перемешивание S-блока с учетом ключа
        j = (j + state[i] + key[i % len(key)]) & 0xFF   # &0xFF == mod 256
        state[i], state[j] = state[j], state[i]         # обмен элементов
    # PRGA (Pseudo-Random Generation Algorithm)
    # Генерация ключевого потока и XOR с данными
    result = bytearray()
    i = j = 0
    for value in data:
        i = (i + 1) & 0xFF
        j = (j + state[i]) & 0xFF
        state[i], state[j] = state[j], state[i]         # снова обмен
        # Байт ключевого потока
        k = state[(state[i] + state[j]) & 0xFF]
        result.append(value ^ k)                        # XOR с исходным байтом
    return bytes(result)

def main() -> None:
    text = input("Введите строку: ")
    key_text = input("Введите ключ: ")
    source = text.encode("utf-8")
    key = key_text.encode("utf-8")
    encrypted = rc4(source, key)
    decrypted = rc4(encrypted, key).decode("utf-8")
    print(f"\nИсходная строка: {text}")
    print(f"Ключ: {key_text}")
    print(f"Шифртекст (hex): {encrypted.hex()}")
    print(f"Расшифрованная строка: {decrypted}")
    print(f"Проверка: {'успешно' if decrypted == text else 'ошибка'}")

if __name__ == "__main__":
    main()