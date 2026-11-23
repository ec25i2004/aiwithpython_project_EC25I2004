
import time

from game.moves import get_valid_moves
from game.rules import get_winner
from ai.evaluation import evaluate


def alpha_beta(
    board,
    depth,
    alpha,
    beta,
    maximizing,
    player,
    stats
):

    stats["nodes"] += 1

    winner = get_winner(board, board.turn)

    if depth == 0 or winner is not None:

        if winner == player:
            return 100000 + depth, None

        if winner == -player:
            return -100000 - depth, None

        if winner is not None:
            return 0, None

        return evaluate(board.board, player), None

    moves = get_valid_moves(
        board.board,
        board.turn
    )

    if not moves:
        return (
            -100000 if maximizing else 100000,
            None
        )

    best_move = None

    if maximizing:

        max_eval = float("-inf")

        for move in moves:

            new_board = board.clone()
            new_board.make_move(move)

            score, _ = alpha_beta(
                new_board,
                depth - 1,
                alpha,
                beta,
                False,
                player,
                stats
            )

            if score > max_eval:
                max_eval = score
                best_move = move

            alpha = max(alpha, max_eval)

            if beta <= alpha:
                stats["cutoffs"] += 1
                break

        return max_eval, best_move

    else:

        min_eval = float("inf")

        for move in moves:

            new_board = board.clone()
            new_board.make_move(move)

            score, _ = alpha_beta(
                new_board,
                depth - 1,
                alpha,
                beta,
                True,
                player,
                stats
            )

            if score < min_eval:
                min_eval = score
                best_move = move

            beta = min(beta, min_eval)

            if beta <= alpha:
                stats["cutoffs"] += 1
                break

        return min_eval, best_move


def get_best_move(board, depth=4):

    stats = {
        "nodes": 0,
        "cutoffs": 0
    }

    start = time.perf_counter()

    score, move = alpha_beta(
        board,
        depth,
        float("-inf"),
        float("inf"),
        True,
        board.turn,
        stats
    )

    elapsed = time.perf_counter() - start

    stats["time"] = elapsed
    stats["score"] = score

    return move, stats
