# Задание 3.8
# 1. Считать из параметров командной строки одномерный массив, состоящий из N целочисленных элементов.
# 2. Вывести в консоль сумму элементов списка.
# 3. Вывести в консоль произведение элементов списка.
# 4. Заменить все нулевые элементы на среднее арифметическое всех элементов массива. Вывести результат в консоль.

import sys

numbers = [int(numbers) for numbers in sys.argv[1:]]

summa = sum(numbers)

proizvedenie = 1
for i in numbers:
    proizvedenie = proizvedenie * i

srednee = summa / len(numbers)
numbers = [srednee if i == 0 
           else 
           i for i in numbers]

print("Сумма введенных чисел: ", summa)
print("Произведение введенных чисел: ", proizvedenie)
print("Введеные числа с заменой нулевых на среднее арифметическое: ", numbers)

# Пример: python lab_3_3.8.py 1 2 3 4 0
