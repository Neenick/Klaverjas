
import csv

from agents.random_agent import RandomAgent
from cards import Suit
from evaluation.tournament import (
    run_tournament,
    save_results_csv,
)


def test_tournament_runs_complete_games():
    tournament = run_tournament(
        RandomAgent,
        RandomAgent,
        trump_suit=Suit.HEARTS,
        num_games=10,
        seed=42,
    )

    assert tournament.summary["games_played"] == 10
    assert len(tournament.records) == 10

    for record in tournament.records:
        assert (
            record["strategy_a_score"]
            + record["strategy_b_score"]
            == 162
        )


def test_tournament_alternates_teams():
    tournament = run_tournament(
        RandomAgent,
        RandomAgent,
        trump_suit=Suit.HEARTS,
        num_games=6,
        seed=42,
    )

    team_assignments = [
        record["strategy_a_team"]
        for record in tournament.records
    ]

    assert team_assignments == [0, 1, 0, 1, 0, 1]


def test_tournament_is_reproducible():
    first = run_tournament(
        RandomAgent,
        RandomAgent,
        trump_suit=Suit.HEARTS,
        num_games=10,
        seed=42,
    )

    second = run_tournament(
        RandomAgent,
        RandomAgent,
        trump_suit=Suit.HEARTS,
        num_games=10,
        seed=42,
    )

    assert first.records == second.records


def test_tournament_exports_csv(tmp_path):
    tournament = run_tournament(
        RandomAgent,
        RandomAgent,
        trump_suit=Suit.HEARTS,
        num_games=5,
        seed=42,
    )

    output_path = tmp_path / "results.csv"

    save_results_csv(tournament, output_path)

    assert output_path.exists()

    with output_path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert len(rows) == 5
    assert "strategy_a_score" in rows[0]
    assert "strategy_b_score" in rows[0]
