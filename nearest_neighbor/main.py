from gui import *
from lib import *
from typing import List, Tuple


if __name__ == "__main__":

    def handler(
        n: int, edges: List[Tuple[int, int, float]]
    ) -> Tuple[list[Tuple[int, int, float], float]]:
        matrix = build_distance_matrix(n, edges)
        tour, dist = nearest_neighbor(matrix)
        print(tour)
        best_tour, best_dist = check_swap(matrix, tour, dist)
        print(best_tour)
        return best_tour, best_dist

    App(
        "The nearest neighbor method",
        handler,
    )
