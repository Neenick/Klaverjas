from .cards import Card, Rank, Suit


TRUMP_POINTS = {
    Rank.JACK: 20,
    Rank.NINE: 14,
    Rank.ACE: 11,
    Rank.TEN: 10,
    Rank.KING: 4,
    Rank.QUEEN: 3,
    Rank.EIGHT: 0,
    Rank.SEVEN: 0,
}

NON_TRUMP_POINTS = {
    Rank.ACE: 11,
    Rank.TEN: 10,
    Rank.KING: 4,
    Rank.QUEEN: 3,
    Rank.JACK: 2,
    Rank.NINE: 0,
    Rank.EIGHT: 0,
    Rank.SEVEN: 0,
}


def get_card_points(card: Card, trump_suit: Suit) -> int:
    """Return the point value of a card."""
    if card.suit == trump_suit:
        return TRUMP_POINTS[card.rank]

    return NON_TRUMP_POINTS[card.rank]


def get_trick_points(
    cards: list[Card],
    trump_suit: Suit,
    is_last_trick: bool = False,
    ) -> int:
    """Calculate the points won in a trick."""

    points = sum(get_card_points(card, trump_suit) for card in cards)

    if is_last_trick:
        points += 10

    return points
