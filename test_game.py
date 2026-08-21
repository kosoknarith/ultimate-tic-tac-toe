import random, collections
from ultimate_tic_tac_toe import UltimateTicTacToe, WINNING_LINES, EMPTY

def verify_terminal(g):
    # Recompute the winner independently and confirm it matches the engine.
    def line_win(marks):
        for a,b,c in WINNING_LINES:
            if marks[a]!=EMPTY and marks[a]==marks[b]==marks[c]:
                return marks[a]
        return None
    big = line_win(g.board_result)
    if big is not None:
        assert g.winner == big, f"winner mismatch {g.winner} vs {big}"
    elif all(r!=EMPTY for r in g.board_result):
        assert g.winner == "D", f"expected draw, got {g.winner}"
    else:
        assert g.winner is None, "game not actually over"

def forcing_rule_ok(g, last_cell):
    # After a move in `last_cell`, the next active board must be last_cell
    # unless that board is finished (then free move = None).
    if g.board_result[last_cell] == EMPTY:
        assert g.active_board == last_cell
    else:
        assert g.active_board is None

results = collections.Counter()
for _ in range(20000):
    g = UltimateTicTacToe()
    while not g.game_over():
        moves = g.legal_moves()
        assert moves, "no legal moves but game not over"
        b, c = random.choice(moves)
        g.make_move(b, c)
        forcing_rule_ok(g, c)
    verify_terminal(g)
    results[g.winner] += 1

print("20000 random games completed with no rule violations.")
print("Outcomes:", dict(results))