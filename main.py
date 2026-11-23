
import copy
import queue
import threading
import sys

import pygame

from config import *
from game.board import Board
from interface.renderer import Renderer

from ai.minimax import get_best_move as minimax_move
from ai.alpha_beta import get_best_move as alpha_beta_move
from ai.greedy import get_best_move as greedy_move


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT + 110))
pygame.display.set_caption("Checkers AI")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 17)

game = Board()
renderer = Renderer(screen)

algorithm = "alpha"

ai_functions = {
    "minimax": minimax_move,
    "alpha": alpha_beta_move,
    "greedy": greedy_move,
}

selected = None
legal_moves = []
ai_stats = {}
ai_error = None

game_over = False
winner = None
running = True

ai_results = queue.Queue()
ai_thinking = False
game_generation = 0


def reset_game():
    global game, selected, legal_moves, ai_stats
    global ai_error, game_over, winner
    global ai_thinking, game_generation

    game_generation += 1

    game = Board()
    selected = None
    legal_moves = []
    ai_stats = {}
    ai_error = None

    game_over = False
    winner = None
    ai_thinking = False

    while True:
        try:
            ai_results.get_nowait()
        except queue.Empty:
            break


def run_ai_search(board_snapshot, search_function, depth, generation):
    try:
        move, stats = search_function(board_snapshot, depth)
        ai_results.put((generation, move, stats or {}, None))
    except Exception as exc:
        ai_results.put((generation, None, {}, exc))


def start_ai_search():
    global ai_thinking, ai_error

    if ai_thinking or game_over or game.turn != BLACK:
        return

    board_snapshot = copy.deepcopy(game)
    search_function = ai_functions[algorithm]
    generation = game_generation

    ai_thinking = True
    ai_error = None

    worker = threading.Thread(
        target=run_ai_search,
        args=(
            board_snapshot,
            search_function,
            SEARCH_DEPTH,
            generation,
        ),
        daemon=True,
    )

    worker.start()


def process_ai_results():
    global ai_thinking, ai_stats, ai_error

    while True:
        try:
            generation, move, stats, error = ai_results.get_nowait()
        except queue.Empty:
            break

        if generation != game_generation:
            continue

        ai_thinking = False

        if error is not None:
            ai_error = f"AI Error: {type(error).__name__}: {error}"
            print(ai_error)
            continue

        ai_stats = stats

        if game_over or game.turn != BLACK:
            continue

        if move is None:
            current_winner = game.winner()

            if current_winner is None:
                ai_error = (
                    "AI returned no move, but the game engine "
                    "reports no winner. Check terminal-state handling."
                )
                print(ai_error)

            continue

        current_legal_moves = game.get_all_moves()

        if move not in current_legal_moves:
            ai_error = "AI returned an illegal move."
            print(ai_error)
            continue

        game.make_move(move)


def draw_text(text, x, y, color=WHITE, target_font=None):
    target_font = target_font or font
    rendered = target_font.render(str(text), True, color)
    screen.blit(rendered, (x, y))


def draw():
    screen.fill((30, 30, 30))

    targets = [
        move.end
        for move in legal_moves
        if selected is not None and move.start == selected
    ]

    renderer.draw_board(game.board, selected, targets)

    if game_over:
        status = "You won!" if winner == RED else "AI won!"
        status_color = GREEN if winner == RED else GOLD
    elif ai_error:
        status = "AI paused - press R to restart"
        status_color = (255, 100, 100)
    elif ai_thinking:
        status = f"AI thinking ({algorithm.upper()})..."
        status_color = GOLD
    else:
        status = "Your turn"
        status_color = WHITE

    draw_text(status, 10, HEIGHT + 8, status_color)

    draw_text(
        f"AI: {algorithm.upper()} | "
        f"Depth: {SEARCH_DEPTH} | "
        f"Nodes: {ai_stats.get('nodes', 0)}",
        10,
        HEIGHT + 43,
        GOLD,
        small_font,
    )

    draw_text(
        "1: Minimax   2: Alpha-Beta   "
        "3: Greedy   R: Restart   Esc: Quit",
        10,
        HEIGHT + 75,
        WHITE,
        small_font,
    )

    pygame.display.flip()


while running:
    clock.tick(60)

    process_ai_results()

    if not game_over:
        winner = game.winner()

        if winner is not None:
            game_over = True
            selected = None
            legal_moves = []

    if (
        not game_over
        and not ai_thinking
        and not ai_error
        and game.turn == BLACK
    ):
        start_ai_search()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_r:
                reset_game()

            elif event.key == pygame.K_1:
                algorithm = "minimax"

            elif event.key == pygame.K_2:
                algorithm = "alpha"

            elif event.key == pygame.K_3:
                algorithm = "greedy"

        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and not game_over
            and not ai_thinking
            and not ai_error
            and game.turn == RED
        ):

            x, y = pygame.mouse.get_pos()

            if y >= HEIGHT or x >= WIDTH:
                continue

            row = y // SQUARE_SIZE
            col = x // SQUARE_SIZE
            clicked = (row, col)

            if selected is None:

                legal_moves = game.get_all_moves()

                matching = [
                    move for move in legal_moves
                    if move.start == clicked
                ]

                if matching:
                    selected = clicked

            else:

                matching = [
                    move for move in legal_moves
                    if move.start == selected
                    and move.end == clicked
                ]

                if matching:
                    game.make_move(matching[0])
                    selected = None
                    legal_moves = []

                else:
                    legal_moves = game.get_all_moves()

                    matching = [
                        move for move in legal_moves
                        if move.start == clicked
                    ]

                    selected = clicked if matching else None

    draw()


pygame.quit()
sys.exit()
