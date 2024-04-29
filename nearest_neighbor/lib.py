import copy
from typing import List, Tuple


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


def check_swap(
    dist_matrix: List[List[float]], tour: List[Tuple[int, int, float]], dist: float
):
    best_tour = tour
    best_dist = dist
    for i in range(len(tour) - 2):
        for j in range(i + 1, len(tour) - 1):
            ap, _, _ = tour[i]
            a, an, _ = tour[i + 1]
            bp, _, _ = tour[j]
            b, bn, _ = tour[j + 1]

            if not (
                dist_matrix[ap][b] < float("inf")
                and dist_matrix[b][an] < float("inf")
                and dist_matrix[bp][a] < float("inf")
                and dist_matrix[a][bn] < float("inf")
            ):
                continue

            was_edges = set([tour[i], tour[i + 1], tour[j], tour[j + 1]])
            was_dist = 0
            for _, _, w in was_edges:
                was_dist += w

            now_edges = [
                (bp, a, dist_matrix[bp][a]),
                (a, bn, dist_matrix[a][bn]),
                (ap, b, dist_matrix[ap][b]),
                (b, an, dist_matrix[b][an]),
            ]
            now_dist = 0
            for _, _, w in set(now_edges):
                now_dist += w

            if dist + now_dist - was_dist < best_dist:
                best_dist = dist + now_dist - was_dist
                best_tour = copy.deepcopy(tour)
                best_tour[i] = now_edges[0]
                best_tour[i + 1] = now_edges[1]
                best_tour[j] = now_edges[2]
                best_tour[j + 1] = now_edges[3]

    return best_tour, best_dist
