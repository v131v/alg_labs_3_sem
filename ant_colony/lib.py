from typing import List, Tuple, Optional
import numpy as np


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


def tour_to_edges(distances: np.ndarray, tour: np.ndarray) -> Tuple[int, int, float]:
    ans = []
    for i in range(len(tour) - 1):
        ans.append((tour[i], tour[i + 1], distances[tour[i]][tour[i + 1]]))
    ans.append((tour[-1], tour[0], distances[tour[-1]][tour[0]]))
    return ans


def ant_colony_optimization(
    distances: np.ndarray,
    n_ants: int,
    n_best: int,
    n_iterations: int,
    decay: float,
    alpha: float = 1,
    beta: float = 1,
) -> Tuple[np.ndarray, float]:
    n_cities: int = distances.shape[0]

    # Инициализация феромона
    pheromone: np.ndarray = np.ones((n_cities, n_cities)) / n_cities

    # Расчет вероятности выбора следующего города
    def probability(city: int, unvisited: List[int]) -> np.ndarray:
        pheromone_row: np.ndarray = pheromone[city][unvisited]
        distance_row: np.ndarray = distances[city][unvisited]
        return pheromone_row**alpha * ((1.0 / distance_row) ** beta)

    # Нахождение маршрута для одного муравья
    def construct_solution() -> np.ndarray:
        tour: np.ndarray = np.zeros(n_cities, dtype=int)
        unvisited: List[int] = list(range(n_cities))
        tour[0] = np.random.choice(unvisited)
        unvisited.remove(tour[0])

        for i in range(1, n_cities):
            last_city: int = tour[i - 1]
            p: np.ndarray = probability(last_city, unvisited)
            # print(p)
            if p.sum() > 0:
                p /= p.sum()
                next_city: int = np.random.choice(unvisited, p=p)
                tour[i] = next_city
                unvisited.remove(next_city)

        return tour

    # Расчет длины маршрута
    def length(tour: np.ndarray) -> float:
        return float(
            sum([distances[tour[i], tour[(i + 1) % n_cities]] for i in range(n_cities)])
        )

    best_tour: np.ndarray = None
    best_length: float = float("inf")

    for iteration in range(n_iterations):
        tours: List[np.ndarray] = [construct_solution() for _ in range(n_ants)]
        tours_length: np.ndarray = np.array([length(tour) for tour in tours])

        # Отбор лучших маршрутов для обновления феромона
        sorted_idx: np.ndarray = np.argsort(tours_length)
        for i in range(n_best):
            t: np.ndarray = tours[sorted_idx[i]]
            for j in range(n_cities - 1):
                pheromone[t[j], t[j + 1]] += 1.0 / tours_length[sorted_idx[i]]
            pheromone[t[-1], t[0]] += 1.0 / tours_length[sorted_idx[i]]

        # Испарение феромона
        pheromone *= decay

        # Обновление лучшего маршрута
        if tours_length.min() < best_length:
            best_length = tours_length.min()
            best_tour = tours[sorted_idx[0]]

    return tour_to_edges(distances, best_tour), best_length
