
from ultimate_tic_tac_toe import UltimateTicTacToe
from agents import HumanAgent, AlphaBetaAgent, DEFAULT_DEPTH

# Play one full game. agent_x plays X, agent_o plays O. Returns the winner.
def play_game(agent_x, agent_o, show=True):
    
    game = UltimateTicTacToe()
    players = {"X": agent_x, "O": agent_o}

    while not game.game_over():
        if show:
            print("\n" + "=" * 41)
            game.render()
            game.board_summary()

        mover = players[game.current_player]
        move = mover.choose_move(game)
        if move is None:            # human chose to quit
            print("Game quit.")
            return None

        if show and not isinstance(mover, HumanAgent):
            print(f"\n{mover.name} ({game.current_player}) plays {move[0]} {move[1]}.")

        game.make_move(*move)

    if show:
        print("\n" + "=" * 41)
        game.render()
        game.board_summary()
        if game.winner == "D":
            print("\nResult: it's a draw.")
        else:
            print(f"\nResult: Player {game.winner} wins!")
    return game.winner

# Ask the user to pick one of `options`. Returns the choice.
def _choose(prompt, options):
    
    options = [o.lower() for o in options]
    while True:
        pick = input(f"{prompt} [{'/'.join(options)}]: ").strip().lower()
        if pick in options:
            return pick
        print(f"  Please type one of: {', '.join(options)}.")


def main():
    print("Ultimate Tic-Tac-Toe\n")
    print(f"  (AI is alpha-beta searching {DEFAULT_DEPTH} moves ahead)")

    side = _choose("Play as X (first) or O", ["X", "O"])
    human, ai = HumanAgent(), AlphaBetaAgent(depth=DEFAULT_DEPTH)
    if side == "x":
        play_game(human, ai)
    else:
        play_game(ai, human)


if __name__ == "__main__":
    main()
