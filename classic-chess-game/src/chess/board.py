from .pieces import Peon, Torre, Caballo, Alfil, Reina, Rey

class Board:
    def __init__(self):
        # Represent the board as an 8x8 matrix of lists (to hold multiple pieces)
        self.board = [[[] for _ in range(8)] for _ in range(8)]

    def place_piece(self, piece, position):
        x, y = position
        self.board[x][y].append(piece)

    def remove_piece(self, piece, position):
        x, y = position
        if piece in self.board[x][y]:
            self.board[x][y].remove(piece)

    def get_pieces(self, position):
        x, y = position
        return self.board[x][y]

    def display(self):
        for row in self.board:
            print(" | ".join([" ".join(str(piece) for piece in cell) if cell else " " for cell in row]))
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