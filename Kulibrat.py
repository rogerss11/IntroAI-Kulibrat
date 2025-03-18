import time
from GameState import GameState
from Board import Board
import numpy as np


def Kulibrat():
    game = GameState(winning_score=1)
    ui = Board(game)
    print("Welcome to Kulibrat!")
    while not game.terminal_test():
        ui.print_actions(game)
        action_idx = ui.get_input()
        if action_idx >= len(game.actions[game.player]):
            print("Invalid action!")
            continue
        game.move(game.actions[game.player][int(action_idx)])
        ui.UI_board(game)
        time.sleep(0.1)
    print("Game over!")
    print(f"Winner: {game.winner}")
    return


def Kulibrat_console():
    game = GameState(winning_score=1)
    print("Welcome to Kulibrat!")
    while not game.terminal_test():
        game.print_actions()
        if game.player == "R":
            action_idx = int(input("Enter action index: "))
            if action_idx >= len(game.actions[game.player]):
                print("Invalid action!")
                continue
            game.move(game.actions[game.player][int(action_idx)])
        else:
            action_idx = np.random.randint(0, len(game.actions[game.player]))
            game.move(game.actions[game.player][int(action_idx)])
        game.print_board()
        time.sleep(0.1)
    print("Game over!")
    print(f"Winner: {game.winner}")
    return


# Kulibrat()
Kulibrat_console()
