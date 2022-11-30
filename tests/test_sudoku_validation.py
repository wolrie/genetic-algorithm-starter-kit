import copy
import unittest

from sudoku_solver.sudoku import Sudoku
from sudoku_solver.utils import validate
from tests.etc import config


class TestSudokuValidation(unittest.TestCase):

    sudoku = Sudoku(config.valid_starting_position)

    @staticmethod
    def _update_board(row, col, symbol):
        # Deep copy so that the board is not changed for other tests
        board = copy.deepcopy(config.valid_starting_position)
        board[row][col] = symbol
        return board

    def test_valid_board(self):
        self.assertEqual(
            self.sudoku.is_valid(),
            True,
            "Sudoku should be valid (True)."
        )

    def test_rows(self):
        self.assertTrue(
            validate.are_valid_rows(config.valid_starting_position),
            "Rows should be valid (True)."
        )

    def test_columns(self):
        self.assertTrue(
            validate.are_valid_cols(config.valid_starting_position),
            "Columns should be valid (True)."
        )

    def test_boxes(self):
        self.assertTrue(
            validate.are_valid_boxes(config.valid_starting_position),
            "Boxes should be valid (True)."
        )

    def test_duplicate(self):
        # Two 3s in the upper left box in same row
        board = self._update_board(row=0, col=0, symbol=3)
        self.assertEqual(
            Sudoku(board).is_valid(),
            False,
            "Should be invalid (False)."
        )

    def test_for_out_of_range_number(self, num=10):
        # Invalid number
        board = self._update_board(row=0, col=0, symbol=num)
        self.assertEqual(
            Sudoku(board).is_valid(),
            False,
            "Should be invalid (False)."
        )


if __name__ == '__main__':
    unittest.main()
