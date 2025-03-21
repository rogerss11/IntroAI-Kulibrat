import time
from GameState import GameState
from Interface import *
import numpy as np
from minimax import minimax_search


def Kulibrat(winning_score=5, N_sim=500, c_param=0.5):
    player1_type = question_ai_red()
    player2_type = question_ai_black()

    game = GameState(winning_score=winning_score)
    ui = Board(game)
    print("Welcome to Kulibrat!")

    while not game.terminal_test():
        ui.print_actions(game)

        if game.player == "R":  # If it's player 1's turn
            if player1_type == "human":
                action_idx = ui.get_input(player1_type)
                game.move(game.actions[game.player][action_idx])
                if action_idx >= len(game.actions[game.player]):
                    print("Invalid action!")
                    continue
            elif player1_type == "random":
                action_idx = np.random.randint(0, len(game.actions[game.player]))
                game.move(game.actions[game.player][action_idx])
                time.sleep(0.5)
            elif player1_type == "ai":
                # AI intelligence
                action = minimax_search(game, depth=4)
                game.move(action)
                time.sleep(0.5)

        else:  # If it's player 2's turn
            if player2_type == "human":
                action_idx = ui.get_input(player2_type)
                game.move(game.actions[game.player][action_idx])
                if action_idx >= len(game.actions[game.player]):
                    print("Invalid action!")
                    continue
            elif player2_type == "random":
                action_idx = np.random.randint(0, len(game.actions[game.player]))
                game.move(game.actions[game.player][action_idx])
                time.sleep(0.5)
            elif player2_type == "ai":
                action = minimax_search(game, depth=4)
                game.move(action) 
                time.sleep(0.5)

        ui.UI_board(game)
        ui.window.update_idletasks()
        ui.window.update()
        time.sleep(0.1)

    ui.on_close()
    end_game(game.winner)
    print("Game over!")
    print(f"Winner: {game.winner}")
    return


def Kulibrat_console(winning_Score=5, N_sim=100, c_param=1.4):
    game = GameState(winning_score=winning_Score)

    # Ask the user for player types
    print("Before starting, choose the player types.")
    player1_type = ask_player_type(1)  # Type of player 1
    player2_type = ask_player_type(2)  # Type of player 2

    print("The players have been selected.")
    print(f"Player 1: {player1_type}")
    print(f"Player 2: {player2_type}")

    while not game.terminal_test():
        game.print_actions()

        if game.player == "R":  # If it's player 1's turn
            if player1_type == "human":
                action_idx = int(input("Player 1, enter the action index: "))
                game.move(game.actions[game.player][action_idx])
                if action_idx >= len(game.actions[game.player]):
                    print("Invalid action!")
                    continue
            elif player1_type == "random":
                action_idx = np.random.randint(0, len(game.actions[game.player]))
                game.move(game.actions[game.player][action_idx])
            elif player1_type == "ai":
                # AI intelligence
                action = minimax_search(game, depth=3)
                game.move(action)

        else:  # If it's player 2's turn
            if player2_type == "human":
                action_idx = int(input("Player 2, enter the action index: "))
                game.move(game.actions[game.player][action_idx])
                if action_idx >= len(game.actions[game.player]):
                    print("Invalid action!")
                    continue
            elif player2_type == "random":
                action_idx = np.random.randint(0, len(game.actions[game.player]))
                game.move(game.actions[game.player][action_idx])
            elif player2_type == "ai":
                action = minimax_search(game, depth=3)
                game.move(action)

        game.print_board()
        time.sleep(0.1)

    print("Game over!")
    print(f"Winner: {game.winner}")


if __name__ == "__main__":  # Un/Comment to play in the UI or console
    Kulibrat()
    # Kulibrat_console()
