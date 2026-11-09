
from enum import Enum

from cards import Card, Rank, Suit


class RuleVariant(Enum):
    AMSTERDAM = "amsterdam"
    ROTTERDAM = "rotterdam"


# Higher values indicate stronger cards.
TRUMP_STRENGTH = {
    Rank.JACK: 8,
    Rank.NINE: 7,
    Rank.ACE: 6,
    Rank.TEN: 5,
    Rank.KING: 4,
    Rank.QUEEN: 3,
    Rank.EIGHT: 2,
    Rank.SEVEN: 1,
}

NON_TRUMP_STRENGTH = {
    Rank.ACE: 8,
    Rank.TEN: 7,
    Rank.KING: 6,
    Rank.QUEEN: 5,
    Rank.JACK: 4,
    Rank.NINE: 3,
    Rank.EIGHT: 2,
    Rank.SEVEN: 1,
}


def get_card_strength(
    card: Card,
    lead_suit: Suit,
    trump_suit: Suit,
) -> tuple[int, int]:
    """Return the strength of a card within a trick."""

    if card.suit == trump_suit:
        return (2, TRUMP_STRENGTH[card.rank])

    if card.suit == lead_suit:
        return (1, NON_TRUMP_STRENGTH[card.rank])

    return (0, 0)


def get_trick_winner(
    played_cards: list[tuple[int, Card]],
    trump_suit: Suit,
) -> int:
    """Return the player index who currently wins the trick."""

    if not played_cards:
        raise ValueError("The trick must contain at least one card.")

    lead_suit = played_cards[0][1].suit

    return max(
        played_cards,
        key=lambda play: get_card_strength(
            play[1], lead_suit, trump_suit
        ),
    )[0]


def get_legal_cards(
    hand: list[Card],
    played_cards: list[tuple[int, Card]],
    player_index: int,
    trump_suit: Suit,
    variant: RuleVariant,
) -> list[Card]:
    """Return all cards the player is allowed to play."""

    if not played_cards:
        return hand.copy()

    lead_suit = played_cards[0][1].suit

    matching_suit = [
        card for card in hand if card.suit == lead_suit
    ]

    current_winner = get_trick_winner(played_cards, trump_suit)

    winning_card = next(
        card for player, card in played_cards
        if player == current_winner
    )

    # If trump was led, players must follow suit and overtrump if possible.
    if lead_suit == trump_suit:
        if not matching_suit:
            return hand.copy()

        higher_trumps = [
            card for card in matching_suit
            if TRUMP_STRENGTH[card.rank] >
            TRUMP_STRENGTH[winning_card.rank]
        ]

        return higher_trumps or matching_suit

    # Follow the requested suit when possible.
    if matching_suit:
        return matching_suit

    trump_cards = [
        card for card in hand if card.suit == trump_suit
    ]

    partner_winning = current_winner % 2 == player_index % 2

    # Amsterdam: players do not have to trump when their partner wins.
    if variant == RuleVariant.AMSTERDAM and partner_winning:

        # If the partner wins with a non-trump card, any card is allowed.
        if winning_card.suit != trump_suit:
            return hand.copy()

        # If the partner wins with a trump, undertrumping is restricted.
        higher_trumps = [
            card for card in trump_cards
            if TRUMP_STRENGTH[card.rank] >
            TRUMP_STRENGTH[winning_card.rank]
        ]

        other_cards = [
            card for card in hand if card.suit != trump_suit
        ]

        if other_cards or higher_trumps:
            return other_cards + higher_trumps

        # Undercutting is allowed when only lower trumps remain.
        return trump_cards

    # No trump available.
    if not trump_cards:
        return hand.copy()

    # No trump has been played yet: playing trump is mandatory.
    if winning_card.suit != trump_suit:
        return trump_cards

    # A trump has already been played: overtrump if possible.
    higher_trumps = [
        card for card in trump_cards
        if TRUMP_STRENGTH[card.rank] >
        TRUMP_STRENGTH[winning_card.rank]
    ]

    if higher_trumps:
        return higher_trumps

    # Otherwise, undercut only when no other suits remain.
    other_cards = [
        card for card in hand if card.suit != trump_suit
    ]

    if other_cards:
        return other_cards

    return trump_cards