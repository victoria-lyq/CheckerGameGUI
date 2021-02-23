from piece import Piece
import constants as c
import unittest


class TestPiece(unittest.TestCase):
    def test_array_to_xy(self):
        piece1 = Piece(c.PLAYER1, 1, 0)
        piece2 = Piece(c.PLAYER2, 6, 5)
        self.assertEqual(piece1.x, -175)
        self.assertEqual(piece1.y, -150)
        self.assertEqual(piece2.x, 75)
        self.assertEqual(piece2.y, 100)

    def test_make_king(self):
        piece_a = Piece(c.PLAYER1, 7, 1)
        piece_a.make_king()
        piece_b = Piece(c.PLAYER2, 7, 4)
        self.assertTrue(piece_a.king)
        self.assertEqual(piece_a.direction, (
            [1, 1], [1, -1], [-1, 1], [-1, -1]))
        self.assertFalse(piece_b.king)
        self.assertEqual(piece_b.direction, ([-1, 1], [-1, -1]))

    def test_change_pos(self):
        piece_a = Piece(c.PLAYER1, 1, 0)
        piece_a.change_pos(2, 1)
        self.assertEqual(piece_a.row, 2)
        self.assertEqual(piece_a.col, 1)
        self.assertEqual(piece_a.x, -125)
        self.assertEqual(piece_a.y, -100)
        piece_a.change_pos(3, 2)
        self.assertEqual(piece_a.row, 3)
        self.assertEqual(piece_a.col, 2)
        self.assertEqual(piece_a.x, -75)
        self.assertEqual(piece_a.y, -50)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
