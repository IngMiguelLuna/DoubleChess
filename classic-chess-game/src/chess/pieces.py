class Piece:
    def __init__(self, color):
        self.color = color

    def __str__(self):
        # Map piece names to asset keys
        piece_map = {
            'Peon': 'p',
            'Torre': 'r',
            'Caballo': 'n',
            'Alfil': 'b',
            'Reina': 'q',
            'Rey': 'k'
        }
        prefix = piece_map[self.__class__.__name__]
        return prefix.upper() if self.color == "white" else prefix.lower()

    def get_score(self):
        # Default score for a generic piece
        return 0

class Peon(Piece):
    def valid_moves(self, position, board):
        moves = []
        x, y = position
        # Corrected direction for white and black pawns
        direction = 1 if self.color == "white" else -1

        # Forward move
        if 0 <= x + direction < 8 and board[x + direction][y] is None:
            moves.append((x + direction, y))
            # Double forward move on first move
            if (self.color == "white" and x == 1) or (self.color == "black" and x == 6):
                if board[x + 2 * direction][y] is None:
                    moves.append((x + 2 * direction, y))

        # Capture moves
        for dy in [-1, 1]:
            if 0 <= y + dy < 8 and 0 <= x + direction < 8:
                target = board[x + direction][y + dy]
                if target and target.color != self.color:
                    moves.append((x + direction, y + dy))

        return moves

    def get_score(self):
        return 1

class Torre(Piece):
    def valid_moves(self, position, board):
        moves = []
        x, y = position
        # Horizontal and vertical moves
        # Check upward
        for i in range(x - 1, -1, -1):
            if board[i][y] is None:
                moves.append((i, y))
            elif board[i][y].color != self.color:
                moves.append((i, y))
                break
            else:
                break
        # Check downward
        for i in range(x + 1, 8):
            if board[i][y] is None:
                moves.append((i, y))
            elif board[i][y].color != self.color:
                moves.append((i, y))
                break
            else:
                break
        # Check left
        for j in range(y - 1, -1, -1):
            if board[x][j] is None:
                moves.append((x, j))
            elif board[x][j].color != self.color:
                moves.append((x, j))
                break
            else:
                break
        # Check right
        for j in range(y + 1, 8):
            if board[x][j] is None:
                moves.append((x, j))
            elif board[x][j].color != self.color:
                moves.append((x, j))
                break
            else:
                break
        return moves

    def get_score(self):
        return 5

class Caballo(Piece):
    def valid_moves(self, position, board):
        moves = []
        x, y = position
        # L-shaped moves
        knight_moves = [
            (x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
            (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)
        ]
        for move in knight_moves:
            if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                moves.append(move)
        return moves

    def get_score(self):
        return 3

class Alfil(Piece):
    def valid_moves(self, position, board):
        moves = []
        x, y = position
        # Diagonal moves
        # Check top-right
        for i, j in zip(range(x - 1, -1, -1), range(y + 1, 8)):
            if board[i][j] is None:
                moves.append((i, j))
            elif board[i][j].color != self.color:
                moves.append((i, j))
                break
            else:
                break
        # Check top-left
        for i, j in zip(range(x - 1, -1, -1), range(y - 1, -1, -1)):
            if board[i][j] is None:
                moves.append((i, j))
            elif board[i][j].color != self.color:
                moves.append((i, j))
                break
            else:
                break
        # Check bottom-right
        for i, j in zip(range(x + 1, 8), range(y + 1, 8)):
            if board[i][j] is None:
                moves.append((i, j))
            elif board[i][j].color != self.color:
                moves.append((i, j))
                break
            else:
                break
        # Check bottom-left
        for i, j in zip(range(x + 1, 8), range(y - 1, -1, -1)):
            if board[i][j] is None:
                moves.append((i, j))
            elif board[i][j].color != self.color:
                moves.append((i, j))
                break
            else:
                break
        return moves

    def get_score(self):
        return 3

class Reina(Piece):
    def valid_moves(self, position, board):
        # Combine rook and bishop moves
        rook_moves = Torre(self.color).valid_moves(position, board)
        bishop_moves = Alfil(self.color).valid_moves(position, board)
        return rook_moves + bishop_moves

    def get_score(self):
        return 9

class Rey(Piece):
    def valid_moves(self, position, board):
        moves = []
        x, y = position
        # One square in any direction
        king_moves = [
            (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
            (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)
        ]
        for move in king_moves:
            if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                moves.append(move)
        return moves

    def get_score(self):
        return 0  # Kings are not scored for this logic