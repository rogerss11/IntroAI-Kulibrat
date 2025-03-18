import random
import tkinter as tk


class GameState:
    def __init__(self, winning_score=5):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]  # 0 = empty, 'B' = black, 'R' = red)
        self.remaining_pieces = {"B": 4, "R": 4}
        self.player = "B"
        self.winning_score = winning_score
        self.score = {"B": 0, "R": 0}
        self.winner = None
        self.game_over = False
        self.utility = 0

        self.actions = self.find_actions()

    def print_board(self):
        window = tk.Tk()
        window.geometry('700x700')
        window.title("Kulibrat Game")

        canvas = tk.Canvas(window, width=700, height= 700,bg="white")
        canvas.pack(fill="both", expand=True)

        cols, rows = 3, 4
        cell_width = 500 / cols
        cell_height = 500 / rows
        board_x = (700 - 500) // 2  
        board_y = (700 - 650) // 2 

        for i in range(rows):
            for j in range(cols):
                x1 = board_x+ j * cell_width
                y1 = board_y + i * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height

                canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

        window.mainloop()




        # Print the current board
        self.find_actions()
        print(f"\nPlayer: {self.player}")
        print("  0 1 2")  # Column numbers
        print("  ------")
        for i, row in enumerate(self.board):
            row_str = f"{i}| " + " ".join(
                str(cell) if cell != 0 else "." for cell in row
            )
            print(row_str)
        print("  ------")
        print(f"Black: {self.score['B']} | {self.score['R']} :Red")

    def print_actions(self):
        # Print the current actions
        if not self.actions[self.player]:
            print(f"\nMoving Player: {self.player}, No available actions")
            return

        print(f"\nMoving Player: {self.player}, Available actions:")
        for i, action in enumerate(self.actions[self.player]):
            move, start, end = action
            if start == (-1, -1):
                start = "Outside"
            if end == (-1, -1):
                end = "Outside"
            print(f"    {i}: {move} from {start} to {end}")
        return

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

    def find_actions(self):  # ACTIONS(s) ------------------------------------------
        self.actions = {"B": [], "R": []}
        # Generate all possible actions for the current player
        black_pieces, red_pieces, empty_spaces = self.piece_coordinates()

        ### Black player ###

        # Insert a piece
        if len(black_pieces) < 4:
            for i in range(3):
                if self.board[0][i] == 0:
                    self.actions["B"].append(
                        ("insert", (-1, -1), (0, i))
                    )  # Out of the board: (-1,-1)

        for piece in black_pieces:
            row, col = piece

            # Diagonal
            if (row + 1, col - 1) in empty_spaces:
                self.actions["B"].append(("diagonal", (row, col), (row + 1, col - 1)))
            if (row + 1, col + 1) in empty_spaces:
                self.actions["B"].append(("diagonal", (row, col), (row + 1, col + 1)))
            if row == 3:
                self.actions["B"].append(
                    ("diagonal", (row, col), (-1, -1))
                )  # Out of the board: (-1,-1)

            # Attack
            if (row + 1, col) in red_pieces:
                self.actions["B"].append(("attack", (row, col), (row + 1, col)))

            # Jump
            if (row + 1, col) in red_pieces:
                if (row + 2, col) in empty_spaces:
                    self.actions["B"].append(("jump", (row, col), (row + 2, col)))
                elif (row + 2, col) in black_pieces:
                    pass
                elif not self.in_bounds(row + 2, col):
                    self.actions["B"].append(
                        ("jump", (row, col), (-1, -1))
                    )  # Out of the board: (-1,-1)

                elif (row + 2, col) in red_pieces:
                    if (row + 3, col) in empty_spaces:
                        self.actions["B"].append(("jump", (row, col), (row + 3, col)))
                    elif (row + 3, col) in black_pieces:
                        pass
                    elif (
                        not self.in_bounds(row + 3, col) or (row + 3, col) in red_pieces
                    ):
                        self.actions["B"].append(("jump", (row, col), (-1, -1)))

        ### Red player ###

        # Insert a piece
        if len(red_pieces) < 4:
            for i in range(3):
                if self.board[3][i] == 0:
                    self.actions["R"].append(
                        ("insert", (-1, -1), (3, i))
                    )  # Out of the board: (-1,-1)

        for piece in red_pieces:
            row, col = piece

            # Diagonal
            if (row - 1, col - 1) in empty_spaces:
                self.actions["R"].append(("diagonal", (row, col), (row - 1, col - 1)))
            if (row - 1, col + 1) in empty_spaces:
                self.actions["R"].append(("diagonal", (row, col), (row - 1, col + 1)))
            if row == 0:
                self.actions["R"].append(
                    ("diagonal", (row, col), (-1, -1))
                )  # Out of the board: (-1,-1)

            # Attack
            if (row - 1, col) in black_pieces:
                self.actions["R"].append(("attack", (row, col), (row - 1, col)))

            # Jump
            if (row - 1, col) in black_pieces:
                if (row - 2, col) in empty_spaces:
                    self.actions["R"].append(("jump", (row, col), (row - 2, col)))
                elif (row - 2, col) in red_pieces:
                    pass
                elif not self.in_bounds(row - 2, col):
                    self.actions["R"].append(
                        ("jump", (row, col), (-1, -1))
                    )  # Out of the board: (-1,-1)

                elif (row - 2, col) in black_pieces:
                    if (row - 3, col) in empty_spaces:
                        self.actions["R"].append(("jump", (row, col), (row - 3, col)))
                    elif (row - 3, col) in red_pieces:
                        pass
                    elif (
                        not self.in_bounds(row - 3, col)
                        or (row - 3, col) in black_pieces
                    ):
                        self.actions["R"].append(("jump", (row, col), (-1, -1)))

        # Pass
        if self.actions["B"] == [] and self.actions["R"] != []:
            self.actions["B"].append(("pass", (-1, -1), (-1, -1)))
        elif self.actions["R"] == [] and self.actions["B"] != []:
            self.actions["R"].append(("pass", (-1, -1), (-1, -1)))

    def move(self, action):  # RESULT(s,a) -----------------------------------------
        # Apply an action to the current state

        if self.game_over:
            print("Game is over")
            return

        if action not in self.actions[self.player]:
            print(f"\n !!! Invalid action: {action}, Moving player: {self.player} !!!")
            print(f"Available actions: {self.actions[self.player]}")
            return

        move, start, end = action

        match move:
            case "insert":
                self.board[end[0]][end[1]] = self.player
                self.remaining_pieces[self.player] -= 1
                self.player = "R" if self.player == "B" else "B"

            case "diagonal":
                self.board[start[0]][start[1]] = 0
                if end != (-1, -1):
                    self.board[end[0]][end[1]] = self.player
                else:
                    self.remaining_pieces[self.player] += 1
                    self.score[self.player] += 1
                self.player = "R" if self.player == "B" else "B"

            case "attack":
                self.board[start[0]][start[1]] = 0
                self.board[end[0]][end[1]] = self.player
                self.remaining_pieces["R" if self.player == "B" else "B"] -= 1
                self.player = "R" if self.player == "B" else "B"

            case "jump":
                self.board[start[0]][start[1]] = 0
                if end != (-1, -1):
                    self.board[end[0]][end[1]] = self.player
                else:
                    self.remaining_pieces[self.player] += 1
                    self.score[self.player] += 1
                self.player = "R" if self.player == "B" else "B"

            case "pass":
                self.player = "R" if self.player == "B" else "B"

    def terminal_test(self):  # TERMINAL-TEST(s) -----------------------------------
        self.find_actions()
        if (self.score["B"] >= self.winning_score) or (
            self.player == "B" and not self.actions["R"] and not self.actions["B"]
        ):
            self.winner = "B"
            self.utility = 1
            return True
        if (self.score["R"] >= self.winning_score) or (
            self.player == "R" and not self.actions["B"] and not self.actions["R"]
        ):
            self.winner = "R"
            self.utility = -1
            return True
        return False

    def generate_random_board(self, seed=None):
        # Initialize an empty board, used for testing
        if seed is not None:
            random.seed(seed)

        board = [[0 for _ in range(3)] for _ in range(4)]

        black_pieces = random.sample([(i, j) for i in range(4) for j in range(3)], 4)
        red_pieces = random.sample(
            [(i, j) for i in range(4) for j in range(3) if (i, j) not in black_pieces],
            4,
        )
        for row, col in black_pieces:
            board[row][col] = "B"
        for row, col in red_pieces:
            board[row][col] = "R"

        return board
