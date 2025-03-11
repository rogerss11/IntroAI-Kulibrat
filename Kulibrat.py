import time
from GameState import GameState


def Kulibrat():
    game = GameState()
    print("Welcome to Kulibrat!")
    game.print_board()
    while not game.terminal_test():
        game.print_actions()
        action_idx = input("Select action: ")
        if action_idx >= str(len(game.actions[game.player])):
            print("Invalid action!")
            continue
        game.move(game.actions[game.player][int(action_idx)])
        game.print_board()
        time.sleep(0.1)
    print("Game over!")
    print(f"Winner: {game.winner}")
    return


Kulibrat()
