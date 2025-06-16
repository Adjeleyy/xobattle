let gameStarted = false;
let playerSymbol = null;
let gameGrid = Array(3).fill().map(() => Array(3).fill(''));

function selectPlayer(symbol) {
    if (gameStarted) return;
    
    playerSymbol = symbol;
    gameStarted = true;
    
    document.getElementById('player-selection').style.display = 'none';
    document.getElementById('game-container').style.display = 'block';
    
    // Initialize game
    fetch('/initialize_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ player_symbol: symbol })
    })
    .then(response => response.json())
    .then(data => {
        gameGrid = data.grid;
        updateGridDisplay();
        if (symbol === 'X') {
            showTurnMessage("X turn");
        }
    });
}

function makeMove(row, col) {
    if (!gameStarted || gameGrid[row][col] !== '') return;
    
    // Disable all cells during move
    disableAllCells();
    
    fetch('/make_move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            row: row,
            col: col,
            player_symbol: playerSymbol
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error(data.error);
            enableAllCells();
            return;
        }
        
        gameGrid = data.grid;
        updateGridDisplay();
        
        if (data.status === 'win') {
            updateScores(data.scores);
            showWinMessage(`${data.winner} wins!`);
        } else if (data.status === 'draw') {
            updateScores(data.scores);
            showWinMessage("Draw!");
        } else {
            const nextSymbol = playerSymbol === 'X' ? 'O' : 'X';
            showTurnMessage(nextSymbol + " turn");
            // Computer's turn
            setTimeout(() => {
                fetch('/make_move', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        row: -1,
                        col: -1,
                        player_symbol: nextSymbol
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error(data.error);
                        enableAllCells();
                        return;
                    }
                    
                    gameGrid = data.grid;
                    updateGridDisplay();
                    
                    if (data.status === 'win') {
                        updateScores(data.scores);
                        showWinMessage(`${data.winner} wins!`);
                    } else if (data.status === 'draw') {
                        updateScores(data.scores);
                        showWinMessage("Draw!");
                    } else {
                        showTurnMessage(playerSymbol + " turn");
                        enableAllCells();
                    }
                });
            }, 500);
        }
    });
}

function createGrid() {
    const grid = document.getElementById('game-grid');
    grid.innerHTML = '';
    
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.row = i;
            cell.dataset.col = j;
            cell.addEventListener('click', () => makeMove(i, j));
            grid.appendChild(cell);
        }
    }
}

function updateGridDisplay() {
    const cells = document.getElementsByClassName('cell');
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            const cell = cells[i * 3 + j];
            cell.textContent = gameGrid[i][j];
        }
    }
}

function updateScores(scores) {
    document.getElementById('x-score').textContent = scores.X;
    document.getElementById('o-score').textContent = scores.O;
}

function showTurnMessage(message) {
    const messageElement = document.getElementById('turn-message');
    messageElement.textContent = message;
    messageElement.style.display = 'block';
}

function showWinMessage(message) {
    const messageElement = document.getElementById('message');
    messageElement.textContent = message;
    messageElement.style.display = 'block';
}

function disableAllCells() {
    const cells = document.getElementsByClassName('cell');
    for (let cell of cells) {
        cell.style.pointerEvents = 'none';
    }
}

function enableAllCells() {
    const cells = document.getElementsByClassName('cell');
    for (let cell of cells) {
        if (cell.textContent === '') {
            cell.style.pointerEvents = 'auto';
        }
    }
}

function resetGame() {
    fetch('/reset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        gameGrid = data.grid;
        updateGridDisplay();
        enableAllCells();
        document.getElementById('message').style.display = 'none';
        
        if (playerSymbol === 'O') {
            showTurnMessage("X turn");
            setTimeout(() => {
                fetch('/make_move', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        row: -1,
                        col: -1,
                        player_symbol: 'X'
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error(data.error);
                        enableAllCells();
                        return;
                    }
                    gameGrid = data.grid;
                    updateGridDisplay();
                    showTurnMessage("O turn");
                    enableAllCells();
                });
            }, 500);
        } else {
            showTurnMessage("X turn");
        }
    });
}

// Initialize the game
createGrid(); 