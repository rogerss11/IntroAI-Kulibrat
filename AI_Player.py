import numpy as np
from collections import defaultdict
from GameState import GameState

class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None, parent_action=None):
        gc = game.clone.state()
        self.state = gc.board
        
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