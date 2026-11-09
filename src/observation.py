from dataclasses import dataclass

from cards import Card, Suit


@dataclass(frozen=True)
class Observation:
    """Information available to an agent at a given turn."""

    hand: tuple[Card, ...]
    legal_cards: tuple[Card, ...]
    current_trick: tuple[tuple[int, Card], ...]
    played_history: tuple[tuple[int, Card], ...]
    void_suits: tuple[frozenset[Suit], ...]
    player_index: int
    trump_suit: Suit

    @property
    def teammate_index(self) -> int:
        """Return the index of the agent's teammate."""

        return (self.player_index + 2) % 4

    def is_void_in_suit(self, player_index: int, suit: Suit) -> bool:
        """Check whether a player is known to have no cards of a suit."""

        return suit in self.void_suits[player_index]
