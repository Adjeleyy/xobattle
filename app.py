from flask import Flask, render_template, request, jsonify, send_from_directory
import logging
import os
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path to the static directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__,
            static_url_path='/static',
            static_folder=STATIC_DIR,
            template_folder=TEMPLATE_DIR)


class TicTacToe:
    def __init__(self):
        self.reset_game()
        self.scores = {'X': 0, 'O': 0}
        self.player_symbol = None

    def reset_game(self):
        self.grid = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X always starts
        logger.info("Game reset")

    def set_player_symbol(self, symbol):
        self.player_symbol = symbol
        logger.info(f"Player symbol set to {symbol}")

    def get_computer_symbol(self):
        return 'O' if self.player_symbol == 'X' else 'X'

    def make_move(self, row, col, symbol):
        if row == -1 and col == -1:  # Computer move
            return self.make_computer_move()

        if self.grid[row][col] == '':
            self.grid[row][col] = symbol
            return True
        return False

    def make_computer_move(self):
        computer_symbol = self.get_computer_symbol()

        # Try to win
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == '':
                    self.grid[i][j] = computer_symbol
                    if self.check_winner() == computer_symbol:
                        return True
                    self.grid[i][j] = ''

        # Try to block player
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == '':
                    self.grid[i][j] = self.player_symbol
                    if self.check_winner() == self.player_symbol:
                        self.grid[i][j] = computer_symbol
                        return True
                    self.grid[i][j] = ''

        # Make random move
        empty_cells = [(i, j) for i in range(3)
                       for j in range(3) if self.grid[i][j] == '']
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = computer_symbol
            return True
        return False

    def check_winner(self):
        # Check rows
        for row in self.grid:
            if row[0] == row[1] == row[2] != '':
                return row[0]

        # Check columns
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] != '':
                return self.grid[0][col]

        # Check diagonals
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != '':
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != '':
            return self.grid[0][2]

        # Check for draw
        if all(cell != '' for row in self.grid for cell in row):
            return 'draw'

        return None


game = TicTacToe()


@app.route('/')
def index():
    game.reset_game()
    game.scores = {'X': 0, 'O': 0}
    return render_template('index.html')


@app.route('/debug/static/<path:filename>')
def debug_static(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/initialize_game', methods=['POST'])
def initialize_game():
    data = request.get_json()
    player_symbol = data.get('player_symbol')
    game.set_player_symbol(player_symbol)

    # If player chose O, make computer's first move
    if player_symbol == 'O':
        game.make_computer_move()

    return jsonify({
        'grid': game.grid
    })


@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')
    symbol = data.get('player_symbol')

    if game.make_move(row, col, symbol):
        winner = game.check_winner()
        if winner:
            if winner == 'draw':
                return jsonify({
                    'status': 'draw',
                    'grid': game.grid,
                    'scores': game.scores
                })
            else:
                game.scores[winner] += 1
                return jsonify({
                    'status': 'win',
                    'winner': winner,
                    'grid': game.grid,
                    'scores': game.scores
                })

        return jsonify({
            'status': 'continue',
            'grid': game.grid
        })

    return jsonify({'error': 'Invalid move'}), 400


@app.route('/reset', methods=['POST'])
def reset():
    game.reset_game()
    return jsonify({
        'grid': game.grid,
        'scores': game.scores
    })


if __name__ == '__main__':
    logger.debug('Starting Flask application')
    app.run(debug=True)
