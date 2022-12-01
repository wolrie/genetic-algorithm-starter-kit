"""Implementation of a genetic algorithm for solving sudokus."""

import random
from typing import List


def evolve(population: List, lift_factor: float, verbose: bool) -> None:
    """Evolve a population of sudokus towards a valid solution.

    TODO Refactor.

    Parameters
    ----------
    population : List[RandomSudoku]
        A list of individual sudokus to breed from.
    lift_factor : float, optional
        Factor of population containing the fittest sudokus that gets lifted,
        i.e. copied, to the new generation.
    """
    def print_out(generation_count: int, fittest_sudoku):
        """Print out during evolution."""
        if verbose:
            separator = "\n"
        else:
            separator = "\r"
        print(
            f"GENERATION: {str(generation_count).zfill(7)} "
            f"FITNESS SCORES - total: {str(round(fittest_sudoku.fitness_score, 5)).zfill(7)} | "
            f"boxes: {str(round(fittest_sudoku.fitness_score_boxes, 5)).zfill(7)} | "
            f"cols: {str(round(fittest_sudoku.fitness_score_cols, 5)).zfill(7)} | "
            f"rows: {str(round(fittest_sudoku.fitness_score_rows, 5)).zfill(7)}",
            end=separator,
        )

    generation_count = 1
    target_found = False
    while not target_found:

        # sort population by decreasing order of fitness score
        population = sorted(
            population,
            key=lambda x: x.fitness_score,
            reverse=True,
        )
        fittest_sudoku = population[0]
        # if fittest individual has fitness score of 1 we are done
        if fittest_sudoku.fitness_score >= 1.0:
            target_found = True

        print_out(generation_count, fittest_sudoku)

        # generate new offsprings for new generation
        new_generation = []

        # fittest individuals go to next generation
        n_fittest_sudokus = int(lift_factor * len(population))
        new_generation.extend(population[:n_fittest_sudokus])

        # 50% of fittest individuals mate to produce offspring
        idx = len(population) - n_fittest_sudokus
        for _ in range(idx):
            parent0 = random.choice(population[:len(population)//2])
            parent1 = random.choice(population[:len(population)//2])
            child = parent0.reproduce(parent1)
            new_generation.append(child)

        population = new_generation
        generation_count += 1

    print("\n\nFittest Individual:")
    print(*fittest_sudoku.board, sep="\n")
    print("\nDone.")
    return fittest_sudoku.board
