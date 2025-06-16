import tkinter
import game_logic

game = game_logic.GameLogic()

game.player_turn()
game.update_score_board()

# TODO Create a 3x3 grid with 9 buttons.
game_grid = []
for row in range(3):
    button_row = []
    for column in range(3):
        cell = tkinter.Button(game, text="", width=10,
                              height=4, font=("Arial", 32, "bold"), fg="black")
        cell.grid(row=row+2, column=column)
        button_row.append(cell)
    game_grid.append(button_row)

game.grid = game_grid

# Set up click handlers
for row in range(3):
    for column in range(3):
        game_grid[row][column].config(
            command=lambda r=row, c=column: game.handle_click(r, c))
        

restart_button = tkinter.Button(game, text="Restart Game", command=game.reset_game)
restart_button.grid(row=5, column=0, columnspan=3, pady=20)

game.mainloop()  # This keeps the window open until it is closed by the user.


# Create a restart game button
