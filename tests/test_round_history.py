import pytest

from cards import Card, Suit, Rank
from round_history import RoundHistory


def test_record_played_card():
    history = RoundHistory()
    card = Card(Suit.HEARTS, Rank.ACE)

    history.record_card(0, card, Suit.HEARTS)

    assert history.played_cards == [(0, card)]
    assert history.get_cards_played_by(0) == [card]


def test_player_becomes_void_in_suit():
    history = RoundHistory()
    card = Card(Suit.SPADES, Rank.JACK)

    history.record_card(1, card, Suit.HEARTS)

    assert history.is_void_in_suit(1, Suit.HEARTS)


def test_following_suit_does_not_mark_player_void():
    history = RoundHistory()
    card = Card(Suit.HEARTS, Rank.ACE)

    history.record_card(0, card, Suit.HEARTS)

    assert not history.is_void_in_suit(0, Suit.HEARTS)


def test_get_unplayed_cards():
    history = RoundHistory()

    card = Card(Suit.HEARTS, Rank.ACE)
    history.record_card(0, card, Suit.HEARTS)

    unplayed = history.get_unplayed_cards()

    assert len(unplayed) == 31
    assert card not in unplayed


def test_get_unplayed_cards_in_suit():
    history = RoundHistory()

    card = Card(Suit.HEARTS, Rank.ACE)
    history.record_card(0, card, Suit.HEARTS)

    remaining = history.get_unplayed_cards_in_suit(Suit.HEARTS)

    assert len(remaining) == 7
    assert all(card.suit == Suit.HEARTS for card in remaining)


def test_cannot_record_same_card_twice():
    history = RoundHistory()
    card = Card(Suit.HEARTS, Rank.ACE)

    history.record_card(0, card, Suit.HEARTS)

    with pytest.raises(ValueError):
        history.record_card(1, card, Suit.HEARTS)


def test_invalid_player_index():
    history = RoundHistory()
    card = Card(Suit.HEARTS, Rank.ACE)

    with pytest.raises(ValueError):
        history.record_card(4, card, Suit.HEARTS)
