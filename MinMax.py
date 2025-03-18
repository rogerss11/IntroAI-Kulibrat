from GameState import GameState

import copy


class MiniMax:
    def __init__(self, game=None):
        self.game = game.clone_state()
        self.search_depth = 0

    def minimax_search(self):  # Basic Minimax algorithm ---------------------
        gc = self.game.clone_state()
        utility, action = self.max_value()
        return utility, action

    def max_value(self):  # MAX-VALUE(game, state) ---------------------------
        gc = self.game.clone_state()
        if gc.terminal_test():
            return gc.utility, None
        v = -float("inf")
        move = None
        for a in gc.actions[gc.player]:
            gc2 = gc.clone_state()
            gc2.move(a)
            v2, a2 = self.min_value()
            self.search_depth += 1
            if v2 > v:
                v, move = v2, a
        return v, move

    def min_value(self):  # MIN-VALUE(game, state ----------------------------)
        gc = self.game.clone_state()
        if gc.terminal_test():
            return gc.utility, None
        v = float("inf")
        move = None
        for a in gc.actions[gc.player]:
            gc2 = gc.clone_state()
            gc2.move(a)
            v2, a2 = self.max_value()
            self.search_depth += 1

            if v2 < v:
                v, move = v2, a
        return v, move

    def ab_max_value(
        self, alpha=-float("inf"), beta=float("inf")
    ):  # MAX-VALUE(game, state, alpha, beta)
        gc = self.game.clone_state()
        if gc.terminal_test():
            return gc.utility, None
        v = -float("inf")
        move = None
        for a in gc.actions[gc.player]:
            gc2 = gc.clone_state()
            gc2.move(a)
            v2, a2 = self.min_value(alpha, beta)
            self.search_depth += 1
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def ab_min_value(
        self, alpha=-float("inf"), beta=float("inf")
    ):  # MIN-VALUE(game, state, alpha, beta)
        gc = self.game.clone_state()
        if gc.terminal_test():
            return gc.utility, None
        v = float("inf")
        move = None
        for a in gc.actions[gc.player]:
            gc2 = gc.clone_state()
            gc2.move(a)
            v2, a2 = self.max_value(alpha, beta)
            self.search_depth += 1
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move


game = GameState()
game.board = [["B", 0, "B"], [0, "B", 0], ["R", "B", "R"], ["R", 0, 0]]
game.print_board()
print("u=", game.utility)
game.find_actions()
gc = copy.deepcopy(game)
mmx = MiniMax(game=gc)
game.print_actions()
u, action = mmx.minimax_search()
print(mmx.search_depth)
print(u)
print(action)
game.move(action)
game.print_board()
game.find_actions()
gc = copy.deepcopy(game)
mmx = MiniMax(game=gc)
game.print_actions()
u, action = mmx.minimax_search()
print(mmx.search_depth)
print(action)
