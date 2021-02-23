'''
Yaqi (Victoria) Liu
CS 5002, Fall 2020 - Final Project
This file handles everything related to Turtle and the UI.
'''
import turtle
import constants as c
from piece import Piece
from gamestate import GameState


class Board:
    '''
        Class -- Board
            The UI
        Attributes:
            gamestate -- A GameState object, used to keep track of
            the status of the squares and the current "turn"
            pen -- Object of tutle pen responsoble for drawing
            high_bound -- The positive edge of the board.
            low_bound -- The negative edge of the board.
            screen -- An instance of TurtleScreen
        Methods:
            (none intended to be accessed outside the class)
    '''

    def __init__(self):
        '''
            Constructor -- creates a new instance of Board
            Parameter:
            self -- The current Board object
        '''
        self.state = GameState()

        turtle.setup(c.WIDTH + c.SQUARE_SIZE, c.HEIGHT + c.SQUARE_SIZE)
        turtle.screensize(c.WIDTH, c.HEIGHT)
        turtle.bgcolor("white")
        turtle.tracer(0, 0)

        # Create the Turtle to draw the board
        self.pen = turtle.Turtle()
        self.pen.penup()
        self.pen.hideturtle()

        # Draw the board and pieces
        self.draw_state()

        # "Convenience attributes" used for drawing
        self.high_bound = 0 - c.CORNER
        self.low_bound = c.CORNER

        self.screen = turtle.Screen()
        self.screen.onclick(self.clickhandler)
        turtle.done()  # Stops the window from closing.

    def draw_square(self, size):
        '''
            Method -- draw_SQUARE
                Draws a squre of a given size.
            Parameters:
                self -- the current Board object
                width -- the width of each side
        '''
        RIGHT_ANGLE = 90
        self.pen.begin_fill()
        self.pen.pendown()
        for i in range(4):
            self.pen.forward(size)
            self.pen.left(RIGHT_ANGLE)
        self.pen.end_fill()
        self.pen.penup()

    def draw_circle(self, color, size):
        '''
            Method -- draw_circle
                Draws a circle of a given size.
            Parameter:
                self -- The current Board object
                color -- a strings that indicates the fill color.
                size -- the radius of the circle
        '''
        self.pen.pendown()
        self.pen.color(color)
        self.pen.begin_fill()
        self.pen.circle(size)
        self.pen.end_fill()
        self.pen.penup()

    def draw_board(self):
        '''
            Method -- draw_board
                draw a patterned checker board on graphic window
            Parameter:
                self -- The current Board object
        '''
        # board outline
        # The first parameter is the outline color, the second is the fille
        self.pen.color("black", c.SQUARE_COLORS[1])
        self.pen.setposition(c.CORNER, c.CORNER)
        self.draw_square(c.WIDTH)
        # board pattern
        self.pen.color("black", c.SQUARE_COLORS[0])
        for row in range(c.ROW):
            for col in range(c.COL):
                if col % 2 != row % 2:
                    self.pen.setposition(
                        c.CORNER + c.SQUARE_SIZE * col, c.CORNER + c.SQUARE_SIZE * row)
                    self.draw_square(c.SQUARE_SIZE)

    def draw_state(self):
        '''
            Method -- draw_state
                draw check pieces on graphic window
            Parameter:
                self -- The current Board object
        '''
        self.draw_board()
        for row in range(c.ROW):
            for col in range(c.COL):
                piece = self.state.square[row][col]
                if piece is not None:
                    self.draw_a_piece(piece)
                    if piece.king:
                        self.draw_king(piece)

    def draw_king(self, piece):
        '''
            Method -- draw_king
                Draw pattern indicates king piece on a given piece
            Parameter:
                self -- The current Board object
                piece -- a Piece object
        '''
        self.pen.setposition(piece.x, piece.y)
        self.pen.color("white")
        self.pen.pendown()
        self.pen.write(u'♔', align="center", font=("Comic Sans MS",
                                                   round(c.SQUARE_SIZE * 0.8), "normal"))
        self.pen.penup()

    def row_col_to_xy(self, row, col):
        '''
            Method -- row_col_to_xy
                Converts a cell location to coordinate
            Parameter:
                self -- the current Board object
                row -- the index of the cell row
                col -- the index of the cell column
            Returns
                (x, y) -- a tuple representing the coordinates of the cell.
        '''
        y = row * c.SQUARE_SIZE - 1/2 * c.WIDTH
        x = col * c.SQUARE_SIZE - 1/2 * c.HEIGHT
        return (x, y)

    def is_in_bound(self, x, y):
        '''
            Method -- is_in_bound
                Checks if the click was in bounds of the board.
            Parameters:
                self -- the current Board object
                x -- the X coordinate of the click
                y -- the Y coordinate of the click
            Returns:
                True if the click is in bounds, False otherwise.
        '''
        if x >= self.low_bound and x <= self.high_bound and \
           y >= self.low_bound and y <= self.high_bound:
            return True
        return False

    def reset_square(self, row, col):
        '''
            Method -- reset_square
                draw a grey square at a given cell.
            Parameters:
                self -- the current Board object
                row -- the index of the cell row
                col -- the index of the cell column
        '''
        self.pen.color("black", c.SQUARE_COLORS[0])
        self.pen.goto(self.row_col_to_xy(row, col))
        self.draw_square(c.SQUARE_SIZE)

    def draw_a_piece(self, piece):
        '''
            Method -- draw_a_piece
                draw a piece object on graphic board.
            Parameters:
                self -- the current Board object
                piece -- A Piece object
        '''
        self.pen.setposition(piece.x, piece.y)
        self.draw_circle(piece.player, c.PIECE_SIZE)

    def reset_captured_square(self, start_row, start_col, end_row, end_col):
        '''
            Method -- reset_captured_square
                draw a grey square at a given cell to replace 
                the captured piece.
            Parameters:
                self -- the current Board object
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
        self.reset_square(capture_row, capture_col)

    def draw_valid_moves(self, moves):
        '''
            Method -- draw_valid_moves
                draw a yellow square to indicates where a slected
                piece can move to.
            Parameters:
                self -- the current Board object
                moves -- a tuple indicates the row and col index of
                a cell
        '''
        for move in moves:
            row, col = move
            x = (col + 0.25) * c.SQUARE_SIZE - 1/2 * c.HEIGHT
            y = (row + 0.25) * c.SQUARE_SIZE - 1/2 * c.WIDTH
            self.pen.goto(x, y)
            self.pen.color(c.VALID_MOVE)
            self.draw_square(0.5 * c.SQUARE_SIZE)

    def remove_valid_moves(self, moves):
        '''
            Method -- draw_valid_moves
                remove the yellow square that indicates where a slected
                piece can move to.
            Parameters:
                self -- the current Board object
                moves -- a tuple indicates the row and col index of
                a cell
        '''
        for move in moves:
            row, col = move
            if self.state.square[row][col] is None:
                self.reset_square(row, col)

    def clickhandler(self, x, y):
        '''
            Method -- clickhandler
                The click event listener. If it's a new turn, triggers the next
                step: select a piece on the board.
            Parameters:
                self -- the current Board object
                x -- The X coordinate of the click
                y -- The Y coordinate of the click
        '''
        # get the row and column for a click at (x,y)
        col = int((x + 1/2 * c.WIDTH) // c.SQUARE_SIZE)
        row = int((y + 1/2 * c.HEIGHT) // c.SQUARE_SIZE)

        if self.is_in_bound(x, y) and self.state.gamestage == c.NEW_TURN:
            self.state.select(row, col)
            if self.state.gamestage == c.SELECTED:
                possible_moves = self.state.get_piece_valid_moves(
                    self.state.selected)
                self.draw_valid_moves(possible_moves)
            return

        if self.is_in_bound(x, y) and self.state.gamestage == c.SELECTED:
            self.state.move(row, col)
            self.draw_state()
            if self.state.gamestage == c.SELECTED:
                possible_moves = self.state.get_piece_valid_moves(
                    self.state.selected)
                self.draw_valid_moves(possible_moves)

        if self.state.gamestage == c.MOVED:
            print("AI's turn")
            self.state.ai_player_move()
            self.draw_state()
            move, capture_move = self.state.get_player_valid_moves(c.PLAYER1)
            if not move and not capture_move:
                print("Game over! RED is the winner")
