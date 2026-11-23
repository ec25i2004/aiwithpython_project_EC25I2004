
import copy

from config import (
    ROWS, COLS,
    RED, BLACK,
    EMPTY,
    RED_KING, BLACK_KING
)


class Board:

    def __init__(self):
        self.board = [
            [EMPTY for _ in range(COLS)]
            for _ in range(ROWS)
        ]

        self.red_left = 12
        self.black_left = 12

        self.red_kings = 0
        self.black_kings = 0

        self.create_board()

    def create_board(self):

        for row in range(ROWS):

            for col in range(COLS):

                if (row + col) % 2 == 1:

                    if row < 3:
                        self.board[row][col] = BLACK

                    elif row > 4:
                        self.board[row][col] = RED

    def print_board(self):

        symbols = {
            EMPTY: ".",
            RED: "R",
            BLACK: "B",
            RED_KING: "RK",
            BLACK_KING: "BK"
        }

        for row in self.board:
            print(" ".join(symbols[piece] for piece in row))

    def get_piece(self, row, col):

        return self.board[row][col]

    def move(self, start, end):

        r1, c1 = start
        r2, c2 = end

        piece = self.board[r1][c1]

        self.board[r1][c1] = EMPTY
        self.board[r2][c2] = piece

        # King promotion
        if piece == RED and r2 == 0:
            self.board[r2][c2] = RED_KING

        elif piece == BLACK and r2 == 7:
            self.board[r2][c2] = BLACK_KING

        return self

    def remove(self, pieces):

        for row, col in pieces:

            piece = self.board[row][col]

            if piece == RED:
                self.red_left -= 1

            elif piece == BLACK:
                self.black_left -= 1

            elif piece == RED_KING:
                self.red_left -= 1
                self.red_kings -= 1

            elif piece == BLACK_KING:
                self.black_left -= 1
                self.black_kings -= 1

            self.board[row][col] = EMPTY

    def winner(self):

        if self.red_left <= 0:
            return BLACK

        if self.black_left <= 0:
            return RED

        return None

    def clone(self):

        return copy.deepcopy(self)
