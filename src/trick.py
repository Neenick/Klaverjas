from cards import Card, Suit
from rules import get_trick_winner
from scoring import get_trick_points


class Trick:

    def __init__(self, starting_player: int):
        if starting_player not in range(4):
            raise ValueError("Starting player must be between 0 and 3.")

        self.starting_player = starting_player
        self.cards: list[Card] = []

    @property
    def played_cards(self) -> list[tuple[int, Card]]:
        """Return played cards together with their player indices."""

        return [
            ((self.starting_player + i) % 4, card)
            for i, card in enumerate(self.cards)
        ]

    def add_card(self, card: Card):
        """Add a card to the trick."""

        if self.is_complete():
            raise ValueError("This trick is already complete.")

        self.cards.append(card)

    def is_complete(self) -> bool:
        return len(self.cards) == 4

    def leading_suit(self) -> Suit | None:
        if not self.cards:
            return None

        return self.cards[0].suit

    def to_play(self) -> int:
        """Return the player whose turn it is."""

        return (self.starting_player + len(self.cards)) % 4

    def winner(self, trump_suit: Suit) -> int:
        """Return the player who wins the trick."""

        return get_trick_winner(self.played_cards, trump_suit)

    def points(self, trump_suit: Suit, is_last_trick: bool = False) -> int:
        """Return the points collected in this trick."""

        return get_trick_points(self.cards, trump_suit, is_last_trick)
