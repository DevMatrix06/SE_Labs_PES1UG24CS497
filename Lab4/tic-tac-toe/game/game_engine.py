"""
GameEngine: owns the board, turn state, and round-end logic.

You (the player) always play X and click to move. The computer always
plays O and moves automatically right after you, using a simple
random-move AI (see game/ai.py) - this is given infrastructure, not
something you need to build.

Starter version: no scoreboard yet, no first-player choice, and only
one combined reset control. Win/draw detection has known bugs (see
game/rules.py and check_round_end below) that Task 1 asks you to fix,
and move validation has a known gap (see handle_click) that Task 3
asks you to fix.
"""

from game.rules import check_winner, is_board_full
from game.renderer import board_pos_to_cell
from game.ai import choose_move

HUMAN_SYMBOL = 'X'
COMPUTER_SYMBOL = 'O'


class GameEngine:
    def __init__(self):
        self.scores = {'X': 0, 'O': 0, 'draw': 0}
        self.first_player = 'X'   # who starts the next round; changed with F
        self.new_round()

    def new_round(self):
        """Start a fresh round; the scoreboard is kept."""
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = self.first_player
        self.round_over = False
        self.winner = None   # 'X', 'O', or None (meaning draw, only valid when round_over)
        self._maybe_take_computer_turn()   # computer opens the round if O starts

    def reset_match(self):
        """Clear the scoreboard and start a fresh round."""
        self.scores = {'X': 0, 'O': 0, 'draw': 0}
        self.new_round()

    def handle_click(self, pos):
        if self.round_over:
            return   # round has ended - ignore further moves
        if self.current_player != HUMAN_SYMBOL:
            return   # not your turn - the computer is about to move (or already has)
        cell = board_pos_to_cell(pos)
        if cell is None:
            return
        row, col = cell
        if self.board[row][col] is not None:
            return   # occupied cell - reject the click, leave board and turn untouched
        self.board[row][col] = self.current_player
        self.check_round_end()
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self._maybe_take_computer_turn()

    def _maybe_take_computer_turn(self):
        if self.round_over or self.current_player != COMPUTER_SYMBOL:
            return
        move = choose_move(self.board)
        if move is None:
            return
        row, col = move
        self.board[row][col] = self.current_player
        self.check_round_end()
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def handle_keydown(self, key):
        import pygame
        if key == pygame.K_r:
            self.new_round()
        elif key == pygame.K_m:
            self.reset_match()
        elif key == pygame.K_f:
            self.first_player = 'O' if self.first_player == 'X' else 'X'   # applies next round

    def check_round_end(self):
        if self.round_over:
            return
        winner = check_winner(self.board)
        if winner:
            self.round_over = True
            self.winner = winner
            self.scores[winner] += 1
        elif is_board_full(self.board):
            self.round_over = True
            self.winner = None
            self.scores['draw'] += 1

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_board(surface, self.board)
        turn_label = "Your turn (X)" if self.current_player == HUMAN_SYMBOL else "Computer's turn (O)"
        renderer.draw_text(surface, font, turn_label, (10, 15))
        renderer.draw_scoreboard(surface, font, self.scores)
        renderer.draw_text(surface, font, "R: new round  M: reset match", (10, renderer.BOARD_TOP + renderer.BOARD_SIZE + 60))
        renderer.draw_text(surface, font, f"Next round starts: {self.first_player} (F)", (10, renderer.BOARD_TOP + renderer.BOARD_SIZE + 88))

        if self.round_over:
            text = f"{self.winner} wins!" if self.winner else "Draw!"
            renderer.draw_banner(surface, font, f"{text} Press R for a new round.")
