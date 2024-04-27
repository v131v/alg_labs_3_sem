from gui import *
from lib import *
from typing import List, Tuple


if __name__ == "__main__":

    def handler(
        n: int, edges: List[Tuple[int, int, float]], tempr: float
    ) -> Tuple[list[Tuple[int, int, float], float]]:
        matrix = build_distance_matrix(n, edges)
        tour = find_hamiltonian_cycle(matrix)
        print(tour)

        if tour is not None:
            tour, dist = simulated_annealing(
                matrix, tour, initial_temperature=tempr + 0.1
            )
            print(tour)
        return tour, dist

    App(
        "The annealing method",
        handler,
    )
