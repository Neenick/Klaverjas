
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

def test_game_tracks_all_played_cards():
    agents = [RandomAgent() for _ in range(4)]
    game = Game(agents, Suit.HEARTS, seed=42)

    game.play()

    assert len(game.history.played_cards) == 32

    for player_index in range(4):
        assert len(
            game.history.get_cards_played_by(player_index)
        ) == 8


def test_multiple_random_games_are_valid():
    for seed in range(25):
        agents = [RandomAgent() for _ in range(4)]
        game = Game(agents, Suit.HEARTS, seed=seed)

        result = game.play()

        # Every game must contain eight complete tricks.
        assert len(result["tricks"]) == 8

        # Every player must have played eight cards.
        assert all(len(hand) == 0 for hand in game.hands)

        # All 32 cards must have been played exactly once.
        played_cards = [
            card
            for trick in result["tricks"]
            for _, card in trick["played_cards"]
        ]

        assert len(played_cards) == 32
        assert len(set(played_cards)) == 32

        # Total points must always equal 162.
        assert sum(result["scores"]) == 162

        # History must contain all played cards.
        assert len(game.history.played_cards) == 32
