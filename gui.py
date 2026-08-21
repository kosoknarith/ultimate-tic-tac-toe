from tkinter import Tk, Canvas, ROUND
from ultimate_tic_tac_toe import UltimateTicTacToe
from agents import AlphaBetaAgent, DEFAULT_DEPTH

"""
Ultimate Tic-Tac-Toe -- Graphical Interface.
"""

AI_DEPTH = DEFAULT_DEPTH

BOARD_PX = 720                 # whole board is a square this many pixels on a side
CELL = BOARD_PX // 9           # one small square (80)
SMALL = BOARD_PX // 3          # one small board (240)

# Colours
X_COLOR = '#EE4035'
O_COLOR = '#0492CF'
GREEN = '#7BC043'
GRID_THIN = '#CCCCCC'
HINT_COLOR = '#E6E6E6'         # 10% black faint cell-number
GRID_THICK = '#000000'
ACTIVE_FILL = '#66BB6A'        # board you must play in acitive green
FREE_FILL = '#DCEDC8'          # playable boards on a free move
X_WON_FILL = '#FFCDD2'
O_WON_FILL = '#B3E5FC'
DRAW_FILL = '#E0E0E0'

# ------------------------------------------------------------------
# Coordinate
# ------------------------------------------------------------------
# Pixel (x, y) of the top-left corner of (board, cell)."""
def cell_top_left(board, cell):
   
    brow, bcol = divmod(board, 3)
    crow, ccol = divmod(cell, 3)
    col = bcol * 3 + ccol
    row = brow * 3 + crow
    return col * CELL, row * CELL

