def caesar_cipher(text: str, shift: int, language: str) -> str:
    if language == "ru":
        alphabet_lower = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        alphabet_upper = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    elif language == "en":
        alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
        alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    else:
        raise ValueError("Поддерживаются только русский и английский языки")
    result = []
    alphabet_len = len(alphabet_lower)
    for char in text:
        if char in alphabet_lower:
            idx = alphabet_lower.index(char)
            new_idx = (idx + shift) % alphabet_len
            result.append(alphabet_lower[new_idx])
        elif char in alphabet_upper:
            idx = alphabet_upper.index(char)
            new_idx = (idx + shift) % alphabet_len
            result.append(alphabet_upper[new_idx])
        else:
            result.append(char)
    return "".join(result)

def main():
    input_path = input("Введите путь к исходному файлу: ").strip()
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл '{input_path}' не найден.")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return
    while True:
        try:
            shift = int(input("Введите сдвиг (целое число, может быть отрицательным): ").strip())
            break
        except ValueError:
            print("Ошибка: введите целое число.")
    while True:
        lang = input("Выберите язык текста (ru — русский, en — английский): ").strip().lower()
        if lang in ("ru", "en"):
            break
        print("Ошибка: введите 'ru' или 'en'.")
    encrypted = caesar_cipher(text, shift, lang)
    output_path = input("Введите имя файла для сохранения результата: ").strip()
    if not output_path:
        output_path = "encrypted.txt"
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(encrypted)
        print(f"\nГотово! Зашифрованный текст сохранен в файл: {output_path}")
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")
if __name__ == "__main__":
    main()