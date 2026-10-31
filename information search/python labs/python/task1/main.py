def pascal_triangle(n):
    triangle = []
    for i in range(n):
        row = [1] * (i + 1) # заполняем строки единицами
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j] # каждый элемент равен сумме двух элементов, стоящих над ним в предыдущей строке
        triangle.append(row)
    return triangle

def main():
    while True:
        user_input = input("Введите целое положительное число n: ").strip()
        try:
            n = int(user_input)
            if n <= 0:
                print("Ошибка: n должно быть целым положительным числом (больше 0). Попробуйте еще раз.")
                continue
            break
        except ValueError:
            print("Ошибка: введено не целое число. Попробуйте еще раз.")
    triangle = pascal_triangle(n)
    for row in triangle:
        print(" ".join(map(str, row)))

if __name__ == "__main__":
    main()