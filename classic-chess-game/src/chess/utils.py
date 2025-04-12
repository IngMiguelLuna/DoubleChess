def validate_move(start_pos, end_pos, board):
    piece = board[start_pos[0]][start_pos[1]]
    if not piece:
        return False  # No piece at the start position

    valid_moves = piece.valid_moves(start_pos, board)
    return end_pos in valid_moves

def convert_position_to_coordinates(position):
    # Convert chessboard position (e.g., 'e4') to board coordinates (e.g., (4, 4))
    col = ord(position[0].lower()) - ord('a')
    row = 8 - int(position[1])
    return (row, col)

def convert_coordinates_to_position(coordinates):
    # Convert board coordinates (e.g., (4, 4)) back to a chessboard position (e.g., 'e4')
    col = chr(coordinates[1] + ord('a'))
    row = str(8 - coordinates[0])
    return f"{col}{row}"

def is_check(board, player_color):
    # Check if the player's king is in check
    king_position = None
    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece and piece.color == player_color and piece.__class__.__name__ == "Rey":
                king_position = (x, y)
                break

    if not king_position:
        return False

    opponent_color = "black" if player_color == "white" else "white"
    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece and piece.color == opponent_color:
                if king_position in piece.valid_moves((x, y), board):
                    return True

    return False

def is_checkmate(board, player_color):
    # Determine if the player is in checkmate
    if not is_check(board, player_color):
        return False

    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece and piece.color == player_color:
                for move in piece.valid_moves((x, y), board):
                    # Simulate the move
                    original_piece = board[move[0]][move[1]]
                    board[move[0]][move[1]] = piece
                    board[x][y] = None

                    if not is_check(board, player_color):
                        # Undo the move
                        board[x][y] = piece
                        board[move[0]][move[1]] = original_piece
                        return False

                    # Undo the move
                    board[x][y] = piece
                    board[move[0]][move[1]] = original_piece

    return True