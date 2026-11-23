
import time

from game.moves import get_valid_moves
from game.rules import get_winner
from ai.evaluation import evaluate


def minimax(board, depth, maximizing, player, stats):

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

        best_score = float("-inf")

        for move in moves:

            new_board = board.clone()
            new_board.make_move(move)

            score, _ = minimax(
                new_board,
                depth - 1,
                False,
                player,
                stats
            )

            if score > best_score:
                best_score = score
                best_move = move

        return best_score, best_move

    else:

        best_score = float("inf")

        for move in moves:

            new_board = board.clone()
            new_board.make_move(move)

            score, _ = minimax(
                new_board,
                depth - 1,
                True,
                player,
                stats
            )

            if score < best_score:
                best_score = score
                best_move = move

        return best_score, best_move


def get_best_move(board, depth=4):

    stats = {"nodes": 0}

    start = time.perf_counter()

    score, move = minimax(
        board,
        depth,
        True,
        board.turn,
        stats
    )

    elapsed = time.perf_counter() - start

    stats["time"] = elapsed
    stats["score"] = score

    return move, stats
