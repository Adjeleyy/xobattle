import tkinter
import random


class GameLogic(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("XO-Battle")
        self.geometry("700x700")
        self.config(padx=10, pady=10)
        self.current_player = ""
        self.grid = []
        self.x_score = 0
        self.o_score = 0
        self.player_symbol = "X"  # Default player symbol
        self.computer_symbol = "O"  # Computer plays as opposite of player
        self.player_turn()
        # self.game_over = False

    def player_turn(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"
        turn_text = tkinter.Label(
            self, text=f"Player {self.current_player}'s turn")
        turn_text.grid(row=1, column=0, columnspan=3,
                       sticky="ew", pady=(10, 20))

    def start_game(self):
        for row in range(3):
            for column in range(3):
                current_row = row
                current_column = column
                self.grid[row][column].config(
                    command=lambda r=current_row, c=current_column: self.handle_click(r, c))

    def handle_click(self, row, column):
        # Only allow player moves on empty cells
        if self.grid[row][column]["text"] == "":
            # Player's move
            self.grid[row][column]["text"] = self.current_player
            winner = self.check_winner()
            if winner:
                self.update_score()
                self.show_win_message(winner)
            elif self.is_grid_full():
                self.show_win_message("Draw")
            else:
                self.player_turn()
                # Computer's move
                self.after(500, self.computer_move)

    def computer_move(self):
        if not self.is_grid_full():
            # First, check if computer can win
            winning_move = self.find_winning_move(self.computer_symbol)
            if winning_move:
                row, col = winning_move
                self.make_move(row, col)
                return

            # Then, check if need to block player's winning move
            blocking_move = self.find_winning_move(self.player_symbol)
            if blocking_move:
                row, col = blocking_move
                self.make_move(row, col)
                return

            # Try to take center if available
            if self.grid[1][1]["text"] == "":
                self.make_move(1, 1)
                return

            # Try to take corners
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            random.shuffle(corners)
            for row, col in corners:
                if self.grid[row][col]["text"] == "":
                    self.make_move(row, col)
                    return

            # Take any available edge
            edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
            random.shuffle(edges)
            for row, col in edges:
                if self.grid[row][col]["text"] == "":
                    self.make_move(row, col)
                    return

    def find_winning_move(self, symbol):
        # Check all empty cells
        for i in range(3):
            for j in range(3):
                if self.grid[i][j]["text"] == "":
                    # Try the move
                    self.grid[i][j]["text"] = symbol
                    # Check if it's a winning move
                    if self.check_winner() == symbol:
                        # Undo the move
                        self.grid[i][j]["text"] = ""
                        return (i, j)
                    # Undo the move
                    self.grid[i][j]["text"] = ""
        return None

    def make_move(self, row, col):
        self.grid[row][col]["text"] = self.current_player
        winner = self.check_winner()
        if winner:
            self.update_score()
            self.show_win_message(winner)
        elif self.is_grid_full():
            self.show_win_message("Draw")
        else:
            self.player_turn()

    def check_winner(self):
        # Check horizontal rows
        for row in range(3):
            if self.grid[row][0]["text"] == self.grid[row][1]["text"] == self.grid[row][2]["text"] != "":
                return self.grid[row][0]["text"]

        # Check vertical columns
        for col in range(3):
            if self.grid[0][col]["text"] == self.grid[1][col]["text"] == self.grid[2][col]["text"] != "":
                return self.grid[0][col]["text"]

        # Check diagonals
        if self.grid[0][0]["text"] == self.grid[1][1]["text"] == self.grid[2][2]["text"] != "":
            return self.grid[0][0]["text"]
        if self.grid[0][2]["text"] == self.grid[1][1]["text"] == self.grid[2][0]["text"] != "":
            return self.grid[0][2]["text"]

        # Check for draw
        if self.is_grid_full():
            return "Draw"

        return None

    def show_win_message(self, winner):
        if hasattr(self, 'win_label'):
            self.win_label.destroy()

        if winner == "Draw":
            message = "Game Over! It's a Draw!"
        else:
            message = f"Game Over! Player {winner} wins!"

        self.win_label = tkinter.Label(
            self, text=message, font=("Arial", 16, "bold"))
        self.win_label.grid(row=4, column=0, columnspan=3, pady=20)
        # Remove the message after 2 seconds
        self.after(2000, self.remove_win_message)

    def remove_win_message(self):
        if hasattr(self, 'win_label'):
            self.win_label.destroy()

    def update_score(self):
        winner = self.check_winner()
        if winner == "X":
            self.x_score += 1
        elif winner == "O":
            self.o_score += 1
        self.update_score_board()

    def update_score_board(self):
        score_board = tkinter.Label(
            self, text=f"X: {self.x_score} | O: {self.o_score}", font=("Arial", 16))
        score_board.grid(row=0, column=0, columnspan=3,
                         sticky="ew", pady=(10, 20))

    def reset_game(self):
        # Clear all cells in the grid
        self.remove_win_message()
        for row in range(3):
            for column in range(3):
                self.grid[row][column]["text"] = ""
        # Reset current player
        self.current_player = ""
        self.player_turn()

    def is_grid_full(self):
        return all(self.grid[i][j]["text"] != "" for i in range(3) for j in range(3))
