from GameState import GameState
import tkinter as tk


class Board:
    def __init__(self, game):

        self.window = tk.Tk()
        self.window.geometry("1000x1000")
        self.window.title("Kulibrat Game")

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.canvas = tk.Canvas(self.window, width=1000, height=1000, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.cols, self.rows = 3, 4
        self.cell_width = 500 / self.cols
        self.cell_height = 500 / self.rows
        self.board_x = (700 - 500) // 2
        self.board_y = (700 - 500) // 2

        # Input control variable
        self.user_input_var = tk.StringVar()
        self.submit_pressed = tk.BooleanVar(value=False)  # Define before on_close!!!

        self.UI_board(game)

    def UI_board(self, game):
        """
        Draw the board and the pieces on the canvas
        """

        self.canvas.delete("all")

        for i in range(self.rows):
            for j in range(self.cols):
                x1 = self.board_x + j * self.cell_width
                y1 = self.board_y + i * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="white", outline="black"
                )

                if game.board[i][j] == "B":  # Black piece
                    self.canvas.create_oval(
                        x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="black"
                    )
                elif game.board[i][j] == "R":  # Red piece
                    self.canvas.create_oval(
                        x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="red"
                    )

        text_x = 700 // 2
        text_y = self.board_y + 530

        # Row numbers
        self.canvas.create_text(
            50,
            self.board_y + 20,
            text="0",
            font=("Arial", 16),
            fill="black",
            anchor="center",
        )
        self.canvas.create_text(
            50,
            self.board_y + self.cell_width - 20,
            text="1",
            font=("Arial", 16),
            fill="black",
            anchor="center",
        )
        self.canvas.create_text(
            50,
            self.board_y + (self.cell_width * 2) - 30,
            text="2",
            font=("Arial", 16),
            fill="black",
            anchor="center",
        )
        self.canvas.create_text(
            50,
            self.board_y + (self.cell_width * 3) - 40,
            text="3",
            font=("Arial", 16),
            fill="black",
            anchor="center",
        )

        # Column numbers
        self.canvas.create_text(
            self.board_x + 20,
            50,
            text="0",
            font=("Arial", 16),
            fill="black",
            anchor="center",
        )
        self.canvas.create_text(
            self.board_x + self.cell_width + 20,
            50,
            text="1",
            font=("Arial", 16),
            fill="black",
            anchor="center",
        )
        self.canvas.create_text(
            self.board_x + +(self.cell_width * 2) + 20,
            50,
            text="2",
            font=("Arial", 16),
            fill="black",
            anchor="center",
        )

        self.canvas.create_text(
            text_x,
            text_y,
            text=f"Score: Black {game.score['B']} | Red {game.score['R']} ",
            font=("Arial", 16),
            fill="black",
            anchor="center",
        )
        self.canvas.create_text(
            text_x,
            text_y + 30,
            text=f"Player:{game.player}",
            font=("Arial", 16),
            fill="black",
            anchor="center",
        )

        # Control variable for input
        self.user_input_var = tk.StringVar()
        self.submit_pressed = tk.BooleanVar(
            value=False
        )  # Controls how much the input changes

        # Input (Entry) and Submit button

        self.canvas.create_text(
            780,
            570,
            text="Select action: ",
            font=("Arial", 16),
            fill="black",
            anchor="center",
        )

        self.input_box = tk.Entry(
            self.window, font=("Arial", 14), textvariable=self.user_input_var
        )
        self.canvas.create_window(780, 600, window=self.input_box, width=200, height=30)

        self.submit_button = tk.Button(
            self.window, text="Submit", command=self.process_input
        )
        self.canvas.create_window(
            820, 650, window=self.submit_button, width=100, height=30
        )

        self.print_board(game)

    def print_board(self, game):
        """
        Print the board in the console
        """
        game.find_actions()
        print(f"\nPlayer: {game.player}")
        print("  0 1 2")  # Column nu2mbers
        print("  ------")
        for i, row in enumerate(game.board):
            row_str = f"{i}| " + " ".join(
                str(cell) if cell != 0 else "." for cell in row
            )
            print(row_str)
        print("  ------")
        print(f"Black: {game.score['B']} | {game.score['R']} :Red")

    def print_actions(self, game):
        """
        Print the available actions for the current player
        """
        if not game.actions[game.player]:
            self.canvas.create_text(
                780,
                200,
                text=f"\nMoving Player: {game.player}, No available actions",
                font=("Arial", 16),
                fill="black",
                anchor="center",
            )
            return

        self.canvas.create_text(
            780,
            200,
            text=f"\nMoving Player: {game.player}, Available actions:",
            font=("Arial", 16),
            fill="black",
            anchor="center",
        )
        for i, action in enumerate(game.actions[game.player]):
            move, start, end = action
            if start == (-1, -1):
                start = "Outside"
            if end == (-1, -1):
                end = "Outside"

            self.canvas.create_text(
                780,
                260 + (i * 30),
                text=f"{i}: {move} from {start} to {end}",
                font=("Arial", 16),
                fill="black",
                anchor="center",
            )
        return

    def get_input(self):
        """
        Get the user input from the Entry widget
        """
        print("Waiting fot the action...")
        self.submit_pressed.set(False)
        self.window.wait_variable(self.submit_pressed)
        return self.user_text

    def process_input(self):
        """
        Process the user input from the Entry widget
        """
        user_input = self.user_input_var.get().strip()

        if user_input.isdigit():
            self.user_text = int(user_input)
            print(f"Selected action: {self.user_text}")
            self.submit_pressed.set(True)
        else:
            print("Not valid entry. Please select a valid entry.")

    def on_close(self):
        """
        Close the game window
        """
        print("Closing the game window...")
        self.submit_pressed.set(True)  # Release the wait_variable
        self.window.destroy()  # Close the board windoe
