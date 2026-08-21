import time
from ultimate_tic_tac_toe import UltimateTicTacToe
from agents import MinimaxAgent, AlphaBetaAgent


def measure(agent, game):
    start = time.time()
    agent.choose_move(game)
    return agent.nodes, time.time() - start


def main():
    game = UltimateTicTacToe()        # benchmark from the opening position
    print(f"{'Depth':>5} | {'Minimax nodes':>14} | {'Alpha-beta nodes':>16} | {'Pruned':>7} | {'Speed-up':>8}")
    print("-" * 64)
    for depth in (2, 3, 4):
        mm_nodes, mm_t = measure(MinimaxAgent(depth=depth, seed=0), game)
        ab_nodes, ab_t = measure(AlphaBetaAgent(depth=depth, seed=0), game)
        pruned = 100 * (mm_nodes - ab_nodes) / mm_nodes
        speedup = mm_nodes / ab_nodes
        print(f"{depth:>5} | {mm_nodes:>14,} | {ab_nodes:>16,} | {pruned:>6.1f}% | {speedup:>7.1f}x")


if __name__ == "__main__":
    main()
