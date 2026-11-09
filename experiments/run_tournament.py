
from agents.random_agent import RandomAgent
from cards import Suit
from evaluation.tournament import run_tournament, save_results_csv


def main():
    tournament = run_tournament(
        strategy_a_factory=RandomAgent,
        strategy_b_factory=RandomAgent,
        trump_suit=Suit.HEARTS,
        num_games=1000,
        seed=7,
    )

    print("\nTournament Results")
    print("------------------")

    for metric, value in tournament.summary.items():
        print(f"{metric}: {value}")

    save_results_csv(
        tournament,
        "results/random_vs_random.csv",
    )

    print("\nResults saved to results/random_vs_random.csv")


if __name__ == "__main__":
    main()
