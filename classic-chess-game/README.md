# Classic Chess Game

This is a classic chess game implemented in Python. The project includes all the necessary components to play chess, including a graphical representation of the board, movement rules for each piece, and game logic to manage turns and win conditions.

## Project Structure

```
classic-chess-game
├── src
│   ├── main.py          # Entry point of the game
│   ├── chess
│   │   ├── board.py     # Class for the chessboard
│   │   ├── pieces.py    # Definitions for chess pieces
│   │   ├── game.py      # Game logic and management
│   │   └── utils.py     # Utility functions
├── tests
│   ├── test_board.py    # Unit tests for the Board class
│   ├── test_pieces.py   # Unit tests for piece classes
│   └── test_game.py     # Unit tests for the Game class
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Installation

To run the game, you need to have Python installed on your machine. You can install the required dependencies by running:

```
pip install -r requirements.txt
```

## Running the Game

To start the game, execute the following command in your terminal:

```
python src/main.py
```

## Features

- Play against another player.
- Valid movement rules for each chess piece.
- Check and checkmate detection.
- User-friendly interface for displaying the board.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. Your feedback and suggestions are welcome!