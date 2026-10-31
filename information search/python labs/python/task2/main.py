def is_valid_brackets(sequence: str) -> bool:
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for char in sequence:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack or stack[-1] != pairs[char]: # либо стек пустой (мы встретили закрывающуюся скобку,
                # но перед ней не было ни одной открывающейся,
                # либо верхний элемент стека (последний добавленный) не соответсвует текущей закрывающейся скобке
                return False
            stack.pop()
    return len(stack) == 0 # все открывающиеся скобки были правильно закрыты

def main():
    print("Выберите способ ввода:")
    print("1 — из консоли")
    print("2 — из файла")
    choice = input("Ваш выбор: ").strip()
    sequence = ""
    if choice == "1":
        sequence = input("Введите скобочную последовательность: ").strip()
    elif choice == "2":
        filename = input("Введите путь к файлу: ").strip()
        try:
            with open(filename, "r", encoding="utf-8") as f:
                sequence = f.read().strip()
        except FileNotFoundError:
            print(f"Ошибка: файл '{filename}' не найден.")
            return
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return
    else:
        print("Такого варианта нет. Завершение программы.")
        return
    if not sequence:
        print("Пустая последовательность считается правильной.")
        return
    if is_valid_brackets(sequence):
        print("Правильная последовательность.")
    else:
        print("Неправильная последовательность.")
if __name__ == "__main__":
    main()