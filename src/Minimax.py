import math


def evaluate_state(state, player):
    opponent = "B" if player == "R" else "R"

    score_diff = state.score[player] - state.score[opponent]
    remaining_diff = state.remaining_pieces[opponent] - state.remaining_pieces[player]

    actions = state.find_actions()
    my_actions = actions[player]
    opp_actions = actions[opponent]

    scoring_moves = [a for a in my_actions if a[2] == (-1, -1)]
    opponent_scoring_moves = [a for a in opp_actions if a[2] == (-1, -1)]

    attack_moves = [a for a in my_actions if a[0] == "attack"]
    under_attack = [a for a in opp_actions if a[0] == "attack" and a[2] != (-1, -1)]

    pass_penalty = -3 if my_actions == [("pass", (-1, -1), (-1, -1))] else 0

    evaluation = (
        score_diff * 10
        + len(scoring_moves) * 6
        - len(opponent_scoring_moves) * 4
        + len(attack_moves) * 5
        - len(under_attack) * 2
        + remaining_diff * 1.5
        + (len(my_actions) - len(opp_actions)) * 0.5
        + pass_penalty
    )

    return evaluation


def minimax(state, depth, alpha, beta, maximizing_player, player_id):
    if depth == 0 or state.terminal_test():
        return evaluate_state(state, player_id), None

    current_player = state.player
    legal_actions = state.find_actions()[current_player]

    if not legal_actions:
        return evaluate_state(state, player_id), None

    best_action = None

    if maximizing_player:
        max_eval = -math.inf
        for action in legal_actions:
            next_state = state.clone_state()
            next_state.move(action)
            eval_score, _ = minimax(
                next_state, depth - 1, alpha, beta, False, player_id
            )
            if eval_score > max_eval:
                max_eval = eval_score
                best_action = action
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_action
    else:
        min_eval = math.inf
        for action in legal_actions:
            next_state = state.clone_state()
            next_state.move(action)
            eval_score, _ = minimax(next_state, depth - 1, alpha, beta, True, player_id)
            if eval_score < min_eval:
                min_eval = eval_score
                best_action = action
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_action


def minimax_search(state, depth=5):
    # Adaptive depth
    pieces_on_board = sum(
        1 for row in state.board for cell in row if cell in ["B", "R"]
    )
    if pieces_on_board >= 6:
        depth += 1
    _, best_action = minimax(state, depth, -math.inf, math.inf, True, state.player)
    return best_action
