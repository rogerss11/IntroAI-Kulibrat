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
        sim_no=15,
        epsilon=0.1,
        score_depth=100000,  # new parameter for cutoff
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
        self._score_depth = score_depth
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
            score_depth=self._score_depth,
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
        The game is simulated from the current state until a terminal condition is reached.
        A cutoff is applied if the score increases by more than score_depth relative to the starting score.
        Returns a final score: +1 if the current player wins, -1 otherwise.
        """
        current_rollout_state = self.state.clone_state()
        # Compute the cutoff based on the current maximum score on the board.
        initial_max_score = max(
            current_rollout_state.score["B"], current_rollout_state.score["R"]
        )
        cutoff = initial_max_score + self._score_depth

        # Run simulation until terminal state or cutoff is reached.
        while not current_rollout_state.terminal_test() and (
            max(current_rollout_state.score["B"], current_rollout_state.score["R"])
            < cutoff
        ):
            all_actions = current_rollout_state.find_actions()
            possible_moves = all_actions[current_rollout_state.player]
            if not possible_moves:
                break
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
        Returns True when all possible moves have been expanded.
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

    def rollout_policy(self, possible_moves):
        """
        Chooses a move during rollout.
        With probability epsilon a random move is selected for exploration.
        Otherwise, the move with the highest heuristic evaluation is chosen.
        epsilon = 0.0 means heuristic policy, epsilon = 1.0 means random policy.
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
        Select a node from which to run the rollout.
        """
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            current_node = current_node.best_child()
        return current_node

    def best_action(self):
        """
        Runs simulations up to _sim_no times and returns the best action.
        """
        simulation_no = self._sim_no

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        # Debug: Print children stats
        print("Final children stats:")
        for child in self.children:
            print(
                f"Action: {child.parent_action}, Visits: {child.n()}, Reward: {child.q()}"
            )
        print(f"-> Selected: {self.best_child().parent_action}")
        return self.best_child()

    def heuristic_evaluation(self, move):
        score = 0.0
        move_type, start, end = move

        # Bonus for move type (attack, jump, scoring)
        if move_type == "attack":
            score += 2.0
        elif move_type == "jump":
            score += 3.0
        elif end == (-1, -1):
            score += 5.0  # Scoring move

        # If move results in a valid on-board destination, add positioning bonuses
        # and apply a penalty for being immediately in front of an opponent.
        if end != (-1, -1) and end != (-1, 1):
            dest_row, dest_col = end
            board = (
                self.state.board
            )  # assuming board is a 2D list representing the current state

            # Penalize if the move puts your piece directly in front of an opponent piece.
            # For Black (who moves downward), check one row above (dest_row - 1)
            # For Red (who moves upward), check one row below (dest_row + 1)
            if self.player == "B":
                if dest_row - 1 >= 0 and board[dest_row - 1][dest_col] == self.opponent:
                    score -= 2.0  # penalize for being in front of an opponent piece
            else:  # self.player is "R"
                if (
                    dest_row + 1 < len(board)
                    and board[dest_row + 1][dest_col] == self.opponent
                ):
                    score -= 2.0  # penalize for being in front of an opponent piece

            # Center bonus: central column is 1 (0-indexed)
            if dest_col == 1:
                score += 1.0

            # Advancement bonus: for Black, a higher row is better;
            # for Red, a lower row is better.
            if self.player == "B":
                advancement = dest_row / (len(board) - 1)
            else:
                advancement = (len(board) - 1 - dest_row) / (len(board) - 1)
            score += advancement * 2.0

        return score


def monte_carlo_search(state, sim_no=15, c_param=1, epsilon=0.1, score_depth=100000):
    root = MonteCarlo(
        state, sim_no=sim_no, c_param=c_param, epsilon=epsilon, score_depth=score_depth
    )
    selected_node = root.best_action()
    return selected_node.parent_action
