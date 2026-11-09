from cards import Card, Suit, Rank
from observation import Observation
from round_history import RoundHistory


def test_observation_contains_correct_information():
    history = RoundHistory()

    played_card = Card(Suit.SPADES, Rank.NINE)
    history.record_card(1, played_card, Suit.HEARTS)

    observation = Observation(
        hand=(Card(Suit.CLUBS, Rank.ACE),),
        legal_cards=(Card(Suit.CLUBS, Rank.ACE),),
        current_trick=((1, played_card),),
        played_history=tuple(history.played_cards),
        void_suits=tuple(frozenset(s) for s in history.void_suits),
        player_index=3,
        trump_suit=Suit.HEARTS,
    )

    assert observation.player_index == 3
    assert observation.teammate_index == 1
    assert observation.trump_suit == Suit.HEARTS
    assert observation.is_void_in_suit(1, Suit.HEARTS)
    assert not observation.is_void_in_suit(1, Suit.CLUBS)


def test_observation_is_independent_of_game_history():
    history = RoundHistory()

    first_card = Card(Suit.SPADES, Rank.NINE)
    history.record_card(1, first_card, Suit.HEARTS)

    observation = Observation(
        hand=(),
        legal_cards=(),
        current_trick=((1, first_card),),
        played_history=tuple(history.played_cards),
        void_suits=tuple(frozenset(s) for s in history.void_suits),
        player_index=0,
        trump_suit=Suit.HEARTS,
    )

    second_card = Card(Suit.CLUBS, Rank.ACE)
    history.record_card(2, second_card, Suit.CLUBS)

    assert len(observation.played_history) == 1
    assert len(history.played_cards) == 2


def test_observation_is_immutable():
    import pytest
    from dataclasses import FrozenInstanceError

    observation = Observation(
        hand=(),
        legal_cards=(),
        current_trick=(),
        played_history=(),
        void_suits=(frozenset(),) * 4,
        player_index=0,
        trump_suit=Suit.HEARTS,
    )

    with pytest.raises(FrozenInstanceError):
        observation.player_index = 2
