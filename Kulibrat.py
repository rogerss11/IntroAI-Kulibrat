
class GameState:
    def __init__(self, winning_score=5):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]	# 0 = empty, 1 = player 1 (black), 2 = player 2 (red)
        self.player = 1
        self.winning_score = winning_score
        self.score = [0, 0]
        self.actions = ["Diagonal", "Insert", "Jump"]

    def print_board(self):
        print("\n", self.board[0], "\n", self.board[1], "\n", self.board[2], "\n", self.board[3])

    def insert(self, column):
        for i in range(3, -1, -1):
            if self.board[i][column] == 0:
                self.board[i][column] = self.player
                break
        self.player = 1 if self.player == 2 else 2


print("Welcome to Kulibrat!")
game = GameState()
game.print_board()
game.insert(1)
game.print_board()
game.insert(2)
game.print_board()