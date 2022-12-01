from itertools import product
from typing import List

from sudoku_solver.etc import config


def check_row_update(board: List[List[int]], row: int, digit: int) -> bool:
    """Check for duplicate entry in row."""
    return not any([board[row][i] == digit for i in range(9)])


def check_col_update(board: List[List[int]], col: int, digit: int) -> bool:
    """Check for duplicate entry in column."""
    return not any([board[i][col] == digit for i in range(9)])


def check_box_update(board: List[List[int]], row: int, col: int, digit: int) -> bool:
    """Check for duplicate entry in box."""
    row, col = 3 * (row // 3), 3 * (col // 3)
    return not any([board[row + i][col + j] == digit for i, j in product(range(3), repeat=2)])


def get_empty_cell_coordinates(board: List[List[int]]) -> List[int]:
    """Return coordinates of empty cell."""
    for row, col in product(range(9), repeat=2):
        if board[row][col] == config.empty_cell_symbol:
            return row, col
    return None, None


def is_valid_update(board: List[List[int]], row: int, col: int, digit: int) -> bool:
    """Check whether given cell entry at given coordinates is a valid update."""
    flag = (check_row_update(board, row=row, digit=digit) and
            check_col_update(board, col=col, digit=digit) and
            check_box_update(board, row=row, col=col, digit=digit))
    return True if flag else False
