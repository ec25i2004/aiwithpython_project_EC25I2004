
import heapq
import itertools
import time

from game.moves import get_valid_moves
from game.rules import get_winner
from ai.evaluation import evaluate


def greedy_search(board, depth=4):

    stats = {"nodes": 0}

    player = board.turn

    counter = itertools.count()

    # Priority queue: (priority, sequence, state, first_move, depth)
    queue = []

    heapq.heappush(
        queue,
        (
            -evaluate(board.board, player),
            next(counter),
            board.clone(),
            None,
            0
        )
    )

    best_move = None
    best_score = float("-inf")

    while queue:

        _, _, current, first_move, level = heapq.heappop(queue)

        stats["nodes"] += 1

        winner = get_winner(current.board, current.turn)

        if winner is not None or level == depth:

            if winner == player:
                score = 100000 + (depth - level)

            elif winner == -player:
                score = -100000 - (depth - level)

            elif winner is not None:
                score = 0

            else:
                score = evaluate(current.board, player)

            if first_move is not None and score > best_score:
                best_score = score
                best_move = first_move

            continue

        moves = get_valid_moves(
            current.board,
            current.turn
        )

        for move in moves:

            new_board = current.clone()
            new_board.make_move(move)

            root_move = (
                move if first_move is None else first_move
            )

            heuristic = evaluate(
                new_board.board,
                player
            )

            heapq.heappush(
                queue,
                (
                    -heuristic,
                    next(counter),
                    new_board,
                    root_move,
                    level + 1
                )
            )

    return best_move, {
        **stats,
        "score": best_score
    }


def get_best_move(board, depth=4):

    start = time.perf_counter()

    move, stats = greedy_search(board, depth)

    stats["time"] = time.perf_counter() - start

    return move, stats
