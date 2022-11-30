from collections import Counter
from typing import List

from sudoku_solver.etc import config


def _score_list(list_: List[int]) -> int:
    """Count number of unique and valid elements in list."""
    counter = Counter(list_)
    [counter.pop(x, None) for x in list_ if x not in config.allowed_symbols]
    return len(counter.keys())


def score_boxes(board: List[List[int]], normalize: bool) -> int:
    """Compute fitness score of all boxes in sudoku board.

    Maximum score is number of cells (81) and minimum score is 0.
    """
    scores = []
    for box_num in range(9):
        row, col = 3 * (box_num // 3), 3 * (box_num % 3)
        box = [board[row + j][col:col + 3] for j in range(3)]
        box_flattened = [item for row in box for item in row]
        scores.append(_score_list(box_flattened))
    if normalize:
        return sum(scores) / (9 * 9)
    return sum(scores)


def score_cols(board: List[List[int]], normalize: bool) -> int:
    """Compute fitness score of all columns in sudoku board.

    Maximum score is number of cells (81) and minimum score is 0.
    """
    score = sum([_score_list([row[i] for row in board]) for i in range(9)])
    if normalize:
        return score / (9 * 9)
    return score


def score_rows(board: List[List[int]], normalize: bool) -> int:
    """Compute fitness score of all rows in sudoku board.

    Maximum score is number of cells (81) and minimum score is 0.
    """
    score = sum([_score_list(row) for row in board])
    if normalize:
        return score / (9 * 9)
    return score
