import numpy as np
from collections import defaultdict

from GameState import GameState

"""
Code inspired from:
https://ai-boson.github.io/mcts/
"""


class MonteCarloSearch:
    def __init__(self, game, parent=None, parent_action=None):
        self.state = game.clone_state()
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        """
        Returns the untried actions for the current state.
        """
        all_actions = self.state.find_actions()
        self._untried_actions = all_actions[self.state.player]
        return self._untried_actions

    def q(self):
        """
        Returns the difference between the number of wins - loses.
        """
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        """
        Returns the number of times each node is visited.
        """
        return self._number_of_visits

    def expand(self):
        """
        The states which are possible from the present state are all generated
        and the child_node corresponding to this generated state is returned.
        """
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloSearch(next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        """
        Returns True if the current node is a terminal node.
        """
        return self.state.terminal_test()

    def rollout(self):
        """
        The entire game is simulated from the current state to the end.
        The final result (utility) of the game is returned. +1, -1 or 0.
        Light playout policy.
        """
        current_rollout_state = self.state.clone_state()

        while not current_rollout_state.terminal_test():
            all_actions = current_rollout_state.find_actions()
            possible_moves = all_actions[current_rollout_state.player]
            action = self.rollout_policy(possible_moves)
            current_rollout_state.move(action)
        return current_rollout_state.utility

    def backpropagate(self, result):
        """
        The node statistics are updated.
        The result of the playout is backpropagated from the tree to the root.
        """
        self._number_of_visits += 1
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        """
        All the actions are poped out of _untried_actions one by one.
        When it becomes empty (the size is zero) it is fully expanded.
        """
        return len(self._untried_actions) == 0

    def best_child(self, c_param=1.4):
        """
        The childs are evaluated using the UCB1 formula.
        The child with the highest value is returned.
        """
        choices_weights = [
            (c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n()))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        """
        Function to select a move from the possible moves.
        In this case, a random move is selected.
        """
        return possible_moves[np.random.randint(len(possible_moves))]

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
        simulation_no = 100

        for i in range(simulation_no):

            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=1.4)


def monte_carlo(state):
    root = MonteCarloSearch(state=state)
    selected_node = root.best_action()
    return selected_node.parent_action
