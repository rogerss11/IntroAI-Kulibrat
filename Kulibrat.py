from GameState import GameState
from Board import Board
import numpy as np

def ask_player_type(player_num):
    """Function to ask the user what type of player they want to be."""
    while True:
        choice = input(f"What type of player will player {player_num} be? (AI/random/human): ").lower()
        if choice in ["ai", "random", "human"]:
            return choice
        else:
            print("Invalid choice, please choose between AI, random, or human.")

def Kulibrat_console():
    game = GameState(winning_score=1)

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
                #AI intelligence
                action= monte_carlo_search(game)
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
                # Here you could add logic for AI intelligence
                action= monte_carlo_search(game)
                game.move(action)

        game.print_board()
        time.sleep(0.1)
    
    print("Game over!")
    print(f"Winner: {game.winner}")

Kulibrat_console()
