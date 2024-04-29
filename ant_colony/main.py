from gui import *
from lib import *
from typing import List, Tuple


if __name__ == "__main__":

    def handler(
        n: int, edges: List[Tuple[int, int, float]], alpha: float, beta: float
    ) -> Tuple[list[Tuple[int, int, float], float]]:
        try:
            matrix = np.array(build_distance_matrix(n, edges))

            tour, dist = ant_colony_optimization(
                matrix, len(matrix), len(matrix) // 2, 1000, 0.8, alpha=alpha, beta=beta
            )
            print(tour)
            return tour, dist
        except:
            return handler(n, edges, alpha, beta)

    App(
        "The annealing method",
        handler,
    )
