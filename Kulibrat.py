import time
from GameState import GameState
from Board import Board
import numpy as np
from MonteCarlo import monte_carlo_search

### REVISAR LA IA, NO ESTA FUNCIONANDO BIEN ###
# creo que juega a perder xd


def Kulibrat():  # -----------------------------------------------------------
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


def Kulibrat_console_simple():  # -------------------------------------------
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


def ask_player_type(player_num):
    """Function to ask the user what type of player they want to be."""
    player_color = "B" if player_num == 1 else "R"
    while True:
        choice = input(
            f"What type of player will player {player_num} ({player_color}) be? (AI/random/human): "
        ).lower()
        if choice in ["ai", "random", "human"]:
            return choice
        else:
            print("Invalid choice, please choose between AI, random, or human.")


def Kulibrat_console():  # -------------------------------------------------
    game = GameState(winning_score=5)

    # Ask the user for player types
    print("Before starting, choose the player types.")
    player1_type = ask_player_type(1)  # Type of player 1
    player2_type = ask_player_type(2)  # Type of player 2

    print("The players have been selected.")
    print(f"Player 1 (B): {player1_type}")
    print(f"Player 2 (R): {player2_type}")

    while not game.terminal_test():
        game.print_actions()

        if game.player == "B":  # If it's player 1's turn
            if player1_type == "human":
                action_idx = int(input("Player 1, enter the action index: "))
                if action_idx > len(
                    game.actions[game.player]
                ):  # Esto no estoy seguro que este bien hecho
                    print("Invalid action!")  #
                    continue  #
                game.move(game.actions[game.player][action_idx])  #
            elif player1_type == "random":
                action_idx = np.random.randint(0, len(game.actions[game.player]))
                game.move(game.actions[game.player][action_idx])
            elif player1_type == "ai":
                # AI intelligence
                action = monte_carlo_search(game, 1000)
                game.move(action)

        else:  # If it's player 2's turn
            if player2_type == "human":
                action_idx = int(input("Player 2, enter the action index: "))
                game.move(game.actions[game.player][action_idx])
                if action_idx > len(game.actions[game.player]):
                    print("Invalid action!")
                    continue
            elif player2_type == "random":
                action_idx = np.random.randint(0, len(game.actions[game.player]))
                game.move(game.actions[game.player][action_idx])
            elif player2_type == "ai":
                action = monte_carlo_search(game, 1000)
                game.move(action)

        game.print_board()
        time.sleep(0.1)

    print("Game over!")
    print(f"Winner: {game.winner}")


# Kulibrat()
# Kulibrat_console_simple()
Kulibrat_console()
