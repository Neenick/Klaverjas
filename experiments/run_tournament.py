from agents.random_agent import RandomAgent
from agents.rule_based_agent import RuleBasedAgent
from cards import Suit
from evaluation.tournament import run_tournament, save_results_csv


def main():
    tournament = run_tournament(
        strategy_a_factory=RuleBasedAgent,
        strategy_b_factory=RandomAgent,
        trump_suit=Suit.HEARTS,
        num_games=1000,
        seed=42,
    )

    print("\nRule-based vs Random")
    print("--------------------")

    for metric, value in tournament.summary.items():
        print(f"{metric}: {value}")

    save_results_csv(
        tournament,
        "results/rule_based_vs_random.csv",
    )


if __name__ == "__main__":
    main()
