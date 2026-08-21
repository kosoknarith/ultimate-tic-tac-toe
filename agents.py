import random
from ultimate_tic_tac_toe import WINNING_LINES, EMPTY

# The agent searches this many plies ahead. Deeper = stronger but slower (2 - 4).
DEFAULT_DEPTH = 4


class RandomAgent:
    name = "Random"

    def __init__(self, seed=None):
        # A random generator. Passing a seed makes games reproducible,
        # which is handy for testing and for screenshots in your report.
        self.rng = random.Random(seed)

    def choose_move(self, game):
        return self.rng.choice(game.legal_moves())


class HumanAgent:
    name = "Human"

    def choose_move(self, game):
        where = "anywhere (free move)" if game.active_board is None else f"board {game.active_board}"
        while True:
            print(f"\nPlayer {game.current_player} -- you must play in {where}.")
            raw = input("Move as 'board cell' (e.g. 4 2), or 'q' to quit: ").strip()
            if raw.lower() in ("q", "quit", "exit"):
                return None
            parts = raw.split()
            if len(parts) != 2 or not all(p.isdigit() for p in parts):
                print("  Enter two numbers 0-8 separated by a space.")
                continue
            board, cell = int(parts[0]), int(parts[1])
            if (board, cell) not in game.legal_moves():
                print("  Not legal right now -- check the active board and that the square is empty.")
                continue
            return (board, cell)

# Lines through each cell (corners 3, edges 2, center 4) -- center is most valuable
LINE_WEIGHT = [3, 2, 3, 2, 4, 2, 3, 2, 3]

WIN_SCORE = 100_000        # a decided game dwarfs any positional term

# Tunable weights for the non-terminal estimate (clearly named on purpose).
W_BOARD_WON     = 100      # winning a small board (multiplied by its position weight)
W_BIG_TWO       = 400      # owning 2 boards on a big-board line with the 3rd still open
W_SMALL_TWO     = 4        # a two-in-a-row threat inside an unfinished small board
W_SMALL_CENTER  = 3        # holding the center cell of an unfinished small board


def _other(player):
    return "O" if player == "X" else "X"

# Count lines in a 3x3 where `me` has exactly 2 marks and the 3rd cell is empty.
def _two_in_line(marks, me):
    
    count = 0
    for a, b, c in WINNING_LINES:
        trio = (marks[a], marks[b], marks[c])
        if trio.count(me) == 2 and trio.count(EMPTY) == 1:
            count += 1
    return count

# Count big-board lines where `me` owns 2 boards and the 3rd is still winnable.
def _big_line_potential(board_result, me):
    
    count = 0
    for a, b, c in WINNING_LINES:
        trio = (board_result[a], board_result[b], board_result[c])
        if trio.count(me) == 2 and trio.count(EMPTY) == 1:   # 'D' (drawn) would block the line
            count += 1
    return count

# Estimate how good `game` is for player `me`. Positive = good for me.
def evaluate(game, me):
    
    opp = _other(me)

    # Decided games are easy: huge values so the search always prefers winning.
    if game.winner is not None:
        if game.winner == me:
            return WIN_SCORE
        if game.winner == opp:
            return -WIN_SCORE
        return 0                      # overall draw

    score = 0
    br = game.board_result

    # (1) Small boards already won, weighted by how strategically placed they are.
    for b in range(9):
        if br[b] == me:
            score += W_BOARD_WON * LINE_WEIGHT[b]
        elif br[b] == opp:
            score -= W_BOARD_WON * LINE_WEIGHT[b]

    # (2) Near-wins on the BIG board (two boards in a line, third still open).
    score += W_BIG_TWO * (_big_line_potential(br, me) - _big_line_potential(br, opp))

    # (3) Tactics inside boards still in play: two-in-a-rows and center control.
    for b in range(9):
        if br[b] == EMPTY:
            cells = game.cells[b]
            score += W_SMALL_TWO * (_two_in_line(cells, me) - _two_in_line(cells, opp))
            if cells[4] == me:
                score += W_SMALL_CENTER
            elif cells[4] == opp:
                score -= W_SMALL_CENTER

    return score


class MinimaxAgent:
    name = "Minimax"

    def __init__(self, depth=3, seed=None):
        self.depth = depth
        self.rng = random.Random(seed)
        self.nodes = 0          # positions visited in the last search

    def choose_move(self, game):
        self.nodes = 0
        me = game.current_player
        best_value = None
        best_moves = []
        for move in game.legal_moves():
            child = game.clone()
            child.make_move(*move)
            value = self._search(child, self.depth - 1, me)
            if best_value is None or value > best_value:
                best_value, best_moves = value, [move]
            elif value == best_value:
                best_moves.append(move)          # collect ties...
        return self.rng.choice(best_moves)        # break them randomly for variety
    
    # Standard minimax: maximize on `me`'s turn, minimize on the opponent's.
    def _search(self, game, depth, me):
        
        self.nodes += 1
        if game.game_over() or depth == 0:
            return evaluate(game, me)

        if game.current_player == me:             # MAX node
            best = float("-inf")
            for move in game.legal_moves():
                child = game.clone()
                child.make_move(*move)
                best = max(best, self._search(child, depth - 1, me))
            return best
        else:                                     # MIN node
            best = float("inf")
            for move in game.legal_moves():
                child = game.clone()
                child.make_move(*move)
                best = min(best, self._search(child, depth - 1, me))
            return best

class AlphaBetaAgent:
    name = "AlphaBeta"

    def __init__(self, depth=3, seed=None):
        self.depth = depth
        self.rng = random.Random(seed)
        self.nodes = 0          # positions visited in the last search

    def choose_move(self, game):
        self.nodes = 0
        me = game.current_player
        alpha, beta = float("-inf"), float("inf")
        best_value = float("-inf")
        best_moves = []
        for move in game.legal_moves():
            child = game.clone()
            child.make_move(*move)
            value = self._search(child, self.depth - 1, alpha, beta, me)
            if value > best_value:
                best_value, best_moves = value, [move]
            elif value == best_value:
                best_moves.append(move)
            alpha = max(alpha, best_value)      # tighten our lower bound as we find better moves
        return self.rng.choice(best_moves)

    def _search(self, game, depth, alpha, beta, me):
        self.nodes += 1
        if game.game_over() or depth == 0:
            return evaluate(game, me)

        if game.current_player == me:           # MAX node
            value = float("-inf")
            for move in game.legal_moves():
                child = game.clone()
                child.make_move(*move)
                value = max(value, self._search(child, depth - 1, alpha, beta, me))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break                        # beta cutoff MIN won't allow this branch
            return value
        else:                                    # MIN node
            value = float("inf")
            for move in game.legal_moves():
                child = game.clone()
                child.make_move(*move)
                value = min(value, self._search(child, depth - 1, alpha, beta, me))
                beta = min(beta, value)
                if beta <= alpha:
                    break                        # alpha cutoff MAX won't allow this branch
            return value

