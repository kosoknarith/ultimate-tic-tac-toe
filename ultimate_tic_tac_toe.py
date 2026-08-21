# Lines that count as "3 in a row" on any 3x3 grid (rows, columns, diagonals).
# These same 8 lines are used for both a small board and the big board.
WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]

EMPTY = " "   # an empty square


class UltimateTicTacToe:
    def __init__(self):
        # cells[b][c] = the mark in board b, cell c.  " ", "X", or "O".
        self.cells = [[EMPTY] * 9 for _ in range(9)]

        # board_result[b] = result of small board b:
        #   " " = still in play,  "X"/"O" = won by that player,  "D" = drawn (full, no winner)
        self.board_result = [EMPTY] * 9

        self.current_player = "X"   # X always moves first

        # Which small board the current player MUST play in.
        # None means "free move" (play in any unfinished board).
        # The very first move of the game is free.
        self.active_board = None

        self.winner = None          # "X", "O", "D" (draw), or None while playing

    # ------------------------------------------------------------------
    # Rule helpers
    # ------------------------------------------------------------------

    # Given a list of 9 marks, return 'X' or 'O' if someone has 3 in a row, else None.
    def _line_winner(self, marks):
        
        for a, b, c in WINNING_LINES:
            if marks[a] != EMPTY and marks[a] == marks[b] == marks[c]:
                return marks[a]
        return None

    def _board_is_full(self, b):
        return all(mark != EMPTY for mark in self.cells[b])

    # Return a fast, independent copy of this game.
    def clone(self):
        
        twin = UltimateTicTacToe.__new__(UltimateTicTacToe)   # new object, skip __init__
        twin.cells = [row[:] for row in self.cells]           # copy each small board
        twin.board_result = self.board_result[:]
        twin.current_player = self.current_player
        twin.active_board = self.active_board
        twin.winner = self.winner
        return twin

    # Return every legal (board, cell) move for the current player.
    def legal_moves(self):
        
        if self.active_board is not None and self.board_result[self.active_board] == EMPTY:
            # Forced into one specific (still-playable) board.
            boards = [self.active_board]
        else:
            # Free move: any board that is still in play.
            boards = [b for b in range(9) if self.board_result[b] == EMPTY]

        moves = []
        for b in boards:
            for c in range(9):
                if self.cells[b][c] == EMPTY:
                    moves.append((b, c))
        return moves

    # Place the current player's mark. Updates board results, winner, and the next active board.
    def make_move(self, board, cell):
        
        if (board, cell) not in self.legal_moves():
            raise ValueError(f"Illegal move: board {board}, cell {cell}")

        # 1) Place the mark.
        self.cells[board][cell] = self.current_player

        # 2) Did this finish the small board (win or draw)?
        small_winner = self._line_winner(self.cells[board])
        if small_winner is not None:
            self.board_result[board] = small_winner
        elif self._board_is_full(board):
            self.board_result[board] = "D"

        # 3) Did finishing that small board win the whole game?
        big_winner = self._line_winner(self.board_result)
        if big_winner is not None:
            self.winner = big_winner
        elif all(r != EMPTY for r in self.board_result):
            self.winner = "D"   # every small board decided, no 3-in-a-row -> overall draw

        # 4) Decide where the opponent is sent next.
        #    The cell just played points at the board with that same index.
        #    If that board is finished, the opponent gets a free move (None).
        if self.board_result[cell] == EMPTY:
            self.active_board = cell
        else:
            self.active_board = None

        # 5) Hand the turn to the other player.
        self.current_player = "O" if self.current_player == "X" else "X"

    def game_over(self):
        return self.winner is not None

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------
    # What to show in a square: the mark if played, otherwise the cell number.
    def _cell_char(self, b, c):
        
        return self.cells[b][c] if self.cells[b][c] != EMPTY else str(c)

    def render(self):
        """Print the full 9x9 board with the big-board divisions drawn in."""
        lines = []
        # The big board has 3 rows of small boards (big rows 0,1,2).
        for big_row in range(3):
            # Each small board has 3 rows of cells (small rows 0,1,2).
            for small_row in range(3):
                row_pieces = []
                for big_col in range(3):
                    b = big_row * 3 + big_col            # which small board
                    base = small_row * 3                 # first cell of this small row
                    trio = " ".join(self._cell_char(b, base + i) for i in range(3))
                    row_pieces.append(" " + trio + " ")
                lines.append("|".join(row_pieces))
            if big_row < 2:
                lines.append("-" * len(lines[-1]))      # divider between rows of small boards
        print("\n".join(lines))

    # A small 3x3 showing who has WON each board.
    def board_summary(self):
        
        print("\nBoards won so far:")
        for r in range(3):
            row = []
            for cidx in range(3):
                res = self.board_result[r * 3 + cidx]
                row.append(res if res != EMPTY else ".")
            print("  " + " ".join(row))