# Turn a pixel click into a (board, cell), or None if outside the board.
def pixel_to_move(x, y):
    
    col, row = int(x // CELL), int(y // CELL)
    if not (0 <= col < 9 and 0 <= row < 9):
        return None
    board = (row // 3) * 3 + (col // 3)
    cell = (row % 3) * 3 + (col % 3)
    return board, cell

# Pixel box (x0, y0, x1, y1) of an entire small board.
def small_board_box(board):
    
    brow, bcol = divmod(board, 3)
    x0, y0 = bcol * SMALL, brow * SMALL
    return x0, y0, x0 + SMALL, y0 + SMALL


class UltimateTicTacToeGUI:
    def __init__(self, depth=AI_DEPTH):
        self.window = Tk()
        self.window.title('Ultimate Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=BOARD_PX, height=BOARD_PX, bg='white')
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.click)

        self.human = 'X'            # you always play X and move first
        self.ai_symbol = 'O'
        self.ai = AlphaBetaAgent(depth=depth)

        self.scores = {'X': 0, 'O': 0, 'D': 0}
        self.showing_gameover = False

        self.new_game()

    def mainloop(self):
        self.window.mainloop()

    # ------------------------------------------------------------------
    # Game lifecycle
    # ------------------------------------------------------------------
    def new_game(self):
        self.game = UltimateTicTacToe()
        self.showing_gameover = False
        self.draw()

    def click(self, event):
        if self.showing_gameover:               # click on the score screen = play again
            self.new_game()
            return
        if self.game.game_over() or self.game.current_player != self.human:
            return                              # not your turn / game finished

        move = pixel_to_move(event.x, event.y)
        if move is None or move not in self.game.legal_moves():
            return                              # ignore illegal clicks

        self.game.make_move(*move)
        self.draw()
        if self.game.game_over():
            self.window.after(200, self.show_gameover)
        else:
            self.window.after(300, self.ai_turn)   # let the board repaint, then AI replies

    def ai_turn(self):
        if self.game.game_over() or self.game.current_player != self.ai_symbol:
            return
        self.game.make_move(*self.ai.choose_move(self.game))
        self.draw()
        if self.game.game_over():
            self.window.after(200, self.show_gameover)

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def draw(self):
        self.canvas.delete('all')
        self._draw_board_fills()
        self._draw_marks()
        self._draw_grid()
        self._update_title()

    # Tint backgrounds: won/drawn boards, plus the active-board highlight.
    def _draw_board_fills(self):
        
        active = self.game.active_board
        free_move = active is None
        for b in range(9):
            result = self.game.board_result[b]
            x0, y0, x1, y1 = small_board_box(b)
            fill = None
            if result == 'X':
                fill = X_WON_FILL
            elif result == 'O':
                fill = O_WON_FILL
            elif result == 'D':
                fill = DRAW_FILL
            elif not self.game.game_over():
                if free_move:
                    fill = FREE_FILL
                elif b == active:
                    fill = ACTIVE_FILL
            if fill:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline='')

    # Won boards show one big symbol; boards in play show their individual cells.
    def _draw_marks(self):
        
        for b in range(9):
            result = self.game.board_result[b]
            if result in ('X', 'O'):
                x0, y0, x1, y1 = small_board_box(b)
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                self._symbol(result, cx, cy, SMALL * 0.32, 16)
            elif result == ' ':                 # still in play
                for c in range(9):
                    mark = self.game.cells[b][c]
                    x0, y0 = cell_top_left(b, c)
                    cx, cy = x0 + CELL / 2, y0 + CELL / 2
                    if mark != ' ':
                        self._symbol(mark, cx, cy, CELL * 0.28, 8)
                    else:                       # empty: show its number as a faint hint
                        self.canvas.create_text(cx, cy, text=str(c),
                                                font='Helvetica 14', fill=HINT_COLOR)

    # Draw an X or O centred at (cx, cy) with half-size s.
    def _symbol(self, mark, cx, cy, s, thickness):
        
        if mark == 'X':
            self.canvas.create_line(cx - s, cy - s, cx + s, cy + s,
                                    width=thickness, fill=X_COLOR, capstyle=ROUND)
            self.canvas.create_line(cx - s, cy + s, cx + s, cy - s,
                                    width=thickness, fill=X_COLOR, capstyle=ROUND)
        else:
            self.canvas.create_oval(cx - s, cy - s, cx + s, cy + s,
                                    width=thickness, outline=O_COLOR)

    def _draw_grid(self):
        # Thin lines between every cell.
        for i in range(1, 9):
            self.canvas.create_line(i * CELL, 0, i * CELL, BOARD_PX, fill=GRID_THIN)
            self.canvas.create_line(0, i * CELL, BOARD_PX, i * CELL, fill=GRID_THIN)
        # Thick lines between the small boards, plus an outer border.
        for i in range(0, 4):
            self.canvas.create_line(i * SMALL, 0, i * SMALL, BOARD_PX, fill=GRID_THICK, width=4)
            self.canvas.create_line(0, i * SMALL, BOARD_PX, i * SMALL, fill=GRID_THICK, width=4)

    def _update_title(self):
        if self.game.game_over():
            return
        if self.game.current_player == self.human:
            if self.game.active_board is None:
                where = 'anywhere (free move)'
            else:
                where = f'board {self.game.active_board}'
            self.window.title(f'Ultimate Tic-Tac-Toe  --  Your turn: Play in {where}')
        else:
            self.window.title('Ultimate Tic-Tac-Toe  --  AI is thinking...')

    # ------------------------------------------------------------------
    # Game-over screen
    # ------------------------------------------------------------------
    def show_gameover(self):
        winner = self.game.winner
        self.scores[winner] += 1

        if winner == 'D':
            text, color = "It's a tie", 'gray'
        elif winner == self.human:
            text, color = 'Winner: You (X)', X_COLOR
        else:
            text, color = 'Winner: AI (O)', O_COLOR

        self.canvas.delete('all')
        self.window.title('Ultimate Tic-Tac-Toe  --  Game Over!!')
        cx = BOARD_PX / 2
        self.canvas.create_text(cx, BOARD_PX / 4, font='Helvetica 44 bold', fill=color, text=text)
        self.canvas.create_text(cx, BOARD_PX / 2 - 30, font='Helvetica 30 bold', fill=GREEN, text='Scores')

        score_text = (f'You (X) : {self.scores["X"]}\n'
                      f'AI  (O) : {self.scores["O"]}\n'
                      f'Ties    : {self.scores["D"]}')
        self.canvas.create_text(cx, BOARD_PX / 2 + 60, font='Helvetica 22 bold',
                                fill=GREEN, text=score_text)
        self.canvas.create_text(cx, BOARD_PX * 7 / 8, font='Helvetica 18',
                                fill='gray', text='Click to play again')
        self.showing_gameover = True


if __name__ == '__main__':
    UltimateTicTacToeGUI().mainloop()