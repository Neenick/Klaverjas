
import pytest

from cards import Card, Suit, Rank
from trick import Trick


def test_trick_initialization():
    trick = Trick(starting_player=2)

    assert trick.cards == []
    assert trick.to_play() == 2
    assert not trick.is_complete()


def test_players_play_in_correct_order():
    trick = Trick(starting_player=2)

    trick.add_card(Card(Suit.HEARTS, Rank.SEVEN))
    assert trick.to_play() == 3

    trick.add_card(Card(Suit.HEARTS, Rank.ACE))
    assert trick.to_play() == 0

    assert trick.played_cards[0][0] == 2
    assert trick.played_cards[1][0] == 3


def test_trick_completion():
    trick = Trick(starting_player=0)

    for _ in range(4):
        trick.add_card(Card(Suit.HEARTS, Rank.SEVEN))

    assert trick.is_complete()


def test_cannot_add_fifth_card():
    trick = Trick(starting_player=0)

    for _ in range(4):
        trick.add_card(Card(Suit.HEARTS, Rank.SEVEN))

    with pytest.raises(ValueError):
        trick.add_card(Card(Suit.SPADES, Rank.ACE))


def test_trick_winner_and_points():
    trick = Trick(starting_player=0)

    trick.add_card(Card(Suit.HEARTS, Rank.SEVEN))
    trick.add_card(Card(Suit.HEARTS, Rank.ACE))
    trick.add_card(Card(Suit.SPADES, Rank.JACK))
    trick.add_card(Card(Suit.HEARTS, Rank.TEN))

    assert trick.winner(Suit.SPADES) == 2
    assert trick.points(Suit.SPADES) == 41
