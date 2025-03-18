from GameState import GameState

def alpha_beta_search(game: GameState):
    player = game.player  # El jugador actual
    # Ejecutamos MAX-VALUE para obtener la mejor acción para el jugador
    value, move = max_value(game, game, float('-inf'), float('inf'))
    return move

def max_value(game: GameState, state, alpha, beta):
    # Si el estado es terminal (fin del juego), devolvemos su valor y ninguna jugada
    if game.terminal_test():
        return game.utility(), None  # Deberías implementar la función `utility` en GameState

    v = float('-inf')
    best_move = None
    # Iteramos sobre todas las acciones posibles
    for action in game.actions[state.player]:
        # Aplicamos la acción y obtenemos el siguiente estado
        new_state = game.result(state, action)
        v2, _ = min_value(game, new_state, alpha, beta)  # Llamada a min_value para explorar el siguiente nivel
        
        if v2 > v:
            v, best_move = v2, action
        
        # Podamos ramas del árbol
        alpha = max(alpha, v)
        if v >= beta:
            return v, best_move  # Podamos, ya no necesitamos explorar más esta rama
    
    return v, best_move

def min_value(game: GameState, state, alpha, beta):
    # Si el estado es terminal (fin del juego), devolvemos su valor y ninguna jugada
    if game.terminal_test():
        return game.utility(), None  # Deberías implementar la función `utility` en GameState
    
    v = float('inf')
    best_move = None
    # Iteramos sobre todas las acciones posibles
    for action in game.actions[state.player]:
        # Aplicamos la acción y obtenemos el siguiente estado
        new_state = game.result(state, action)
        v2, _ = max_value(game, new_state, alpha, beta)  # Llamada a max_value para explorar el siguiente nivel
        
        if v2 < v:
            v, best_move = v2, action
        
        # Podamos ramas del árbol
        beta = min(beta, v)
        if v <= alpha:
            return v, best_move  # Podamos, ya no necesitamos explorar más esta rama
    
    return v, best_move
