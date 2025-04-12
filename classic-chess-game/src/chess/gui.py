import pygame
import os
from .game import ChessGame
from .pieces import Rey

class ChessGUI:
    def __init__(self, board):
        pygame.init()
        self.board = board
        self.screen = pygame.display.set_mode((800, 640))  # 640px for board + 160px for panels
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_assets()
        self.selected_piece = None
        self.valid_moves = []
        self.current_turn = "white"
        self.captured_white = []  # List to store pieces captured by black
        self.captured_black = []  # List to store pieces captured by white
        self.check_message = None  # Message to display when a player is in check
        self.check_message_timer = 0  # Timer for how long the message is displayed
        self.game = ChessGame()  # Initialize ChessGame to access game logic
        self.winner_message = None  # Message to display the winner

    def load_assets(self):
        self.assets = {}
        asset_path = os.path.join(os.path.dirname(__file__), "assets")
        self.assets = {
            "P": pygame.image.load(os.path.join(asset_path, "peon_blanco.png")),
            "p": pygame.image.load(os.path.join(asset_path, "peon_negro.png")),
            "R": pygame.image.load(os.path.join(asset_path, "torre_blanca.png")),
            "r": pygame.image.load(os.path.join(asset_path, "torre_negra.png")),
            "N": pygame.image.load(os.path.join(asset_path, "caballo_blanco.png")),
            "n": pygame.image.load(os.path.join(asset_path, "caballo_negro.png")),
            "B": pygame.image.load(os.path.join(asset_path, "alfil_blanco.png")),
            "b": pygame.image.load(os.path.join(asset_path, "alfil_negro.png")),
            "Q": pygame.image.load(os.path.join(asset_path, "reina_blanca.png")),
            "q": pygame.image.load(os.path.join(asset_path, "reina_negra.png")),
            "K": pygame.image.load(os.path.join(asset_path, "rey_blanco.png")),
            "k": pygame.image.load(os.path.join(asset_path, "rey_negro.png")),
        }

    def draw_board(self):
        # Draw a black border around the board
        pygame.draw.rect(self.screen, pygame.Color("black"), pygame.Rect(80, 0, 640, 640), 5)  # Border thickness of 5px

        # Adjust board drawing to leave space for panels
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(self.screen, color, pygame.Rect(80 + col * 80, row * 80, 80, 80))

    def draw_pieces(self):
        # Adjust piece drawing to align with the shifted board
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    piece_str = str(piece)
                    self.screen.blit(self.assets[piece_str], (80 + col * 80, row * 80))

    def draw_captured_pieces(self):
        # Draw background for captured pieces panels
        pygame.draw.rect(self.screen, pygame.Color("gray"), pygame.Rect(0, 0, 80, 640))  # Left panel
        pygame.draw.rect(self.screen, pygame.Color("gray"), pygame.Rect(720, 0, 80, 640))  # Right panel

        # Draw captured pieces on the left (black's captures) and right (white's captures)
        for i, piece in enumerate(self.captured_black):
            self.screen.blit(self.assets[str(piece)], (10, i * 40))  # Left panel
        for i, piece in enumerate(self.captured_white):
            self.screen.blit(self.assets[str(piece)], (730, i * 40))  # Right panel

    def handle_click(self, pos):
        row, col = pos[1] // 80, (pos[0] - 80) // 80
        if self.selected_piece:
            print(f"Intentando mover pieza seleccionada desde {self.selected_piece} a {(row, col)}")
            # If a piece is already selected, try to move it
            if (row, col) in self.valid_moves:
                piece = self.board[self.selected_piece[0]][self.selected_piece[1]]
                target_piece = self.board[row][col]
                if piece.color == self.current_turn and (not target_piece or target_piece.color != self.current_turn):
                    if target_piece:
                        print(f"DEBUG: {target_piece} ha sido capturada.")  # Flag for captured piece
                        if isinstance(target_piece, Rey):
                            self.winner_message = "Black Wins!" if target_piece.color == "white" else "White Wins!"
                            self.screen.fill(pygame.Color("black"))  # Clear the screen
                            self.display_winner_message()
                            pygame.display.flip()
                            pygame.time.wait(3000)  # Wait for 3 seconds before closing
                            self.running = False
                            return
                        if target_piece.color == "white":
                            self.captured_black.append(target_piece)
                        else:
                            self.captured_white.append(target_piece)
                    print(f"Movimiento válido: {piece} movido a {(row, col)}")
                    self.board[row][col] = piece
                    self.board[self.selected_piece[0]][self.selected_piece[1]] = None
                    self.selected_piece = None
                    self.valid_moves = []
                    # Switch turn after a valid move
                    self.current_turn = "black" if self.current_turn == "white" else "white"
                    print(f"Turno cambiado a: {self.current_turn}")
                else:
                    print("Movimiento inválido: no puedes capturar tus propias piezas.")
            else:
                print("Movimiento inválido: posición seleccionada no está en los movimientos válidos.")
                self.selected_piece = None
                self.valid_moves = []
        elif self.board[row][col]:
            # Select a piece if clicked on it
            piece = self.board[row][col]
            if piece.color == self.current_turn:
                self.selected_piece = (row, col)
                self.valid_moves = [move for move in piece.valid_moves((row, col), self.board) if not self.board[move[0]][move[1]] or self.board[move[0]][move[1]].color != self.current_turn]
                print(f"Pieza seleccionada: {piece} en {self.selected_piece}. Movimientos válidos: {self.valid_moves}")
            else:
                print("No puedes seleccionar piezas del oponente.")
        else:
            print("No hay pieza en la posición seleccionada.")

    def draw_valid_moves(self):
        for move in self.valid_moves:
            pygame.draw.circle(self.screen, pygame.Color("green"), (80 + move[1] * 80 + 40, move[0] * 80 + 40), 10)

    def display_check_message(self):
        if self.check_message and self.check_message_timer > 0:
            font = pygame.font.Font(None, 36)
            text = font.render(self.check_message, True, pygame.Color("red"))
            text_rect = text.get_rect(center=(400, 320))  # Centered on the screen
            self.screen.blit(text, text_rect)
            self.check_message_timer -= 1

    def handle_check(self):
        if self.is_in_check("white"):
            self.check_message = "Check to White!"
            self.check_message_timer = 180  # Display for 3 seconds (at 60 FPS)
        elif self.is_in_check("black"):
            self.check_message = "Check to Black!"
            self.check_message_timer = 180
        else:
            self.check_message = None

    def is_in_check(self, color):
        return self.game.is_in_check(color)

    def display_winner_message(self):
        if self.winner_message:
            font = pygame.font.Font(None, 48)
            text = font.render(self.winner_message, True, pygame.Color("gold"))
            text_rect = text.get_rect(center=(400, 320))  # Centered on the screen
            self.screen.blit(text, text_rect)

    def check_winner(self):
        if not self.game.is_king_alive("white"):
            self.winner_message = "Black Wins!"
            return True
        elif not self.game.is_king_alive("black"):
            self.winner_message = "White Wins!"
            return True
        return False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.winner_message:
                    print("DEBUG: Click detected")  # Debug message
                    self.handle_click(pygame.mouse.get_pos())

            if self.check_winner():
                print("DEBUG: Winner detected")  # Debug message
                self.screen.fill(pygame.Color("black"))  # Clear the screen
                self.display_winner_message()
                pygame.display.flip()
                pygame.time.wait(3000)  # Wait for 3 seconds before closing
                self.running = False
                continue

            if not self.winner_message:
                self.handle_check()  # Check for check conditions
                self.draw_board()
                self.draw_pieces()
                self.draw_valid_moves()
                self.draw_captured_pieces()
                self.display_check_message()  # Display check message if applicable

            pygame.display.flip()
            self.clock.tick(30)

        print("DEBUG: Exiting game loop")  # Debug message
        pygame.quit()