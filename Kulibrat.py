from GameState import GameState
from AI_Player import alpha_beta_search  # Archivo donde estará la función

def Kulibrat():
    game = GameState()
    print("Welcome to Kulibrat!")
    game.print_board()

    while not game.terminal_test():
        if game.player == "AI":  # Si el jugador actual es la IA
            action = alpha_beta_search(game)  # Llamamos a Alpha-Beta para que la IA elija el movimiento
            print(f"AI selects: {action}")
        else:
            game.print_actions()
            action_idx = input("Select action: ")
            if action_idx >= str(len(game.actions[game.player])):
                print("Invalid action!")
                continue
            action = game.actions[game.player][int(action_idx)]
        
        game.move(action)  # Ejecutamos el movimiento
        game.print_board()
    
    print("Game over!")
    print(f"Winner: {game.winner}")
