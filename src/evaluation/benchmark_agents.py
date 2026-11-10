
import csv
from pathlib import Path

from agents.random_agent import RandomAgent
from agents.rule_based_agent import RuleBasedAgent
from cards import Suit
from evaluation.benchmark import benchmark_agent


def main():
    num_games = 10000

    agents = [
        ("Random", RandomAgent),
        ("Rule-based", RuleBasedAgent),
    ]

    results = []

    for name, agent_factory in agents:
        print(f"\nBenchmarking {name}...")

        result = benchmark_agent(
            agent_factory=agent_factory,
            trump_suit=Suit.HEARTS,
            num_games=num_games,
            warmup_games=10,
            seed=42,
        )

        result["agent"] = name
        results.append(result)

        print(f"Average decision time: "
              f"{result['average_decision_time_us']:.2f} us")

        print(f"Median decision time: "
              f"{result['median_decision_time_us']:.2f} us")

        print(f"P95 decision time: "
              f"{result['p95_decision_time_us']:.2f} us")

        print(f"Games per second: "
              f"{result['games_per_second']:.2f}")

    random_time = results[0]["average_decision_time_us"]
    rule_time = results[1]["average_decision_time_us"]

    ratio = rule_time / random_time

    print("\nComputational comparison")
    print("------------------------")
    print(f"Rule-based / Random: {ratio:.2f}x")

    # Export benchmark results.
    output_path = Path("results/computational_benchmark.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys(),
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
