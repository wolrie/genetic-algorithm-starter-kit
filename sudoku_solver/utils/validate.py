from collections import Counter
from typing import List

from sudoku_solver.etc import config


def _is_valid_list(list_: List[str or int]) -> bool:
    """Check if list contains duplicates or invalid digits.

    Parameters
    ----------
    list_ :
        List to be checked for validity (no duplicates and only valid Sudoku
        entries).
    empty_symbol :
        Symbol specifying an empty cell in a Sudoku grid.

    """
    counter = Counter(list_)
    counter.pop(config.empty_cell_symbol, None)
    if set(counter.values()) not in [set(), {1}]:
        return False
    return set([int(key) for key in counter.keys()]).issubset(config.allowed_symbols)


def are_valid_rows(board: List[List[int]]) -> bool:
    """Check sudoku's rows for validity according to rules."""
    return all([_is_valid_list(row) for row in board])


def are_valid_cols(board: List[List[int]]) -> bool:
    """Check sudoku's columns for validity according to rules."""
    return all([_is_valid_list([row[i] for row in board])
                for i in range(9)])


def are_valid_boxes(board: List[List[int]]) -> bool:
    """Check sudoku's 3x3 sub-boxes for validity according to rules."""
    flags = []
    for box_num in range(9):
        row, col = 3 * (box_num // 3), 3 * (box_num % 3)
        box = [board[row + j][col:col + 3] for j in range(3)]
        box_flattened = [item for row in box for item in row]
        flags.append(_is_valid_list(box_flattened))
    return all(flags)
