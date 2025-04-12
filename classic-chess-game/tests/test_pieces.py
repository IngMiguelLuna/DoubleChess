import unittest
from src.chess.pieces import Peon, Torre, Caballo, Alfil, Reina, Rey

class TestPieces(unittest.TestCase):

    def setUp(self):
        self.peon = Peon()
        self.rook = Torre()
        self.knight = Caballo()
        self.bishop = Alfil()
        self.queen = Reina()
        self.rey = Rey()

    def test_peon_moves(self):
        self.assertEqual(self.peon.valid_moves((1, 1)), [(2, 1), (3, 1)])  # Example moves for a peon

    def test_rook_moves(self):
        self.assertEqual(self.rook.valid_moves((0, 0)), [(0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)])  # Example moves for a rook

    def test_knight_moves(self):
        self.assertEqual(self.knight.valid_moves((1, 0)), [(2, 2), (0, 2)])  # Example moves for a knight

    def test_bishop_moves(self):
        self.assertEqual(self.bishop.valid_moves((2, 2)), [(3, 3), (4, 4), (1, 1), (0, 0)])  # Example moves for a bishop

    def test_queen_moves(self):
        self.assertEqual(self.queen.valid_moves((3, 3)), [(3, 4), (3, 5), (3, 6), (3, 7), (4, 3), (5, 3), (6, 3), (7, 3)])  # Example moves for a queen

    def test_rey_moves(self):
        self.assertEqual(self.rey.valid_moves((4, 4)), [(4, 5), (5, 5), (5, 4), (5, 3), (4, 3)])  # Example moves for a rey

if __name__ == '__main__':
    unittest.main()