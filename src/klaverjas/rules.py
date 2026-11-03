
from enum import Enum

from .cards import Card, Rank, Suit


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


def get_card_strength(card: Card, lead_suit: Suit, trump_suit: Suit) -> tuple[int, int]:
    """Return the strength of a card within a trick."""

    if card.suit == trump_suit:
        return (2, TRUMP_STRENGTH[card.rank])

    if card.suit == lead_suit:
        return (1, NON_TRUMP_STRENGTH[card.rank])

    return (0, 0)


def get_trick_winner(played_cards: list[tuple[int, Card]], trump_suit: Suit) -> int:
    """Return the player index who currently wins the trick."""

    if not played_cards:
        raise ValueError("The trick must contain at least one card.")

    lead_suit = played_cards[0][1].suit

    return max(played_cards, key=lambda play: get_card_strength(play[1], lead_suit, trump_suit))[0]




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

    matching_suit = [card for card in hand if card.suit == lead_suit]

    current_winner = get_trick_winner(played_cards, trump_suit)

    # If trump was led, players must follow suit and overtrump if possible.
    if matching_suit:
        if lead_suit == trump_suit:
            winning_card = next(
                card for player, card in played_cards
                if player == current_winner
            )

            higher_trumps = [
                card for card in matching_suit
                if TRUMP_STRENGTH[card.rank] >
                TRUMP_STRENGTH[winning_card.rank]
            ]

            if higher_trumps:
                return higher_trumps

        return matching_suit

    # The player cannot follow suit.
    partner_index = (player_index + 2) % 4

    # Amsterdam: discarding is allowed when your partner wins.
    if (variant == RuleVariant.AMSTERDAM and current_winner == partner_index):
        return hand.copy()

    trump_cards = [card for card in hand if card.suit == trump_suit]

    if not trump_cards:
        return hand.copy()

    winning_card = next(card for player, card in played_cards if player == current_winner)

    # Overtrump if the current winning card is a trump.
    if winning_card.suit == trump_suit:
        higher_trumps = [
            card for card in trump_cards
            if TRUMP_STRENGTH[card.rank] >
            TRUMP_STRENGTH[winning_card.rank]
        ]

        if higher_trumps:
            return higher_trumps

    return trump_cards
