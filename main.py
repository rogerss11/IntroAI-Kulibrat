from src.Kulibrat import Kulibrat, Kulibrat_console

"""
KULIBRAT GAME

Subject: Introduction to Artificial Intelligence 02180
Authors: Mikel Fernandez (s243273), Mateo de Assas (s243328), 
        Guillermo Moya (s243295), Roger Sala (s243328)
Denmark Technical University
"""
# ======================== GAME PARAMETERS ============================

# Game parameters
win_score = 5

# Select AI type
ai_type = "mmx"  # "mmx" or "mcts"

# Minimax parameters:
search_depth = 7  # Higher means better but slower AI

# Monte Carlo parameters:
N_sim = 100
c_param = 1.4

# ======================== PLAY THE GAME ============================

if __name__ == "__main__":  # Un/Comment to play in the UI or console
    Kulibrat(
        winning_score=win_score,
        ai=ai_type,
        N_sim=N_sim,
        c_param=c_param,
        search_depth=search_depth,
    )  # UI
    """
    Kulibrat_console(
        winning_score=win_score,
        ai=ai_type,
        N_sim=N_sim,
        c_param=c_param,
        search_depth=search_depth,
    )    # Console"
    """
