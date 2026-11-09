
from cards import Suit
from game import Game
from rules import RuleVariant
from agents.random_agent import RandomAgent


def test_complete_game():
    agents = [RandomAgent() for _ in range(4)]

    game = Game(
        agents=agents,
        trump_suit=Suit.HEARTS,
        variant=RuleVariant.AMSTERDAM,
        seed=42,
    )

    result = game.play()

    assert len(result["tricks"]) == 8
    assert sum(result["scores"]) == 162
    assert all(len(hand) == 0 for hand in game.hands)


def test_every_trick_has_four_cards():
    agents = [RandomAgent() for _ in range(4)]
    game = Game(agents, Suit.SPADES, seed=42)

    result = game.play()

    for trick in result["tricks"]:
        assert len(trick["played_cards"]) == 4
