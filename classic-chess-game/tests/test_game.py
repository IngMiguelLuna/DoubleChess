import unittest
from src.chess.game import Game

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_initial_turn(self):
        self.assertEqual(self.game.current_turn, 'white')

    def test_valid_move(self):
        self.game.make_move('e2', 'e4')
        self.assertEqual(self.game.board.get_piece('e4').color, 'white')

    def test_invalid_move(self):
        with self.assertRaises(ValueError):
            self.game.make_move('e2', 'e5')  # Invalid move for a peon

    def test_check_condition(self):
        self.game.make_move('e2', 'e4')
        self.game.make_move('e7', 'e5')
        self.game.make_move('g1', 'f3')
        self.game.make_move('b8', 'c6')
        self.game.make_move('f3', 'e5')  # This should put the black rey in check
        self.assertTrue(self.game.is_in_check('black'))

    def test_checkmate_condition(self):
        # Set up a checkmate scenario
        self.game.make_move('e2', 'e4')
        self.game.make_move('e7', 'e5')
        self.game.make_move('g1', 'f3')
        self.game.make_move('b8', 'c6')
        self.game.make_move('f3', 'e5')
        self.game.make_move('d7', 'd6')
        self.game.make_move('e5', 'f7')  # Checkmate move
        self.assertTrue(self.game.is_checkmate('black'))

if __name__ == '__main__':
    unittest.main()