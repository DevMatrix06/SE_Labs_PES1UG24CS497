"""
ai: a simple computer opponent for the second player (O).

Picks a random empty cell - this is intentionally simple. The point
of this lab is testing your own win/draw/turn logic against a working
opponent, not building a hard-to-beat AI.
"""

import random


def choose_move(board):
    empty_cells = [
        (r, c) for r in range(3) for c in range(3) if board[r][c] is None
    ]
    if not empty_cells:
        return None
    return random.choice(empty_cells)
