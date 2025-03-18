import time
from GameState import GameState

# Tests
game = GameState()
game.board = [[0, "B", 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
game.print_board()
game.print_actions()
print(game.actions)
print(game.terminal_test())


"""
# Test 1
game = GameState()
game.board = game.generate_random_board(seed=2)
game.print_board()
game.find_actions()
print(game.actions)
print(game.terminal_test())

# Test 2
game = GameState()
game.board = [["R", "B", "R"], ["R", 0, "R"], [0, 0, 0], [0, 0, 0]]
game.print_board()
game.find_actions()
game.print_actions()
print(game.terminal_test())
game.move(("jump", (0, 0), (2, 0)))
game.move(("pass", (-1, -1), (-1, -1)))
game.move(("diagonal", (0, 0), (-1, -1)))
game.print_board()
game.find_actions()

# Test 3
game = GameState()
game.board = [["B", 0, "B"], [0, "B", 0], ["R", "B", "R"], ["R", 0, "R"]]
game.player = "R"
game.print_board()
game.find_actions()
print(game.actions)
print(game.terminal_test())
print(f"Moving player: {game.player}, Winner: {game.winner}")

"""
