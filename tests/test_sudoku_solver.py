import unittest

from sudoku_solver.sudoku import Sudoku
from tests.etc import config


class TestSudokuSolver(unittest.TestCase):

    sudoku = Sudoku(config.valid_starting_position)

    def test_board_solver(self):
        """ Check solver output. """
        self.assertTrue(self.sudoku.solve())

    def test_solved_board(self):
        """ Check solved sudoku. """
        self.assertEqual(self.sudoku.board, config.solved_board)


if __name__ == '__main__':
    unittest.main()
