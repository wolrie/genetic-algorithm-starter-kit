from __future__ import annotations

import copy
import random
from functools import cache
from itertools import product
from typing import List

from .etc import config
from .utils import evolve, score_fitness, solve, validate


class Sudoku:
    """A class for solving sudokus.

    This class implements two algorithms to solve a sudoku:
        * backtracking algorithm
        * genetic algorithm

    A sudoku is a 9x9 grid which has to be filled entirely according to the
    following rules:

    1. Each row must contain the digits 1-9 without repetition.
    2. Each column must contain the digits 1-9 without repetition.
    3. Each of the nine distinct non-overlapping 3x3 sub-boxes of the grid
    must contain the digits 1-9 without repetition.
    """

    def __init__(self, board: List[List[int]]) -> None:
        self.board = copy.deepcopy(board)

    @property
    def fitness_score(self) -> float:
        """Compute mean of all fitness scores for sudoku configuration."""
        scores = [
            self.fitness_score_boxes,
            self.fitness_score_cols,
            self.fitness_score_rows,
        ]
        return sum(scores) / len(scores)

    @property
    def fitness_score_boxes(self) -> float:
        """Compute fitness score for boxes."""
        return score_fitness.score_boxes(self.board, normalize=True)

    @property
    def fitness_score_cols(self) -> float:
        """Compute fitness score for cols."""
        return score_fitness.score_cols(self.board, normalize=True)

    @property
    def fitness_score_rows(self) -> float:
        """Compute fitness score for rows."""
        return score_fitness.score_rows(self.board, normalize=True)

    def evolve(self, population_size: int, lift_factor: float = 0.1, verbose: bool = True) -> None:
        """Solve sudoku with a genetic algorithm.

        Parameters
        ----------
        population_size : int
            Size of the population for the genetic algorithm.
        cutoff_factor : float, optional
            Factor of population containing the fittest sudokus that gets lifted,
            i.e. copied, to the new generation. Default is 0.1.
        """
        population = []
        for _ in range(population_size):
            sudoku = RandomSudoku(self.board)
            sudoku.fill_empty_cells()
            population.append(sudoku)
        self.board = evolve.evolve(population, lift_factor, verbose)

    def is_valid(self) -> bool:
        """Check if sudoku board is valid."""
        return all([func(self.board) for func in [validate.are_valid_rows,
                                                  validate.are_valid_cols,
                                                  validate.are_valid_boxes]])

    def solve(self) -> None:
        """Solve sudoku with backtracking algorithm."""
        row, col = solve.get_empty_cell_coordinates(self.board)
        # No empty cell left, sudoku is solved
        if row not in range(9) and col not in range(9):
            return True
        for digit in config.allowed_symbols:
            if solve.is_valid_update(self.board, row=row, col=col, digit=digit):
                self.board[row][col] = digit
                if self.solve():
                    return True
                # Backtrack in case of inconsistency
                self.board[row][col] = config.empty_cell_symbol
        return False

    # TODO
    # def __repr__(self):
    #     return self.board


class RandomSudoku(Sudoku):
    """Helper class for solving sudokus with a genetic algorithm."""

    prob_cutoffs = {
        "self": 0.45,
        "mate": 0.45 * 2,
    }

    def __init__(self, board: List[List[int]], empty_cell_coordinates: List[List[int]] = None) -> None:
        super().__init__(board)
        if empty_cell_coordinates is None:
            self._empty_cell_coordinates = self._get_empty_cell_coordinates()
        else:
            self._empty_cell_coordinates = empty_cell_coordinates

    @cache
    def _get_empty_cell_coordinates(self) -> List[int]:
        """Return coordinates of empty cells."""
        coords = []
        for row, col in product(range(9), repeat=2):
            if self.board[row][col] == config.empty_cell_symbol:
                coords.append((row, col))
        return coords

    def fill_empty_cells(self) -> None:
        """Fill all empty cells with random digits."""
        for row, col in self._empty_cell_coordinates:
            self.board[row][col] = random.choice(list(config.allowed_symbols))

    def reproduce(self, sudoku: RandomSudoku) -> RandomSudoku:
        """Perform reproduction and produce new offspring."""
        child_sudoku = RandomSudoku(self.board, self._empty_cell_coordinates)
        for row, col in self._empty_cell_coordinates:
            prob = random.random()
            if prob < self.prob_cutoffs["self"]:
                # get digit from self
                digit = self.board[row][col]
            elif prob < self.prob_cutoffs["mate"]:
                # get digit from other sudoku
                digit = sudoku.board[row][col]
            else:
                # random mutation
                digit = random.choice(list(config.allowed_symbols))
            child_sudoku.board[row][col] = digit
        return child_sudoku
