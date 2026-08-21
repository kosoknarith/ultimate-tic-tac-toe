# Ultimate Tic-Tac-Toe

A command-line and graphical Ultimate Tic-Tac-Toe game with an bot opponent built
on classical adversarial search: minimax, alpha-beta pruning, and a
heuristic evaluation function



# Quick Start:

## Run any of these from inside the project folder:
------------------------------------------------------------------------------

python3 main.py        # play in the terminal — you are X vs the AI
python3 gui.py         # play in a window — graphical version of the same game
python3 benchmark.py   # minimax vs alpha-beta: prints the node-count comparison
python3 winrate.py     # minimax vs random: prints the win rate over 100 games
python3 test_engine.py # validates the game rules over 20,000 random games

## How It Works
------------------------------------------------------------------------------

The game. Ultimate Tic-Tac-Toe is nine small Tic-Tac-Toe boards inside one
big board. Win a small board to claim its square; claim three squares in a row to
win. The "forcing rule" makes it strategic: the cell you play in decides which
board your opponent must play in next.

# How The Board Is Numbered
------------------------------------------------------------------------------
There is one big 3x3 board. Each of its 9 cells is itself a small 3x3 board.
Both the big board and every small board use the SAME numbering, 0-8, row by row:

        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8

So a move is two numbers: (board, cell)
  - board = which small board (0-8)
  - cell  = which square inside that small board (0-8)

# The Forcing Rule
------------------------------------------------------------------------------
The CELL you play in decides which BOARD your opponent must play in next.
Example: if you play in cell 4 of any board, your opponent must play next
inside small board 4.

Exception: if the board they are sent to is already finished (won or full),
they get a "free move" and may play in any board that still has empty cells.

You win a small board the normal way: 3 in a row inside it.
You win the GAME by winning 3 small boards in a row on the big board.
