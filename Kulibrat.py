import tkinter as tk
from tkinter import messagebox
import copy
import math

# -----------------------------
# Game logic for Kulibrat
# -----------------------------
class KulibratGame:
    def __init__(self, score_to_win=5):
        # Board dimensions: 4 rows, 3 columns.
        self.rows = 4
        self.cols = 3
        self.board = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        # Reserves: number of pieces not yet on board.
        self.reserve = {'B': 4, 'R': 4}
        self.score = {'B': 0, 'R': 0}
        self.score_to_win = score_to_win
        # Black always starts.
        self.current = 'B'

    def clone(self):
        new_game = KulibratGame(self.score_to_win)
        new_game.board = copy.deepcopy(self.board)
        new_game.reserve = self.reserve.copy()
        new_game.score = self.score.copy()
        new_game.current = self.current
        return new_game

    def opponent(self, player):
        return 'R' if player == 'B' else 'B'

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def legal_moves(self, player):
        moves = []
        direction = 1 if player == 'B' else -1  # Black moves downward, Red upward.
        start_row = 0 if player == 'B' else self.rows - 1

        # Insert moves.
        if self.reserve[player] > 0:
            for c in range(self.cols):
                if self.board[start_row][c] == '.':
                    moves.append({
                        'type': 'insert',
                        'position': (start_row, c)
                    })

        # Moves from pieces already on board.
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == player:
                    # Diagonal move:
                    for dc in [-1, 1]:
                        new_r = r + direction
                        new_c = c + dc
                        # Special case: exiting board.
                        if not self.in_bounds(new_r, new_c):
                            opp_start = self.rows - 1 if player == 'B' else 0
                            if r == opp_start:
                                moves.append({
                                    'type': 'diagonal',
                                    'from': (r, c),
                                    'to': 'exit'
                                })
                        else:
                            if self.board[new_r][new_c] == '.':
                                moves.append({
                                    'type': 'diagonal',
                                    'from': (r, c),
                                    'to': (new_r, new_c)
                                })
                    # Attack move: straight forward.
                    new_r = r + direction
                    new_c = c
                    if self.in_bounds(new_r, new_c) and self.board[new_r][new_c] == self.opponent(player):
                        moves.append({
                            'type': 'attack',
                            'from': (r, c),
                            'to': (new_r, new_c)
                        })
                    # Jump move: over contiguous opponent pieces.
                    jump_r = r + direction
                    count = 0
                    while self.in_bounds(jump_r, c) and self.board[jump_r][c] == self.opponent(player):
                        count += 1
                        jump_r += direction
                    if count > 0:
                        if not self.in_bounds(jump_r, c):
                            moves.append({
                                'type': 'jump',
                                'from': (r, c),
                                'to': 'exit',
                                'over': count
                            })
                        elif self.board[jump_r][c] == '.':
                            moves.append({
                                'type': 'jump',
                                'from': (r, c),
                                'to': (jump_r, c),
                                'over': count
                            })
        return moves

    def apply_move(self, move, player):
        direction = 1 if player == 'B' else -1
        if move['type'] == 'insert':
            r, c = move['position']
            self.board[r][c] = player
            self.reserve[player] -= 1
        elif move['type'] == 'diagonal':
            if 'from' in move:
                r, c = move['from']
                self.board[r][c] = '.'
            if move['to'] == 'exit':
                self.score[player] += 1
                self.reserve[player] += 1
            else:
                new_r, new_c = move['to']
                self.board[new_r][new_c] = player
        elif move['type'] == 'attack':
            r, c = move['from']
            new_r, new_c = move['to']
            self.board[r][c] = '.'
            opp = self.opponent(player)
            self.board[new_r][new_c] = player
            self.reserve[opp] += 1
        elif move['type'] == 'jump':
            r, c = move['from']
            self.board[r][c] = '.'
            if move['to'] == 'exit':
                self.score[player] += 1
                self.reserve[player] += 1
            else:
                new_r, new_c = move['to']
                self.board[new_r][new_c] = player

    def has_moves(self, player):
        return len(self.legal_moves(player)) > 0

    def game_over(self):
        return (self.score['B'] >= self.score_to_win or 
                self.score['R'] >= self.score_to_win or
                (not self.has_moves('B') and not self.has_moves('R')))

    def evaluate(self, player):
        opp = self.opponent(player)
        score_diff = self.score[player] - self.score[opp]
        pieces = sum(row.count(player) for row in self.board)
        opp_pieces = sum(row.count(opp) for row in self.board)
        piece_diff = pieces - opp_pieces
        reserve_diff = self.reserve[player] - self.reserve[opp]
        return 10 * score_diff + 2 * piece_diff + reserve_diff

    def minimax(self, depth, maximizing_player, alpha=-math.inf, beta=math.inf, ai_player=None):
        if ai_player is None:
            ai_player = self.current
        if depth == 0 or self.game_over():
            return self.evaluate(ai_player), None
        
        moves = self.legal_moves(self.current)
        if not moves:
            child = self.clone()
            child.current = child.opponent(child.current)
            return child.minimax(depth-1, not maximizing_player, alpha, beta, ai_player)[0], None
        
        best_move = None
        if maximizing_player:
            max_eval = -math.inf
            for move in moves:
                child = self.clone()
                child.apply_move(move, child.current)
                child.current = child.opponent(child.current)
                eval_val, _ = child.minimax(depth-1, False, alpha, beta, ai_player)
                if eval_val > max_eval:
                    max_eval = eval_val
                    best_move = move
                alpha = max(alpha, eval_val)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in moves:
                child = self.clone()
                child.apply_move(move, child.current)
                child.current = child.opponent(child.current)
                eval_val, _ = child.minimax(depth-1, True, alpha, beta, ai_player)
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_move = move
                beta = min(beta, eval_val)
                if beta <= alpha:
                    break
            return min_eval, best_move

