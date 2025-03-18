import time
from GameState import GameState
import tkinter as tk


def Kulibrat():
    game = GameState()
    print("Welcome to Kulibrat!")
    game.init_ventana()
    while not game.terminal_test():
        game.print_actions()
        action_idx = game.get_input()
        if action_idx >= len(game.actions[game.player]):
            print("Invalid action!")
            continue
        game.move(game.actions[game.player][int(action_idx)])
        game.UI_board()
        time.sleep(0.1)
    print("Game over!")
    print(f"Winner: {game.winner}")
    return


Kulibrat()
