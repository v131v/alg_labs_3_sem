import copy
from typing import List, Tuple, Optional


def build_distance_matrix(
    num_vertices: int, edges: List[Tuple[int, int, float]]
) -> List[List[float]]:
    # Инициализируем матрицу большими значениями
    dist_matrix = [[float("inf")] * num_vertices for _ in range(num_vertices)]
    for i in range(num_vertices):
        dist_matrix[i][i] = 0  # Расстояние от вершины к самой себе равно 0

    for start, end, weight in edges:
        dist_matrix[start][end] = weight

    print(dist_matrix)
    return dist_matrix


def nearest_neighbor(
    dist_matrix: List[List[float]],
) -> Tuple[List[Tuple[int, int, float]], float]:
    num_vertices = len(dist_matrix)
    visited = [False] * num_vertices
    tour = []
    total_distance = 0.0
    current_city = 0
    visited[current_city] = True

    for _ in range(num_vertices - 1):
        nearest_distance = float("inf")
        nearest_city = None

        for i in range(num_vertices):
            if not visited[i] and dist_matrix[current_city][i] < nearest_distance:
                nearest_distance = dist_matrix[current_city][i]
                nearest_city = i

        if nearest_city is None:
            total_distance += nearest_distance
            return tour, total_distance

        visited[nearest_city] = True
        tour.append((current_city, nearest_city, nearest_distance))
        total_distance += nearest_distance
        current_city = nearest_city

    # Завершаем тур возвращением в начальную точку
    total_distance += dist_matrix[current_city][0]
    tour.append((current_city, 0, dist_matrix[current_city][0]))

    return tour, total_distance


def find_hamiltonian_cycle(graph: List[List[int]]) -> Optional[List[int]]:
    n = len(graph)
    path: List[int] = []

    def dfs(vertex: int, path: List[int]) -> Optional[List[int]]:
        path.append(vertex)
        if len(path) == n:
            if (
                graph[path[-1]][path[0]] != 0
            ):  # Проверяем, можем ли вернуться в начальную вершину
                path.append(path[0])  # Замыкаем цикл
                return path
            else:
                path.pop()
                return None

        for next_vertex in range(n):
            if graph[vertex][next_vertex] != 0 and next_vertex not in path:
                result = dfs(next_vertex, path)
                if result:
                    return result

        path.pop()  # Backtracking
        return None

    for start_vertex in range(n):  # Можем начать с любой вершины
        result = dfs(start_vertex, [])
        if result:
            return result

    return None


import random
import math


def calculate_total_distance(tour, dist_matrix):
    total_distance = 0
    num_cities = len(tour)
    for i in range(num_cities):
        total_distance += dist_matrix[tour[i]][tour[(i + 1) % num_cities]]
    return total_distance


def simulated_annealing(
    dist_matrix,
    tour: List[int],
    initial_temperature=1000,
    cooling_rate=0.999,
):
    num_cities = len(dist_matrix)
    current_distance = calculate_total_distance(tour, dist_matrix)
    current_tour = tour[:-1]

    best_tour = current_tour[:]
    best_distance = current_distance

    temperature = initial_temperature

    while temperature > 0.1:
        new_tour = current_tour[:]
        # Производим мутацию текущего маршрута (поменяем местами два города)
        city1, city2 = random.sample(range(num_cities), 2)
        new_tour[city1], new_tour[city2] = new_tour[city2], new_tour[city1]

        new_distance = calculate_total_distance(new_tour, dist_matrix)
        delta_distance = new_distance - current_distance
        if new_distance < float("inf"):
            print(temperature, " dist: ", new_distance, " tour: ", new_tour)

        if delta_distance < 0 or random.random() <= math.exp(
            -delta_distance / temperature
        ):
            current_tour = new_tour
            current_distance = new_distance

            if current_distance < best_distance:
                best_tour = current_tour[:]
                best_distance = current_distance

        # Уменьшаем температуру
        temperature *= cooling_rate

    ans_tour = []

    for i in range(len(best_tour) - 1):
        ans_tour.append(
            (
                best_tour[i],
                best_tour[i + 1],
                dist_matrix[best_tour[i]][best_tour[i + 1]],
            )
        )

    ans_tour.append(
        (best_tour[-1], best_tour[0], dist_matrix[best_tour[-1]][best_tour[0]])
    )

    return ans_tour, calculate_total_distance(best_tour, dist_matrix)