# -----------------------------
# Graphical Interface using tkinter with Mouse Interaction
# -----------------------------
class KulibratGUI:
    def __init__(self, master, ai_for=None, search_depth=3):
        self.master = master
        self.master.title("Kulibrat")
        self.ai_for = ai_for  # 'B' or 'R' for AI-controlled player, or None for human vs. human
        self.search_depth = search_depth

        # Create game instance.
        self.game = KulibratGame(score_to_win=5)
        # Selected cell for a move (tuple: (row, col) or None).
        self.selected_cell = None

        # Create GUI elements.
        self.board_frame = tk.Frame(master)
        self.board_frame.grid(row=0, column=0, padx=10, pady=10)

        self.info_frame = tk.Frame(master)
        self.info_frame.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        self.status_label = tk.Label(self.info_frame, text="Game Status", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.newgame_button = tk.Button(self.info_frame, text="New Game", command=self.new_game)
        self.newgame_button.pack(pady=5)

        # Create a grid of Canvas widgets for the board.
        self.cell_size = 60
        self.cells = [[None for _ in range(self.game.cols)] for _ in range(self.game.rows)]
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                canvas = tk.Canvas(self.board_frame, width=self.cell_size, height=self.cell_size, bg="white", highlightthickness=1, highlightbackground="black")
                canvas.grid(row=r, column=c, padx=2, pady=2)
                # Bind mouse click event and pass row, col
                canvas.bind("<Button-1>", lambda event, row=r, col=c: self.cell_clicked(row, col))
                self.cells[r][c] = canvas

        # Start the game loop.
        self.update_gui()
        self.master.after(500, self.game_loop)

    def update_gui(self):
        # Update board cells: clear and redraw pieces as colored circles.
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                canvas = self.cells[r][c]
                canvas.delete("all")
                # If this cell is selected, draw a yellow highlight rectangle.
                if self.selected_cell == (r, c):
                    canvas.create_rectangle(2, 2, self.cell_size-2, self.cell_size-2, outline="yellow", width=3)
                # Draw piece if present.
                piece = self.game.board[r][c]
                if piece != '.':
                    color = "black" if piece == 'B' else "red"
                    margin = 10
                    canvas.create_oval(margin, margin, self.cell_size - margin, self.cell_size - margin, fill=color)
        # Update status.
        status = f"Turn: {'Black' if self.game.current=='B' else 'Red'}\n"
        status += f"Score: Black {self.game.score['B']} - Red {self.game.score['R']}\n"
        status += f"Reserves: Black {self.game.reserve['B']} - Red {self.game.reserve['R']}"
        self.status_label.config(text=status)

    def cell_clicked(self, row, col):
        # Ignore clicks if game over.
        if self.game.game_over():
            return

        current = self.game.current
        start_row = 0 if current == 'B' else self.game.rows - 1
        legal = self.game.legal_moves(current)

        if not legal:
            self.switch_turn()

        # If nothing is selected yet.
        if self.selected_cell is None:
            # If clicked cell is empty and in starting row => insert move?
            if self.game.board[row][col] == '.' and row == start_row:
                # Check if an insert move for this cell exists.
                for move in legal:
                    if move['type'] == 'insert' and move['position'] == (row, col):
                        self.game.apply_move(move, current)
                        self.switch_turn()
                        self.update_gui()
                        return
            # Otherwise, if clicked cell has a piece of current player, select it.
            if self.game.board[row][col] == current:
                self.selected_cell = (row, col)
                self.update_gui()
            else:
                # Not a valid selection.
                return
        else:
            # A cell is already selected.
            sel_row, sel_col = self.selected_cell
            # If the same cell is clicked, check for an exit move (if available).
            if (row, col) == self.selected_cell:
                for move in legal:
                    if move.get('from') == self.selected_cell and move['to'] == 'exit':
                        self.game.apply_move(move, current)
                        self.selected_cell = None
                        self.switch_turn()
                        self.update_gui()
                        return
            # Otherwise, check if there is a legal move from the selected cell to the clicked cell.
            valid_move = None
            for move in legal:
                if move.get('from') == self.selected_cell and move.get('to') != 'exit':
                    if move['to'] == (row, col):
                        valid_move = move
                        break
            if valid_move:
                self.game.apply_move(valid_move, current)
                self.selected_cell = None
                self.switch_turn()
                self.update_gui()
            else:
                # If clicked on another piece of the current player, change selection.
                if self.game.board[row][col] == current:
                    self.selected_cell = (row, col)
                    self.update_gui()
                else:
                    # Otherwise, clear selection.
                    self.selected_cell = None
                    self.update_gui()

    def switch_turn(self):
        self.game.current = self.game.opponent(self.game.current)

    def ai_move(self):
        legal = self.game.legal_moves(self.game.current)
        if not legal:
            self.switch_turn()
            return
        _, chosen_move = self.game.minimax(self.search_depth, True, ai_player=self.game.current)
        if chosen_move:
            self.game.apply_move(chosen_move, self.game.current)
            self.switch_turn()

    def game_loop(self):
        if self.game.game_over():
            winner = "Black" if self.game.score['B'] >= self.game.score_to_win else "Red"
            messagebox.showinfo("Game Over", f"Game Over! {winner} wins!")
            return
        # If current turn is AI, perform AI move.
        if self.ai_for is not None and self.game.current == self.ai_for:
            self.ai_move()
            self.selected_cell = None
            self.update_gui()
        self.master.after(500, self.game_loop)

    def new_game(self):
        self.game = KulibratGame(score_to_win=5)
        self.selected_cell = None
        self.update_gui()

# -----------------------------
# Main function to start the game
# -----------------------------
def main():
    # Set AI control: set ai_for = 'R' to have the AI control Red; set to None for two-player.
    ai_for = 'R'
    root = tk.Tk()
    gui = KulibratGUI(root, ai_for=ai_for, search_depth=3)
    root.mainloop()

if __name__ == "__main__":
    main()
