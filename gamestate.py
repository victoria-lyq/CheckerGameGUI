'''
Yaqi (Victoria) Liu
CS 5002, Fall 2020 - Final Project
This file handles everything related to the game state as well as all logic.
'''
from piece import Piece
import constants as c
import random


class GameState:
    '''
        Class -- GameState
            The state of the game.
        Attributes:
            square -- A nested list storing the state of each square on the
            board.
            selected -- represent selected piece
            current_player -- the player allowed to select a piece
            valid_moves -- a dictionary collecting all valid moves a player
            can make. 
            capture_direction -- a nested list. Each sub list indicating
            direction of a captuirng move.
            gamestate -- represents the stage of a player's turn
        Method:
            get_piece_valid_move -- Find all valid moves a piece can make
            get_player_valid_moves -- Find all valid moves a player can make
            select -- Updates the squares list when the user selects a piece.
            Highlight valid moves for selected piece. Also updates the stage
            of the turn.
            move -- Updates the squares list when the user selects an empty
            square. Move previously select piece to an empty square. Remove
            valid moves highlight if invalid selection. Also updates the
            stage of the turn.
            ai_player_move -- Initiates a computer plater's move.
    '''

    def __init__(self):
        '''
            Constructor -- Creates a new instance of GameState
            Parameters:
                self -- The current GameState object.
        '''
        self.square = []
        self.selected = None
        self.current_player = c.PLAYER1
        self.valid_moves = {}
        self.capture_direction = [[2, 2], [2, -2], [-2, 2], [-2, -2]]
        self.gamestage = c.NEW_TURN

        self.create_game()

    def create_game(self):
        '''
            Method -- create_game
               populates the square list with Piece objects
            Parameters:
                self -- the current GameState object
        '''
        for row in range(c.ROW):
            self.square.append([])
            for col in range(c.COL):
                if col % 2 != row % 2 and row < 3:
                    self.square[row].append(Piece(c.PLAYER1, row, col))
                elif col % 2 != row % 2 and row > 4:
                    self.square[row].append(Piece(c.PLAYER2, row, col))
                else:
                    self.square[row].append(None)

    def remove_a_piece(self, row, col):
        '''
            Method -- remove_a_piece
               replace a Piece objects with None in the square list
            Parameters:
                self -- the current GameState object
                row -- the index of the cell row
                col -- the index of the cell column
        '''
        self.square[row][col] = None

    def move_piece_to(self, piece, row, col):
        ''''
            Method -- move_piece_to
               replace a Piece objects with None in the square list
               and add the same piece at a given cell. 
            Parameters:
                self -- the current GameState object
                piece -- A Piece object. 
                row -- the index of the cell row
                col -- the index of the cell column
        '''
        start_row, start_col = piece.row, piece.col
        self.square[start_row][start_col] = None
        self.square[row][col] = piece
        if row == 0 or row == c.ROW - 1:
            piece.make_king()
        piece.change_pos(row, col)

    def remove_captured(self, start_row, start_col, end_row, end_col):
        '''
            Method -- remove_captured
               replace a captured Piece objects with None in the square list
            Parameters:
                self -- the current GameState object
                piece -- A Piece object. 
                start_row -- the index of the cell row where a capturing
                piece is moved from.
                start_col -- the index of the cell column where a capturing
                piece is moved from.
                end_row -- the index of the cell row where a capturing
                piece is moved to.
                end_col -- the index of the cell column where a capturing
                piece is moved to.
        '''
        capture_row = int(start_row + (end_row - start_row) / 2)
        capture_col = int(start_col + (end_col - start_col) / 2)
        self.remove_a_piece(capture_row, capture_col)

    def is_on_board(self, row, col):
        '''
            Method -- is_on_board
                Checks if a cell was in range of the square list.
            Parameters:
                self -- the current GameState object
                row -- the index of the cell row
                col -- the index of the cell column
            Returns:
                True if the click is in range, False otherwise.
        '''
        return row in range(c.ROW) and col in range(c.COL)

    def get_piece_moves(self, piece):
        '''
            Method -- get_piece_moves
                Find all moves a piece can make
            Parameters:
                self -- the current GameState object
                piece -- A Piece object.
            Returns:
                A nested list represents a Piece's direction information
                e.g. for a regular black piece, the list would be
                [[1, -1], [1, 1]], which translates to up-left and up-right.
        '''
        moves = []
        for item in piece.direction:
            to_row = piece.row + item[0]
            to_col = piece.col + item[1]
            # append direction for non-capture move
            if self.is_on_board(to_row, to_col) and \
                    self.square[to_row][to_col] == None:
                moves.append(item)
            # move to cell contains an enemy piece then skip and capture
            elif self.is_on_board(to_row, to_col) and \
                    self.square[to_row][to_col].player != piece.player:
                to_row = to_row + item[0]
                to_col = to_col + item[1]
                # append direction for capture move
                if self.is_on_board(to_row, to_col) and \
                        self.square[to_row][to_col] == None:
                    r = to_row - piece.row
                    c = to_col - piece.col
                    moves.insert(0, [r, c])
        return moves

    def get_player_moves(self, player):
        '''
            Method -- get_player_moves
                Find all moves a player can make
            Parameters:
                self -- the current GameState object
                player -- A string that indicates the player's color
            Returns:
                A dictionary. The keys represent all the Pieces a player
                can select to move and the values represents a
                Piece's direction information.
        '''
        moves = {}
        for row in range(c.ROW):
            for col in range(c.COL):
                piece = self.square[row][col]
                if self.square[row][col] and \
                        self.square[row][col].player == player:
                    piece_move = self.get_piece_moves(piece)
                    if piece_move:
                        moves[piece] = piece_move
        return moves

    def get_catchers(self, player):
        '''
            Method -- get_catchers
                Find all pieces that can capture a enemy piece for a player
            Parameters:
                self -- the current GameState object
                player -- A string that indicates the player's color
            Returns:
                A list of Pieces objects that can make capture move
        '''
        pieces = []
        moves = self.get_player_moves(player)
        for key, val in moves.items():
            for i in val:
                if i in self.capture_direction and i not in pieces:
                    pieces.append(key)
        return pieces

    def is_catcher(self, piece):
        '''
            Method -- is_catchers
                Determine whether a piece can make capture move or not
            Parameters:
                self -- the current GameState object
                piece -- A Piece object
            Returns:
                True if it can make capture move, false otherwise
        '''
        catchers = self.get_catchers(piece.player)
        return piece in catchers

    def get_piece_valid_moves(self, piece):
        '''
            Method -- get_piece_valid_moves
                Find all valid moves a piece can make
            Parameters:
                self -- the current GameState object
                piece -- A Piece object
            Returns:
                A dictionary. The keys represent all the Pieces a player
                can select to make valid moves and the values represents
                a Piece's direction information.
        '''
        moves = self.get_piece_moves(piece)
        valid_moves = {}
        if self.is_catcher(piece):
            for i in moves:
                if i in self.capture_direction:
                    to_row = piece.row + i[0]
                    to_col = piece.col + i[1]
                    valid_moves[(to_row, to_col)] = piece
        else:
            for i in moves:
                to_row = piece.row + i[0]
                to_col = piece.col + i[1]
                valid_moves[(to_row, to_col)] = piece
        return valid_moves

    def get_player_pieces(self, player):
        '''
            Method -- get_player_pieces
                Find all pieces and king pieces that belong to a player
            Parameters:
                self -- the current GameState object
                player -- A string that indicates the player's color
            Returns:
                A list of all pieces belongs to a player and a list
                of all king pieces belongs to the same player
        '''
        pieces = []
        kings = []
        for row in self.square:
            for piece in row:
                if piece is not None and piece.player == player:
                    pieces.append(piece)
                if piece is not None and piece.king:
                    kings.append(piece)
        return pieces, kings

    def get_player_valid_moves(self, player):
        '''
            Method -- get_player_valid_moves
                Find all valid moves a player can make
            Parameters:
                self -- the current GameState object
                player -- A string that indicates the player's color
            Returns:
                A list of all valid moves a player can make and a list
                of all capturing moves a player can make. each move is
                a dictionary. The keys represent all the Pieces a player
                can select to make valid moves and the values represents
                a Piece's direction information.
        '''
        capture_moves = []
        valid_moves = []
        for piece in self.get_player_pieces(player)[0]:
            valid_move = self.get_piece_valid_moves(piece)
            if valid_move:
                valid_moves.append(valid_move)
            if self.is_catcher(piece):
                capture_moves.append(valid_move)
        return valid_moves, capture_moves

    def is_valid_piece(self, piece):
        '''
            Method -- is_valid_piece
                Determine whether a piece belongs to current player
                and can make valid move or not.
            Parameters:
                self -- the current GameState object
                piece -- A Piece object
            Returns:
                True if it's a valid piece, false otherwise
        '''
        catcher = self.get_catchers(piece.player)
        if piece.player != self.current_player or \
                not self.get_piece_valid_moves(piece) or \
                (catcher and piece not in catcher):
            return False
        return True

    def select(self, row, col):
        '''
                Method -- select
                Updates the squares list when the user selects a piece.
                Highlight valid moves for selected piece. Also
                updates the stage of the turn.
            Parameters:
                self -- the current GameState object
                row -- the row of the square that was clicked
                col -- the column of the square that was clicked
            Returns:
                Selected Piece object if the selection is valid.
        '''
        self.selected = self.square[row][col]
        if self.selected is None \
            or self.selected.player != self.current_player \
                or not self.is_valid_piece(self.selected):
            # print("Not a valid piece!") for debugging
            self.gamestage = c.NEW_TURN
        elif self.is_valid_piece(self.selected):
            self.gamestage = c.SELECTED
            return self.selected
        else:
            self.gamestage = c.NEW_TURN

    def move(self, row, col):
        '''
            Method -- move
                Updates the squares list when the user selects an empty
                square. Move previously select piece to an empty square.
                Remove valid moves highlight if invalid selection.
                Also updates the stage of the turn.
            Parameters:
                self -- the current GameState object
                row -- the row of the square that was clicked
                col -- the column of the square that was clicked
            Returns:
                Return selected Piece object if the selection is invalid.
        '''
        to_cell = self.square[row][col]
        self.valid_moves = self.get_piece_valid_moves(self.selected)
        if to_cell == None and (row, col) in self.valid_moves:
            print("valid move")
            if self.is_catcher(self.selected):
                self.remove_captured(self.selected.row,
                                     self.selected.col, row, col)
                self.move_piece_to(self.selected, row, col)
                if self.is_catcher(self.selected):
                    self.gamestage = c.SELECTED
                    return self.selected
            else:
                self.move_piece_to(self.selected, row, col)
            self.valid_moves = {}
            self.selected = None
            self.gamestage = c.MOVED

        else:
            self.valid_moves = {}
            self.selected = None
            self.gamestage = c.NEW_TURN
        return

    def ai_possible_move(self):
        '''
            Metod -- ai_possible_move
                Find a possible valid move for computer player
            Parameters:
                self -- the current GameState object
            Returns:
                A Piece Object and index of row and column for
                it's valid move
        '''
        move, advance_move = self.get_player_valid_moves(c.PLAYER2)
        if not move and not advance_move:
            print("Game over! BLACK is the winner.")
            return
        elif len(advance_move) != 0:
            move = random.choice(advance_move)
        else:
            move = random.choice(move)
        for key, value in move.items():
            row = key[0]
            col = key[1]
            piece = value
        return piece, row, col

    def get_ai_state(self):
        '''
            Method -- get_ai_state
                Find gamestate after a computer player's move
            Parameters:
                self -- the current GameState object
            Returns:
                Square list after a computer player's move
        '''
        piece, row, col = self.ai_possible_move()
        if self.is_catcher(piece):
            self.remove_captured(piece.row, piece.col, row, col)
            self.move_piece_to(piece, row, col)
            if self.is_catcher(piece):
                self.get_ai_state()
        else:
            self.move_piece_to(piece, row, col)
        return self.square

    def ai_player_move(self):
        '''
            Method -- ai_player_move
                Initiate a computer plater's move. Ends if not ai's turn.
            Parameters:
                self -- the current GameState object
        '''
        if self.gamestage != c.MOVED:
            return
        self.square = self.get_ai_state()
        self.gamestage = c.NEW_TURN
