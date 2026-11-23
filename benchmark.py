
import time
import matplotlib.pyplot as plt

from game.board import Board

from ai.minimax import get_best_move as minimax
from ai.alpha_beta import get_best_move as alpha_beta
from ai.greedy import get_best_move as greedy


ALGORITHMS = {
    "Minimax": minimax,
    "Alpha-Beta": alpha_beta,
    "Greedy": greedy
}


def benchmark(depth=4):

    game = Board()

    results = {}

    for name, algorithm in ALGORITHMS.items():

        # Each algorithm receives an independent copy.
        test_board = game.clone()

        move, stats = algorithm(
            test_board, depth
        )

        results[name] = {
            "time": stats["time"],
            "nodes": stats["nodes"],
            "score": stats["score"],
            "move": move
        }

        if "cutoffs" in stats:
            results[name]["cutoffs"] = stats["cutoffs"]

    print("\nALGORITHM COMPARISON\n")

    for name, data in results.items():

        print(f"\n{name}")

        print("Time:", round(data["time"], 6), "seconds")
        print("Nodes:", data["nodes"])
        print("Score:", data["score"])
        print("Move:", data["move"])

        if "cutoffs" in data:
            print("Cutoffs:", data["cutoffs"])

    return results


def plot_results(results):

    names = list(results.keys())

    times = [
        results[name]["time"]
        for name in names
    ]

    nodes = [
        results[name]["nodes"]
        for name in names
    ]

    plt.figure()

    plt.bar(names, times)

    plt.title("Algorithm Execution Time")
    plt.ylabel("Time (seconds)")

    plt.savefig("execution_time.png")
    plt.show()

    plt.figure()

    plt.bar(names, nodes)

    plt.title("Algorithm Node Exploration")
    plt.ylabel("Nodes explored")

    plt.savefig("explored_nodes.png")
    plt.show()


if __name__ == "__main__":

    results = benchmark(depth=4)

    plot_results(results)
