from src.Kulibrat import Kulibrat, Kulibrat_console

"""
KULIBRAT GAME

Subject: Introduction to Artificial Intelligence 024000
Authors: Mikel ... (s00000), Mateo ...(s00000), 
        Guillermo Moya (s00000), Roger Sala (s00000)
Denmark Technical University
"""

# Game parameters ---------------------------------------------------
win_score = 5
# AI paramters
N_sim = 1000  # Number of simulations per move
c_param = 1  # Higher C means more exploration
epsilon = 0.2  # 0.0 means heuristic policy, 1.0 means random policy
score_depth = 5  # Depth of the score function

# ======================== PLAY THE GAME ============================

if __name__ == "__main__":  # Un/Comment to play in the UI or console
    Kulibrat(
        winning_score=win_score,
        N_sim=N_sim,
        c_param=c_param,
        epsilon=epsilon,
        score_depth=score_depth,
    )  # UI
    # Kulibrat_console(winning_score=win_score, N_sim=N_sim, c_param=c_param, score_depth=score_depth)  # Console
