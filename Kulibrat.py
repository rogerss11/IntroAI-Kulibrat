import time
from GameState import GameState
from Board import Board

def Kulibrat():
    game = GameState()
    ui = Board(game)
    print("Welcome to Kulibrat!")
    #game.init_ventana()
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


Kulibrat()
