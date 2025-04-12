from .pieces import Peon, Torre, Caballo, Alfil, Reina, Rey

class Board:
    def __init__(self):
        # Represent the board as an 8x8 matrix of single pieces
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()

    def initialize_board(self):
        # Place white pieces
        self.board[0] = [
            Torre("white"), Caballo("white"), Alfil("white"), Reina("white"),
            Rey("white"), Alfil("white"), Caballo("white"), Torre("white")
        ]
        self.board[1] = [Peon("white") for _ in range(8)]

        # Place black pieces
        self.board[7] = [
            Torre("black"), Caballo("black"), Alfil("black"), Reina("black"),
            Rey("black"), Alfil("black"), Caballo("black"), Torre("black")
        ]
        self.board[6] = [Peon("black") for _ in range(8)]

    def place_piece(self, piece, position):
        x, y = position
        self.board[x][y] = piece

    def remove_piece(self, piece, position):
        x, y = position
        if self.board[x][y] == piece:
            self.board[x][y] = None

    def display(self):
        for row in self.board:
            print(" | ".join([str(piece) if piece else " " for piece in row]))
        print()

    def make_move(self, start_pos, end_pos):
        # Logic to move a piece from start_pos to end_pos
        piece = self.board[start_pos[0]][start_pos[1]]
        if piece and self.is_valid_move(piece, start_pos, end_pos):
            self.board[end_pos[0]][end_pos[1]] = piece
            self.board[start_pos[0]][start_pos[1]] = None
            return True
        return False

    def is_valid_move(self, piece, start_pos, end_pos):
        # Check if the move is valid for the piece
        return end_pos in piece.valid_moves(start_pos, self.board)