from .board import Board
from .pieces import Rey

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.current_turn = "white"

    def parse_move(self, move):
        # Convert chess notation (e.g., e2e4) to board indices
        start = (8 - int(move[1]), ord(move[0]) - ord('a'))
        end = (8 - int(move[3]), ord(move[2]) - ord('a'))
        return start, end

    def is_checkmate(self):
        # Updated to remove dependency on `is_in_check`
        return False

    def is_stalemate(self):
        # Updated to remove dependency on `is_in_check`
        return False

    def is_king_alive(self, color):
        # Check if the king of the given color is still on the board
        for x in range(8):
            for y in range(8):
                piece = self.board.board[x][y]
                if piece and isinstance(piece, Rey) and piece.color == color:
                    return True
        return False

    def check_winner(self):
        # Refactored to ensure accurate detection of king's status
        white_king_alive = self.is_king_alive("white")
        black_king_alive = self.is_king_alive("black")

        if not white_king_alive:
            print("DEBUG: White king is dead.")
            return "Black Wins!"
        elif not black_king_alive:
            print("DEBUG: Black king is dead.")
            return "White Wins!"
        return None

    def move_piece(self, start, end):
        piece = self.board.board[start[0]][start[1]]
        target = self.board.board[end[0]][end[1]]

        if piece and (not target or target.color != piece.color):
            self.board.board[end[0]][end[1]] = piece
            self.board.board[start[0]][start[1]] = None

    def play_turn(self):
        self.board.display()
        print(f"Turno de {self.current_turn.capitalize()}")
        move = input("Introduce tu movimiento (e.g., e2e4): ")
        try:
            start, end = self.parse_move(move)
            piece = self.board.board[start[0]][start[1]]
            if piece and piece.color == self.current_turn:
                # Perform the move
                self.move_piece(start, end)
                self.current_turn = "black" if self.current_turn == "white" else "white"
            else:
                print("Selección inválida de pieza. Intenta de nuevo.")
        except Exception as e:
            print(f"Error: {e}. Intenta de nuevo.")

        # Check if either king is dead
        winner = self.check_winner()
        if winner:
            print(winner)
            self.running = False

    def start_game(self):
        print("Welcome to Classic Chess!")
        while not self.is_checkmate() and not self.is_stalemate():
            self.play_turn()
        if self.is_checkmate():
            print(f"Checkmate! {self.current_turn.capitalize()} loses.")
        else:
            print("Stalemate! It's a draw.")