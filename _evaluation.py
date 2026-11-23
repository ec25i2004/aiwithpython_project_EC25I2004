
from config import RED, BLACK, RED_KING, BLACK_KING


def evaluate(board, player=BLACK):

    score = 0

    for row in range(8):

        for col in range(8):

            piece = board[row][col]

            if piece == RED:
                score -= 100

                # Advancement towards promotion
                score -= (7 - row) * 5

            elif piece == BLACK:
                score += 100
                score += row * 5

            elif piece == RED_KING:
                score -= 175

            elif piece == BLACK_KING:
                score += 175

            # Center control
            if piece != 0 and 2 <= col <= 5:

                score += 3 if piece > 0 else -3

    # Mobility
    from game.moves import get_valid_moves

    black_moves = len(
        get_valid_moves(board, BLACK)
    )

    red_moves = len(
        get_valid_moves(board, RED)
    )

    score += 2 * (black_moves - red_moves)

    return score * player
