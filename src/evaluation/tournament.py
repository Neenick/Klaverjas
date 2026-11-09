import csv

from dataclasses import dataclass
from pathlib import Path
from collections.abc import Callable

from agents.base_agent import BaseAgent
from cards import Suit
from game import Game
from rules import RuleVariant


AgentFactory = Callable[[int], BaseAgent]


@dataclass
class TournamentResult:
    summary: dict
    records: list[dict]


def run_tournament(
    strategy_a_factory: AgentFactory,
    strategy_b_factory: AgentFactory,
    trump_suit: Suit,
    num_games: int = 100,
    variant: RuleVariant = RuleVariant.AMSTERDAM,
    seed: int = 42,
) -> TournamentResult:
    """
    Run a tournament between two strategies.

    Each strategy controls two players.
    Teams alternate positions to reduce seat bias.
    """

    if num_games < 1:
        raise ValueError("Number of games must be at least 1.")

    records = []

    for game_index in range(num_games):
        game_seed = seed + game_index

        # Alternate which team occupies seats 0 and 2.
        strategy_a_team = game_index % 2

        if strategy_a_team == 0:
            factories = [
                strategy_a_factory,
                strategy_b_factory,
                strategy_a_factory,
                strategy_b_factory,
            ]
        else:
            factories = [
                strategy_b_factory,
                strategy_a_factory,
                strategy_b_factory,
                strategy_a_factory,
            ]

        # Create fresh agents with independent seeds.
        agents = [
            factory(seed + game_index * 4 + seat + 1)
            for seat, factory in enumerate(factories)
        ]

        game = Game(
            agents=agents,
            trump_suit=trump_suit,
            variant=variant,
            seed=game_seed,
        )

        result = game.play()

        # Convert team scores to strategy scores.
        if strategy_a_team == 0:
            score_a = result["scores"][0]
            score_b = result["scores"][1]
        else:
            score_a = result["scores"][1]
            score_b = result["scores"][0]

        # Identify the winning strategy.
        if result["winner"] is None:
            winner = "draw"
        elif result["winner"] == strategy_a_team:
            winner = "A"
        else:
            winner = "B"

        records.append({
            "game": game_index + 1,
            "seed": game_seed,
            "trump_suit": trump_suit.value,
            "strategy_a_team": strategy_a_team,
            "strategy_a_score": score_a,
            "strategy_b_score": score_b,
            "point_difference": score_a - score_b,
            "winner": winner,
        })

    # Calculate tournament statistics.
    wins_a = sum(r["winner"] == "A" for r in records)
    wins_b = sum(r["winner"] == "B" for r in records)
    draws = sum(r["winner"] == "draw" for r in records)

    average_score_a = sum(
        r["strategy_a_score"] for r in records
    ) / num_games

    average_score_b = sum(
        r["strategy_b_score"] for r in records
    ) / num_games

    average_difference = sum(
        r["point_difference"] for r in records
    ) / num_games

    summary = {
        "games_played": num_games,
        "strategy_a_wins": wins_a,
        "strategy_b_wins": wins_b,
        "draws": draws,
        "strategy_a_win_rate": wins_a / num_games,
        "strategy_b_win_rate": wins_b / num_games,
        "draw_rate": draws / num_games,
        "average_strategy_a_points": average_score_a,
        "average_strategy_b_points": average_score_b,
        "average_point_difference": average_difference,
    }

    return TournamentResult(
        summary=summary,
        records=records,
    )


def save_results_csv(
    tournament: TournamentResult,
    file_path: str | Path,
):
    """Save individual game results to a CSV file."""

    if not tournament.records:
        raise ValueError("No tournament results to export.")

    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(tournament.records[0].keys())

    with file_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(tournament.records)
