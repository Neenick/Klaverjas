
from klaverjas.cards import Card, Suit, Rank
from klaverjas.rules import (RuleVariant, get_legal_cards, get_trick_winner)


def test_trump_jack_beats_trump_nine():
    played_cards = [
        (0, Card(Suit.HEARTS, Rank.NINE)),
        (1, Card(Suit.HEARTS, Rank.JACK)),
    ]

    winner = get_trick_winner(played_cards, Suit.HEARTS)

    assert winner == 1


def test_player_must_follow_suit():
    hand = [
        Card(Suit.HEARTS, Rank.ACE),
        Card(Suit.SPADES, Rank.JACK),
    ]

    played_cards = [(0, Card(Suit.HEARTS, Rank.SEVEN))]

    legal_cards = get_legal_cards(
        hand,
        played_cards,
        1,
        Suit.SPADES,
        RuleVariant.AMSTERDAM,
    )

    assert legal_cards == [Card(Suit.HEARTS, Rank.ACE)]


def test_rotterdam_requires_trumping():
    hand = [
        Card(Suit.SPADES, Rank.JACK),
        Card(Suit.CLUBS, Rank.ACE),
    ]

    played_cards = [(0, Card(Suit.HEARTS, Rank.SEVEN))]

    legal_cards = get_legal_cards(
        hand,
        played_cards,
        1,
        Suit.SPADES,
        RuleVariant.ROTTERDAM,
    )

    assert legal_cards == [Card(Suit.SPADES, Rank.JACK)]


def test_player_must_overtrump():
    hand = [
        Card(Suit.SPADES, Rank.JACK),
        Card(Suit.SPADES, Rank.SEVEN),
        Card(Suit.CLUBS, Rank.ACE),
    ]

    played_cards = [
        (0, Card(Suit.HEARTS, Rank.SEVEN)),
        (2, Card(Suit.SPADES, Rank.NINE)),
    ]

    legal_cards = get_legal_cards(
        hand, played_cards, 1,
        Suit.SPADES, RuleVariant.ROTTERDAM
    )

    assert legal_cards == [
        Card(Suit.SPADES, Rank.JACK)
    ]


def test_amsterdam_can_discard_when_partner_wins():
    hand = [
        Card(Suit.SPADES, Rank.SEVEN),
        Card(Suit.CLUBS, Rank.ACE),
    ]

    played_cards = [
        (2, Card(Suit.HEARTS, Rank.SEVEN)),
    ]

    legal_cards = get_legal_cards(
        hand, played_cards, 0,
        Suit.SPADES, RuleVariant.AMSTERDAM
    )

    assert legal_cards == hand



def test_must_discard_instead_of_undercutting():
    hand = [
        Card(Suit.SPADES, Rank.SEVEN),
        Card(Suit.CLUBS, Rank.ACE),
    ]

    played_cards = [
        (0, Card(Suit.HEARTS, Rank.SEVEN)),
        (2, Card(Suit.SPADES, Rank.JACK)),
    ]

    legal_cards = get_legal_cards(
        hand, played_cards, 1,
        Suit.SPADES, RuleVariant.ROTTERDAM
    )

    assert legal_cards == [
        Card(Suit.CLUBS, Rank.ACE)
    ]


def test_undercutting_allowed_when_only_trumps_remain():
    hand = [
        Card(Suit.SPADES, Rank.SEVEN),
    ]

    played_cards = [
        (0, Card(Suit.HEARTS, Rank.SEVEN)),
        (2, Card(Suit.SPADES, Rank.JACK)),
    ]

    legal_cards = get_legal_cards(
        hand, played_cards, 1,
        Suit.SPADES, RuleVariant.ROTTERDAM
    )

    assert legal_cards == hand


def test_must_play_trump_when_trump_is_led():
    hand = [
        Card(Suit.SPADES, Rank.SEVEN),
        Card(Suit.CLUBS, Rank.ACE),
    ]

    played_cards = [
        (0, Card(Suit.SPADES, Rank.JACK)),
    ]

    legal_cards = get_legal_cards(
        hand, played_cards, 1,
        Suit.SPADES, RuleVariant.ROTTERDAM
    )

    assert legal_cards == [
        Card(Suit.SPADES, Rank.SEVEN)
    ]


def test_rotterdam_must_trump_when_partner_wins():
    hand = [
        Card(Suit.SPADES, Rank.JACK),
        Card(Suit.CLUBS, Rank.ACE),
    ]

    played_cards = [
        (3, Card(Suit.HEARTS, Rank.ACE)),
    ]

    legal_cards = get_legal_cards(
        hand, played_cards, 0,
        Suit.SPADES, RuleVariant.ROTTERDAM
    )

    assert legal_cards == [
        Card(Suit.SPADES, Rank.JACK)
    ]
