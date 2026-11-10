
from math import ceil
from statistics import fmean, median
from time import perf_counter_ns
from collections.abc import Callable

from agents.base_agent import BaseAgent
from cards import Suit
from game import Game
from rules import RuleVariant
from observation import Observation


AgentFactory = Callable[[int], BaseAgent]


class TimedAgent(BaseAgent):
    """Wrap an agent and measure its decision time."""

    def __init__(self, agent: BaseAgent):
        self.agent = agent
        self.decision_times_ns = []

    def select_card(self, observation: Observation):
        start = perf_counter_ns()

        try:
            return self.agent.select_card(observation)
        finally:
            self.decision_times_ns.append(
                perf_counter_ns() - start
            )


def benchmark_agent(
    agent_factory: AgentFactory,
    trump_suit: Suit,
    num_games: int = 100,
    warmup_games: int = 5,
    variant: RuleVariant = RuleVariant.AMSTERDAM,
    seed: int = 42,
) -> dict:
    """Measure the computational performance of an agent."""

    if num_games < 1:
        raise ValueError("Number of games must be at least 1.")

    if warmup_games < 0:
        raise ValueError("Warmup games cannot be negative.")

    def play_game(game_index: int) -> list[int]:
        timed_agents = [
            TimedAgent(
                agent_factory(seed + game_index * 4 + seat + 1)
            )
            for seat in range(4)
        ]

        game = Game(
            agents=timed_agents,
            trump_suit=trump_suit,
            variant=variant,
            seed=seed + game_index,
        )

        game.play()

        return [
            decision_time
            for agent in timed_agents
            for decision_time in agent.decision_times_ns
        ]

    # Warm up Python and the agent before measuring.
    for i in range(warmup_games):
        play_game(num_games + i)

    decision_times = []

    start = perf_counter_ns()

    for game_index in range(num_games):
        decision_times.extend(play_game(game_index))

    wall_time_ns = perf_counter_ns() - start

    total_decision_time_ns = sum(decision_times)
    average_ns = fmean(decision_times)
    sorted_times = sorted(decision_times)

    p95_index = min(
        len(sorted_times) - 1,
        ceil(0.95 * len(sorted_times)) - 1,
    )

    wall_time_seconds = wall_time_ns / 1_000_000_000

    return {
        "agent": agent_factory.__name__,
        "games": num_games,
        "decisions": len(decision_times),
        "total_decision_time_ms": total_decision_time_ns / 1_000_000,
        "average_decision_time_us": average_ns / 1_000,
        "median_decision_time_us": median(decision_times) / 1_000,
        "p95_decision_time_us": sorted_times[p95_index] / 1_000,
        "agent_decisions_per_second": 1_000_000_000 / average_ns,
        "wall_time_seconds": wall_time_seconds,
        "games_per_second": num_games / wall_time_seconds,
        "decision_time_share": total_decision_time_ns / wall_time_ns,
    }
