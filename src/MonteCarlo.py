import numpy as np
from collections import defaultdict
import random

"""
Code inspired from:
https://ai-boson.github.io/mcts/
"""


class MonteCarlo:
    def __init__(
        self,
        game,
        parent=None,
        parent_action=None,
        c_param=1,
        sim_no=100,
        epsilon=0.1,
    ):
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
        self._epsilon = epsilon
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
        Returns the score difference.
        """
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

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
        action = self._untried_actions.pop()
        next_state = self.state.clone_state()
        next_state.move(action)
        child_node = MonteCarlo(
            next_state,
            parent=self,
            parent_action=action,
            c_param=self._c,
            sim_no=self._sim_no,
            epsilon=self._epsilon,
        )

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
        The final result (score) of the game is returned (Player score - Opponent score).
        Light playout policy.
        """
        current_rollout_state = self.state.clone_state()

        while not current_rollout_state.terminal_test():
            all_actions = current_rollout_state.find_actions()
            possible_moves = all_actions[current_rollout_state.player]
            action = self.rollout_policy(possible_moves)
            current_rollout_state.move(action)

        score = 1 if current_rollout_state.winner == self.player else -1
        return score

    def backpropagate(self, result):
        """
        The node statistics are updated.
        The result of the playout is backpropagated from the tree to the root.
        """
        if result > 0:
            self._results[+1] += abs(result)
        else:
            self._results[-1] += abs(result)
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
        Returns the best child node based on the UCB formula.
        """
        choices_weights = []
        for child in self.children:
            weight = (child.q() / child.n()) + self._c * np.sqrt(
                2 * (np.log(self.n()) / child.n())
            )
            choices_weights.append(weight)

        best = self.children[np.argmax(choices_weights)]
        return best

        # def rollout_policy(self, possible_moves):
        """
        Function to select a move from the possible moves.
        In this case, a random move is selected.
        """
        # return possible_moves[np.random.randint(len(possible_moves))]

    def rollout_policy(self, possible_moves):
        """
        Chooses a move during rollout.
        With probability epsilon a random move is selected for exploration.
        Otherwise, the move with the highest heuristic evaluation is chosen.
        epsilon = 1.0 means random policy.
        """
        if np.random.rand() < self._epsilon:
            return random.choice(possible_moves)

        best_move = None
        best_score = -np.inf
        for move in possible_moves:
            score = self.heuristic_evaluation(move)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

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

            # Debug: Print all children of the root
        print("Final children stats:")
        for child in self.children:
            print(
                f"Action: {child.parent_action}, Visits: {child.n()}, Reward: {child.q()}"
            )
        print(f"-> Selected: {self.best_child().parent_action}")
        return self.best_child()

    def heuristic_evaluation(self, move):
        """
        Heuristic evaluation function for the Kulibrat rollout policy.
        """
        score = 0.0
        move_type, start, end = move

        # Bonus for move type (attack, jump, scoring)
        if move_type == "attack":
            score += 2.0
        elif move_type == "jump":
            score += 3.0
        elif move_type == "diagonal" and end == (-1, -1):
            score += 5.0  # Scoring move

        # If move results in a valid on-board destination, add positioning bonuses.
        if end != (-1, -1):
            dest_row, dest_col = end

            # 1. Center bonus: central column is 1 (0-indexed)
            if dest_col == 1:
                score += 1.0

            # 2. Advancement bonus: for Black, higher row is better; for Red, lower row is better.
            if self.player == "B":
                # Board rows range from 0 to 3; target is row 3.
                advancement = dest_row / 3.0
            else:
                advancement = (3 - dest_row) / 3.0
            score += advancement * 2.0  # weight factor for advancement

        return score


def monte_carlo_search(state, sim_no=100, c_param=1, epsilon=0.1):
    root = MonteCarlo(state, sim_no=sim_no, c_param=c_param, epsilon=epsilon)
    selected_node = root.best_action()
    return selected_node.parent_action
