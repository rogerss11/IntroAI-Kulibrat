
class GameState:
    def __init__(self, winning_score=5):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]	# 0 = empty, 'B' = black, 'R' = red)
        self.player = "B"
        self.winning_score = winning_score
        self.score = {"B": 0, "R": 0}
        self.remaining_pieces = {"B": 4, "R": 4}
        self.actions = []

    def print_board(self):
        print("\n", self.board[0], "\n", self.board[1], "\n", self.board[2], "\n", self.board[3])

    def piece_coordinates(self):
        # Find coordinates of all pieces
        black_pieces = []
        red_pieces = []
        empty_spaces = []

        for i in range(4):
            for j in range(3):
                if self.board[i][j] == "B":
                    black_pieces.append((i, j))
                elif self.board[i][j] == "R":
                    red_pieces.append((i, j))
                else:
                    empty_spaces.append((i, j))
        return black_pieces, red_pieces, empty_spaces
    
    def in_bounds(row, col):
        return row >= 0 and row < 4 and col >= 0 and col < 3
    
    def actions(self):
        black_pieces, red_pieces, empty_spaces = self.piece_coordinates()
        
        # Black player
        if self.player == "B":
            # Insert a piece
            if (self.remaining_pieces["B"] > 0):
                # Find empty spots
                for i in range(3):
                    if self.board[0][i] == 0:
                        self.actions.append(("insert", "B", (0, i)))

            # Diagonal
            for piece in black_pieces:
                row, col = piece
                if self.in_bounds(row+1, col-1):
                    if self.board[row+1][col+1] == 0:
                        self.actions.append(("move", "B", (row+1, col+1)))



            # Jump

        
        # Red player
        if self.player == "R":
            # Insert a piece
            if (self.remaining_pieces["R"] > 0) and (0 in self.board[3]):
                    self.actions.append(("insert", 3))
            # Diagonal
    
    def result(self, action):
        pass

    def terminal_test(self):
        pass
        
    
        

print("Welcome to Kulibrat!")
game = GameState()
game.print_board()
game.print_board()
game.print_board()