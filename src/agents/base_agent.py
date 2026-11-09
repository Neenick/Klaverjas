from abc import ABC, abstractmethod

from cards import Card, Suit


class BaseAgent(ABC):

    @abstractmethod
    def select_card(
        self,
        hand: list[Card],
        legal_cards: list[Card],
        played_cards: list[tuple[int, Card]],
        player_index: int,
        trump_suit: Suit,
    ) -> Card:
        """Select a card to play."""
        pass
