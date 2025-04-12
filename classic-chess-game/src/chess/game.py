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

    def is_in_check(self, color):
        # Check if the king of the given color is under attack
        rey_position = None
        for x in range(8):
            for y in range(8):
                piece = self.board.board[x][y]
                if piece and isinstance(piece, Rey) and piece.color == color:
                    rey_position = (x, y)
                    break

        if not rey_position:
            return False

        # Check if any opponent piece can attack the king
        opponent_color = "black" if color == "white" else "white"
        for x in range(8):
            for y in range(8):
                piece = self.board.board[x][y]
                if piece and piece.color == opponent_color:
                    if rey_position in piece.valid_moves((x, y), self.board.board):
                        return True
        return False

    def is_checkmate(self):
        # Check if the current player is in checkmate
        if not self.is_in_check(self.current_turn):
            return False

        # Check if the current player has any valid moves to escape check
        for x in range(8):
            for y in range(8):
                piece = self.board.board[x][y]
                if piece and piece.color == self.current_turn:
                    for move in piece.valid_moves((x, y), self.board.board):
                        # Simulate the move
                        original_piece = self.board.board[move[0]][move[1]]
                        self.board.board[move[0]][move[1]] = piece
                        self.board.board[x][y] = None

                        if not self.is_in_check(self.current_turn):
                            # Undo the move
                            self.board.board[x][y] = piece
                            self.board.board[move[0]][move[1]] = original_piece
                            return False

                        # Undo the move
                        self.board.board[x][y] = piece
                        self.board.board[move[0]][move[1]] = original_piece

        return True

    def is_stalemate(self):
        # Check if the current player has no valid moves but is not in check
        if self.is_in_check(self.current_turn):
            return False

        for x in range(8):
            for y in range(8):
                piece = self.board.board[x][y]
                if piece and piece.color == self.current_turn:
                    for move in piece.valid_moves((x, y), self.board.board):
                        # Simulate the move
                        original_piece = self.board.board[move[0]][move[1]]
                        self.board.board[move[0]][move[1]] = piece
                        self.board.board[x][y] = None

                        if not self.is_in_check(self.current_turn):
                            # Undo the move
                            self.board.board[x][y] = piece
                            self.board.board[move[0]][move[1]] = original_piece
                            return False

                        # Undo the move
                        self.board.board[x][y] = piece
                        self.board.board[move[0]][move[1]] = original_piece

        return True

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

    def capture_logic(self, attacker, defender_pieces):
        # Calculate the total score of the defender's pieces
        defender_score = sum(piece.get_score() for piece in defender_pieces)
        attacker_score = attacker.get_score()

        if attacker_score > defender_score:
            # Attacker wins, defender pieces are captured
            return "attacker_wins"
        else:
            # Defender wins, attacker is captured
            return "defender_wins"

    def move_piece(self, start, end):
        attacker = self.board.get_pieces(start).pop(0)  # Get the attacking piece
        defender_pieces = self.board.get_pieces(end)

        if defender_pieces:
            result = self.capture_logic(attacker, defender_pieces)
            if result == "attacker_wins":
                self.board.place_piece(attacker, end)  # Replace defender with attacker
                for defender in defender_pieces:
                    self.board.remove_piece(defender, end)  # Remove all defenders
            elif result == "defender_wins":
                self.board.place_piece(attacker, start)  # Return attacker to start
        else:
            self.board.place_piece(attacker, end)  # Move attacker to empty square

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