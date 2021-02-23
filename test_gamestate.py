from gamestate import GameState
from piece import Piece
import constants as c
import unittest
from copy import deepcopy


class TestGameState(unittest.TestCase):
    def test_create_game(self):
        game = GameState()
        piece1 = Piece(c.PLAYER1, 0, 1)
        piece2 = Piece(c.PLAYER2, 5, 2)
        self.assertEqual(game.square[0][0], None)
        self.assertEqual(game.square[1][1], None)
        self.assertEqual(game.square[3][5], None)
        self.assertNotEqual(game.square[0][1], None)
        self.assertEqual(game.square[0][1].x, piece1.x)
        self.assertEqual(game.square[0][1].y, piece1.y)
        self.assertEqual(game.square[0][1].king, piece1.king)
        self.assertEqual(game.square[0][1].row, piece1.row)
        self.assertEqual(game.square[0][1].col, piece1.col)
        self.assertEqual(game.square[0][1].player, piece1.player)
        self.assertNotEqual(game.square[5][2], None)
        self.assertEqual(game.square[5][2].x, piece2.x)
        self.assertEqual(game.square[5][2].y, piece2.y)
        self.assertEqual(game.square[5][2].king, piece2.king)
        self.assertEqual(game.square[5][2].row, piece2.row)
        self.assertEqual(game.square[5][2].col, piece2.col)
        self.assertEqual(game.square[5][2].player, piece2.player)

    def test_remove_a_piece(self):
        game = GameState()
        self.assertNotEqual(game.square[0][1], None)

        game.remove_a_piece(0, 1)
        self.assertEqual(game.square[0][1], None)

    def test_move_piece_to(self):
        game = GameState()
        piece1 = Piece(c.PLAYER1, 1, 2)
        self.assertEqual(game.square[3][0], None)
        self.assertNotEqual(game.square[1][2], None)

        game.move_piece_to(piece1, 3, 0)
        self.assertEqual(game.square[1][2], None)
        self.assertEqual(game.square[3][0].row, piece1.row)
        self.assertEqual(game.square[3][0].col, piece1.col)
        self.assertEqual(game.square[3][0].y, piece1.y)
        self.assertEqual(game.square[3][0].x, piece1.x)
        self.assertEqual(game.square[3][0].king, piece1.king)
        self.assertEqual(game.square[3][0].player, piece1.player)

    def test_remove_capture(self):
        game = GameState()
        piece1 = game.square[2][1]
        game.move_piece_to(piece1, 4, 1)
        game.remove_captured(5, 2, 3, 0)
        self.assertEqual(game.square[4][1], None)

    def test_is_on_board(self):
        game = GameState()
        self.assertTrue(game.is_on_board(0, 0))
        self.assertTrue(game.is_on_board(4, 5))
        self.assertFalse(game.is_on_board(-1, 0))
        self.assertFalse(game.is_on_board(8, 0))
        self.assertFalse(game.is_on_board(0, 8))

    def test_get_piece_moves(self):
        game = GameState()
        move1 = game.get_piece_moves(Piece(c.PLAYER1, 2, 1))
        move2 = game.get_piece_moves(Piece(c.PLAYER2, 4, 5))
        move3 = game.get_piece_moves(Piece(c.PLAYER1, 0, 1))
        self.assertEqual(move1.sort(), [[1, -1], [1, 1]].sort())
        self.assertEqual(move2.sort(), [[-1, -1], [-1, 1]].sort())
        self.assertEqual(move3, [])

    def test_get_player_moves(self):
        game = GameState()
        moves1 = game.get_player_moves(c.PLAYER1)
        moves2 = game.get_player_moves(c.PLAYER2)
        self.assertTrue(len(moves1) == len(moves2) == 4)

    def test_get_catcher(self):
        game = GameState()
        game.move_piece_to(game.square[2][3], 4, 3)
        game.move_piece_to(game.square[5][6], 3, 6)

        catchers_player1 = game.get_catchers(c.PLAYER1)
        catchers_player2 = game.get_catchers(c.PLAYER2)
        self.assertEqual(catchers_player2, [
                         game.square[5][2], game.square[5][4]])
        self.assertEqual(catchers_player1, [
                         game.square[2][5], game.square[2][7]])

    def test_is_catcher(self):
        game = GameState()
        game.move_piece_to(game.square[1][0], 4, 1)
        self.assertTrue(game.is_catcher(game.square[5][0]))
        self.assertTrue(game.is_catcher(game.square[5][2]))
        self.assertFalse(game.is_catcher(game.square[2][1]))
        self.assertFalse(game.is_catcher(game.square[5][4]))

    def test_get_piece_valid_moves(self):
        game = GameState()
        game.move_piece_to(game.square[1][0], 4, 1)
        piece1 = game.square[5][0]
        piece2 = game.square[5][2]
        piece3 = game.square[0][1]
        piece4 = game.square[1][2]
        piece5 = game.square[2][3]
        moves1 = game.get_piece_valid_moves(piece1)
        moves2 = game.get_piece_valid_moves(piece2)
        moves3 = game.get_piece_valid_moves(piece3)
        moves4 = game.get_piece_valid_moves(piece4)
        moves5 = game.get_piece_valid_moves(piece5)
        self.assertTrue((3, 2) in moves1)
        self.assertTrue((3, 0) in moves2)
        self.assertTrue((1, 0) in moves3)
        self.assertTrue(not moves4)
        self.assertTrue((3, 2) in moves5 and (3, 4) in moves5)
        self.assertTrue(len(moves1) == len(moves2) == len(moves3) == 1)
        self.assertTrue(len(moves5) == 2)

    def test_get_player_valid_moves(self):
        game = GameState()
        moves1, capture1 = game.get_player_valid_moves(c.PLAYER1)
        moves2, capture2 = game.get_player_valid_moves(c.PLAYER2)
        self.assertTrue(len(moves1) == len(moves2) == 4)
        self.assertTrue(not capture1 and not capture2)

        game.move_piece_to(game.square[2][1], 4, 1)
        moves3, capture3 = game.get_player_valid_moves(c.PLAYER1)
        moves4, capture4 = game.get_player_valid_moves(c.PLAYER2)
        self.assertTrue(len(moves3) == 5)
        self.assertTrue(len(moves4) == 4)
        self.assertTrue(not capture3)
        self.assertTrue(len(capture4) == 2)
        piece = game.square[5][2]
        piece2 = game.square[5][0]
        dict1 = {(3, 0): piece}
        dict2 = {(3, 2): piece2}
        self.assertTrue(dict1 in moves4 and dict1 in capture4)
        self.assertTrue(dict2 in moves4 and dict2 in capture4)

    def test_is_valid_piece(self):
        game = GameState()
        game.current_player = c.PLAYER2
        piece1 = game.square[5][4]
        piece2 = game.square[5][0]
        piece3 = game.square[2][3]

        self.assertTrue(game.is_valid_piece(piece1))
        self.assertTrue(game.is_valid_piece(piece2))
        self.assertFalse(game.is_valid_piece(piece3))

        game.move_piece_to(game.square[2][1], 4, 1)
        self.assertFalse(game.is_valid_piece(piece1))
        self.assertTrue(game.is_valid_piece(piece2))
        self.assertFalse(game.is_valid_piece(piece3))

        game.current_player = c.PLAYER1
        self.assertFalse(game.is_valid_piece(piece1))
        self.assertFalse(game.is_valid_piece(piece2))
        self.assertTrue(game.is_valid_piece(piece3))

    def test_select(self):
        game = GameState()
        game.select(5, 2)
        self.assertEqual(game.gamestage, c.NEW_TURN)
        game.select(4, 3)
        self.assertEqual(game.gamestage, c.NEW_TURN)
        game.select(1, 0)
        self.assertEqual(game.gamestage, c.NEW_TURN)
        game.select(2, 1)
        self.assertEqual(game.gamestage, c.SELECTED)

    def test_move(self):
        # capturing move
        game = GameState()
        game.move_piece_to(game.square[2][1], 4, 1)
        game.move_piece_to(game.square[1][2], 2, 1)
        game.current_player = c.PLAYER2
        game.selected = game.square[5][2]
        game.move(3, 0)
        # if catcher move again after move
        self.assertEqual(game.gamestage, c.SELECTED)
        self.assertEqual(game.square[4][1], None)
        self.assertEqual(game.selected, game.square[3][0])
        self.assertTrue(game.is_catcher(game.selected))
        dict1 = {(3, 0): game.square[3][0]}
        self.assertEqual(game.valid_moves, dict1)

        # non capturing move
        game = GameState()
        game.selected = game.square[2][1]
        self.assertEqual(game.square[3][0], None)
        game.move(3, 0)

        self.assertEqual(game.square[3][0].player, c.PLAYER1)
        self.assertTrue(game.square[2][1] is None)
        self.assertTrue(game.selected is None)
        self.assertTrue(game.gamestage, c.MOVED)
        self.assertFalse(game.valid_moves)

        # non valid move
        game.selected = game.square[1][2]
        game.move(2, 3)
        self.assertEqual(game.gamestage, c.NEW_TURN)
        self.assertFalse(game.valid_moves)

    def test_get_ai_state(self):
        game = GameState()
        # non-capturing move
        game.current_player = c.PLAYER2
        newstate = game.get_ai_state()
        self.assertNotEqual(game, newstate)
        empty_cell = 0
        empty_cell_newstate = 0
        # assert number of pieces are the same for both player
        for row in range(c.ROW):
            for col in range(c.COL):
                if game.square[row][col] == None:
                    empty_cell += 1
                if newstate[row][col] == None:
                    empty_cell_newstate += 1
        self.assertEqual(empty_cell, empty_cell_newstate)

        # capturing move
        game = GameState()
        game.current_player = c.PLAYER2
        piece1 = Piece(c.PLAYER1, 2, 1)
        game.move_piece_to(piece1, 4, 1)
        # get a deep copy of game to not alter origion gamestate
        newstate = deepcopy(game).get_ai_state()
        print(newstate[5][0], newstate[5][2])
        self.assertNotEqual(game, newstate)
        self.assertEqual(newstate[4][1], None)
        empty_cell = 0
        empty_cell_newstate = 0
        # assert number of pieces are not the same for both player
        for row in range(c.ROW):
            for col in range(c.COL):
                if game.square[row][col] == None:
                    empty_cell += 1
                if newstate[row][col] == None:
                    empty_cell_newstate += 1
        self.assertTrue((empty_cell_newstate - empty_cell) == 1)

    def test_ai_player_move(self):
        game = GameState()
        # not AI's turn
        game.ai_player_move()
        self.assertTrue(game.gamestage != c.MOVED)

        # AI's turen
        self.current_player = c.PLAYER2
        newstate = game.get_ai_state()
        self.assertTrue(game.square, newstate)
        self.assertTrue(game.gamestage == c.NEW_TURN)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
