
from config import (
    RED, BLACK,
    RED_KING, BLACK_KING,
    EMPTY
)


def apply_move(board, move, player):

    new_board = [
        row[:] for row in board
    ]

    start_r, start_c = move.start

    piece = new_board[start_r][start_c]

    new_board[start_r][start_c] = EMPTY

    for row, col in move.captured:
        new_board[row][col] = EMPTY

    end_r, end_c = move.end

    # Promotion
    if piece == RED and end_r == 0:
        piece = RED_KING

    elif piece == BLACK and end_r == 7:
        piece = BLACK_KING

    new_board[end_r][end_c] = piece

    return new_board


def count_pieces(board, player):

    return sum(
        1
        for row in board
        for piece in row
        if piece * player > 0
    )


def get_winner(board, player):

    if count_pieces(board, -player) == 0:
        return player

    from game.moves import get_valid_moves

    if not get_valid_moves(board, player):
        return -player

    return None
