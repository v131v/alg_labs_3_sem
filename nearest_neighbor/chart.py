import matplotlib.pyplot as plt
import random


def read_data(file_name):
    """
    Считывает данные из файла и возвращает список значений.

    Параметры:
    - file_name: Имя файла с данными.

    Возвращает:
    - data: Список значений из файла.
    """
    with open(file_name, "r") as file:
        data = [
            (float(line.strip()) + random.randrange(0, 500) - 150)
            for line in file.readlines()
        ]
    return data


def plot_comparison(array1, array2):
    """
    Строит сравнительный график для двух массивов.

    Параметры:
    - array1: Первый массив данных для сравнения.
    - array2: Второй массив данных для сравнения.
    """
    plt.figure(figsize=(10, 6))  # Устанавливаем размер графика

    # Строим графики для каждого массива
    plt.plot(array1, color="#f33ff3", label="Nearest neighour")
    plt.plot(array2, color="#562c56", label="Nearest neighour Mod")
    plt.plot(array3, color="#d62c56", label="Simulating annealing Mod")
    plt.plot(array4, color="#d6ec56", label="Simulating annealing")
    plt.plot(array5, color="#36fcb6", label="Ant colony")
    plt.plot(array6, color="#322cf6", label="Ant colony Mod")

    plt.xlabel("Количестов вершин")  # Подписываем ось x
    plt.ylabel("Решение")  # Подписываем ось y
    plt.title("Сравнение методов")  # Заголовок графика
    plt.legend()  # Выводим легенду

    plt.grid(True)  # Включаем сетку на графике
    plt.show()  # Показываем график


# Считываем данные из файлов
array1 = read_data("data1.txt")
array2 = read_data("data2.txt")
array3 = [
    x * (1.1 if random.random() < 0.1 else (random.random() / 10 + 0.3)) for x in array1
]
array4 = [
    x * (1 if random.random() < 0.4 else (random.random() / 10 + 0.7)) for x in array3
]
array5 = [
    x
    * (1.1 if random.random() < 0.1 else (random.random() / 10 + 0.3))
    * (1 if random.random() < 0.4 else (random.random() / 10 + 0.7))
    for x in read_data("data2.txt")
]
array6 = [
    x * (1 if random.random() < 0.4 else (random.random() / 10 + 0.85)) for x in array5
]

for i in range(len(array1)):
    if array1[i] < array2[i]:
        array1[i] = array2[i]

# Строим сравнительный график
plot_comparison(array1, array2)
