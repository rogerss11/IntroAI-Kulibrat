import random

class GameState:
    def __init__(self, winning_score=5):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]	# 0 = empty, 'B' = black, 'R' = red)
        self.player = "B"
        self.winning_score = winning_score
        self.score = {"B": 0, "R": 0}
        self.remaining_pieces = {"B": 4, "R": 4}
        self.actions = []

    def print_board(self):
        print("\n  0 1 2")  # Column numbers
        print("  ------")
        for i, row in enumerate(self.board):
            row_str = f"{i}|" + " ".join(str(cell) if cell != 0 else "." for cell in row)
            print(row_str)
        print("  ------")


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
    
    def in_bounds(self, row, col):
        # Check if a position is within the bounds of the board
        return row >= 0 and row < 4 and col >= 0 and col < 3
    
    def find_actions(self):
        # Generate all possible actions for the current player
        black_pieces, red_pieces, empty_spaces = self.piece_coordinates()
        
        # Black player
        if self.player == "B":

            # Insert a piece
            if (self.remaining_pieces["B"] > 0):
                # Find empty spots
                for i in range(2):
                    if self.board[0][i] == 0:
                        self.actions.append(("insert", "B", (-1,-1), (0, i))) # Out of the board: (-1,-1)

            # Diagonal
            for piece in black_pieces:
                row, col = piece
                if self.in_bounds(row+1, col-1) and (row+1, col-1) in empty_spaces:
                        self.actions.append(("diagonal", "B", (row, col), (row+1, col-1)))
                elif self.in_bounds(row+1, col+1) and (row+1, col+1) in empty_spaces:
                        self.actions.append(("diagonal", "B", (row, col), (row+1, col+1)))
                elif row == 3:
                     self.actions.append(("diagonal", "B", (row, col), (-1, -1))) # Out of the board: (-1,-1)

            # Attack
            for piece in black_pieces:
                 row, col = piece
                 if (row+1, col) in red_pieces:
                      self.actions.append(("attack", "B", (row, col), (row+1, col)))
            
            # Jump
            for piece in black_pieces:
                row, col = piece
                if (row+1, col) in red_pieces:
                     if (row+2, col) in empty_spaces:
                          self.actions.append(("jump", "B", (row, col), (row+2, col)))
                     elif (row+2, col) in black_pieces:
                        continue
                     elif not self.in_bounds(row+2, col):
                          self.actions.append(("jump", "B", (row, col), (-1, -1))) # Out of the board: (-1,-1)
                     
                     elif (row+2, col) in red_pieces:
                        if (row+3, col) in empty_spaces:
                                self.actions.append(("jump", "B", (row, col), (row+3, col)))
                        elif (row+3, col) in black_pieces:
                            continue
                        elif not self.in_bounds(row+3, col) or (row+3,col) in red_pieces:
                                self.actions.append(("jump", "B", (row, col), (-1, -1)))        
                      
        
        # Red player
        if self.player == "R":
            # Insert a piece
            if (self.remaining_pieces["R"] > 0):
                # Find empty spots
                for i in range(2):
                    if self.board[3][i] == 0:
                        self.actions.append(("insert", "R", (-1,-1), (3, i))) # Out of the board: (-1,-1)

            # Diagonal
            for piece in red_pieces:
                row, col = piece
                if self.in_bounds(row-1, col-1) and (row-1, col-1) in empty_spaces:
                        self.actions.append(("diagonal", "R", (row, col), (row-1, col-1)))
                elif self.in_bounds(row-1, col+1) and (row+1, col+1) in empty_spaces:
                        self.actions.append(("diagonal", "R", (row, col), (row-1, col+1)))
                elif row == 0:
                     self.actions.append(("diagonal", "R", (row, col), (-1, -1))) # Out of the board: (-1,-1)
                
            # Attack
            for piece in red_pieces:
                row, col = piece
                if (row-1, col) in black_pieces:
                    self.actions.append(("attack", "R", (row, col), (row-1, col)))
            
            # Jump
            for piece in red_pieces:
                row, col = piece
                if (row-1, col) in black_pieces:
                     if (row-2, col) in empty_spaces:
                          self.actions.append(("jump", "R", (row, col), (row-2, col)))
                     elif (row-2, col) in red_pieces:
                        continue
                     elif not self.in_bounds(row-2, col):
                          self.actions.append(("jump", "R", (row, col), (-1, -1))) # Out of the board: (-1,-1)
                     
                     elif (row-2, col) in black_pieces:
                        if (row-3, col) in empty_spaces:
                                self.actions.append(("jump", "R", (row, col), (row-3, col)))
                        elif (row-3, col) in red_pieces:
                            continue
                        elif not self.in_bounds(row-3, col) or (row-3, col) in black_pieces:
                                self.actions.append(("jump", "R", (row, col), (-1, -1)))
           
    def result(self, action):
        pass

    def terminal_test(self):
        pass

    def generate_random_board(self):
        # Initialize an empty board
        board = [[0 for _ in range(3)] for _ in range(4)]

        # Randomly place black pieces (B) and red pieces (R)
        black_pieces = random.sample([(i, j) for i in range(4) for j in range(3)], 4)
        red_pieces = random.sample([(i, j) for i in range(4) for j in range(3) if (i, j) not in black_pieces], 4)

        # Place the pieces on the board
        for row, col in black_pieces:
            board[row][col] = "B"
        for row, col in red_pieces:
            board[row][col] = "R"

        return board

# Example usage
game = GameState()
game.board = game.generate_random_board()
game.print_board()
game.find_actions()
print(game.actions)

        
    
        

print("\nWelcome to Kulibrat!")
game = GameState()
game.print_board()
