import numpy as np
from collections import defaultdict
import random

"""
Code inspired from:
https://ai-boson.github.io/mcts/
"""


class MonteCarlo:
    def __init__(self, game, parent=None, parent_action=None, c_param=0.5, sim_no=500):
        self.state = game.clone_state()
        self.player = self.state.player
        self.opponent = "B" if self.player == "R" else "R"
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        self._c = c_param
        self._sim_no = sim_no
        return

    def untried_actions(self):
        """
        Returns the untried actions for the current state.
        """
        all_actions = self.state.find_actions()
        self._untried_actions = all_actions[self.state.player]
        return self._untried_actions

    def q(self):  # U(n)
        """
        Returns the difference between the number of wins - loses.
        """
        wins = self._results[1]
        loses = self._results[-1]
        return self._results["sum"] / self._number_of_visits

    def n(self):  # N(n)
        """
        Returns the number of times each node is visited.
        """
        return self._number_of_visits

    def expand(self):
        """
        The states which are possible from the present state are all generated
        and the child_node corresponding to this generated state is returned.
        """
        if not self._untried_actions:
            return None

        action = self._untried_actions.pop()
        next_state = self.state.clone_state()
        next_state.move(action)

        child_node = MonteCarlo(
            next_state,
            parent=self,
            parent_action=action,
            c_param=self._c,
            sim_no=self._sim_no,
        )

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        """
        Returns True if the current node is a terminal node.
        """
        return self.state.terminal_test()

    def is_scoring_move(self, action):
        move, start, end = action
        return move in ["diagonal", "jump"] and end == (-1, -1)

    def is_forward_move(self, action):
        move, start, end = action
        if move in ["insert", "pass"]:
            return False
        if end == (-1, -1):
            return True
        start_row, _ = start
        end_row, _ = end
        return (self.player == "B" and end_row > start_row) or (
            self.player == "R" and end_row < start_row
        )

    def rollout(self):
        """
        The entire game is simulated from the current state to the end.
        The final result (score) of the game is returned (Player score - Opponent score).
        Light playout policy.
        """
        current_rollout_state = self.state.clone_state()

        while not current_rollout_state.terminal_test():
            all_actions = current_rollout_state.find_actions()
            possible_moves = all_actions[current_rollout_state.player]
            action = self.rollout_policy(possible_moves)
            current_rollout_state.move(action)

        if current_rollout_state.winner == self.player:
            return 1
        elif current_rollout_state.winner == self.opponent:
            return -1
        elif current_rollout_state.terminal_test():
            return -0.5
        else:
            return (
                current_rollout_state.score[self.player]
                - current_rollout_state.score[self.opponent]
            ) / self.state.winning_score

    def backpropagate(self, result):
        """
        The node statistics are updated.
        The result of the playout is backpropagated from the tree to the root.
        """
        self._results["sum"] += result
        self._number_of_visits += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        """
        All the actions are poped out of _untried_actions one by one.
        When it becomes empty (the size is zero) it is fully expanded.
        """
        return len(self._untried_actions) == 0

    def best_child(self):
        """
        The childs are evaluated using the UCB1 formula.
        The child with the highest value is returned.
        UCB1 = U(n) / N(n) + c * sqrt(ln(N(parent_n)) / N(n))
        """
        for child in self.children:
            if child.is_terminal_node() and child.state.winner == self.player:
                return child  # Ganar inmediatamente
        choices_weights = [
            child.q() + self._c * np.sqrt(np.log(self.n()) / (child.n() + 1e-6))
            for child in self.children
        ]

        if np.random.rand() < 0.05:
            chosen = np.random.choice(self.children)
            return chosen

        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        """
        Function to select a move from the possible moves.
        In this case, a random move is selected.
        """
        scoring = [a for a in possible_moves if self.is_scoring_move(a)]
        attacking = [a for a in possible_moves if a[0] == "attack"]
        jumping = [a for a in possible_moves if a[0] == "jump"]
        forward = [a for a in possible_moves if self.is_forward_move(a)]

        for prioritized in [scoring, attacking, jumping, forward]:
            if prioritized:
                return random.choice(prioritized)
        return random.choice(possible_moves)

    def _tree_policy(self):
        """
        Select a node to run rollout from.
        """
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            current_node = current_node.best_child()
        return current_node

    def best_action(self):
        """
        Returns the node corresponding to the best possible move
        For all the simulations: run the tree policy, rollout and backpropagate.
        """
        simulation_no = self._sim_no

        for i in range(simulation_no):

            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child()


def monte_carlo_search(state, sim_no=100, c_param=1.4):
    root = MonteCarlo(state, sim_no=sim_no, c_param=c_param)
    selected_node = root.best_action()
    print("Number of visits: ", root._number_of_visits)
    print("Results: ", root._results)
    return selected_node.parent_action
