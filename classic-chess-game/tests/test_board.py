import unittest
from src.chess.board import Board

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_initialization(self):
        self.assertEqual(len(self.board.board), 8)
        self.assertEqual(len(self.board.board[0]), 8)

    def test_display_board(self):
        self.assertIsNone(self.board.display_board())

    def test_make_move(self):
        self.board.make_move((1, 0), (3, 0))  # Move a peon
        self.assertEqual(self.board.board[3][0].piece_type, 'Peon')
        self.assertIsNone(self.board.board[1][0].piece_type)

    def test_invalid_move(self):
        with self.assertRaises(ValueError):
            self.board.make_move((0, 0), (0, 1))  # Invalid move for a rook

if __name__ == '__main__':
    unittest.main()