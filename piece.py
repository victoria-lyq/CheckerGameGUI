'''
Yaqi (Victoria) Liu
CS 5002, Fall 2020 - Final Project
This file handles everything related to the check pieces.
'''
import constants as c
import unittest


class Piece:
    '''
        Class -- Piece
            The checker piece
        Attributes:
            player -- A string representing player's color
            row -- An integer representing the row of the cell or
            the 1st dimension of square list
            col -- An interger representing the column of the cell
            or the 2nd dimention of square list
        Method:
            make_king -- Change a piece's valid moving direction when it
            becomes a king piece
            change_pos -- Change a piece's row and column index
            when it is moved to an empty cell
    '''

    def __init__(self, player, row, col):
        '''
            Constructor --  create a new instant of Piece
            Parameters:
                self -- The current Piece Object
                player -- A string that indicates the player's color
                row -- The index of the cell row
                col -- The index of the cell column
        '''
        self.player = player
        self.row = row
        self.col = col
        self.king = False

        self.x = 0
        self.y = 0
        self.array_to_xy()

        if self.player == c.PLAYER1:
            self.direction = ([1, 1], [1, -1])
        else:
            self.direction = ([-1, 1], [-1, -1])

    def array_to_xy(self):
        '''
            Method -- array_to_xy
                Converts a piece location to coordinate
            Parameters:
                self -- The current Piece Object
        '''
        self.x = self.col * c.SQUARE_SIZE + 0.5 * c.SQUARE_SIZE - 1/2 * c.HEIGHT
        self.y = self.row * c.SQUARE_SIZE - 1/2 * c.WIDTH

    def make_king(self):
        '''
            Method -- make_king
                Change a piece's valid moving direction when it
                becomes a king piece
            Parameters:
                self -- The current Piece Object
        '''
        self.king = True
        self.direction = ([1, 1], [1, -1], [-1, 1], [-1, -1])

    def change_pos(self, row, col):
        '''
            Method -- change_pos
                Change a piece location when it is moved to an empty cell.
            Parameters:
                self -- The current Piece Object
        '''
        self.row = row
        self.col = col
        self.array_to_xy()

    def __repr__(self):
        '''
            Method -- __repr__
                Returns a printable representation of the piece
            Parameters:
                self -- The current Piece Object
            Returns:
                A printable representation of the piece's player
                and it's location.
        '''
        return str(self.player)
