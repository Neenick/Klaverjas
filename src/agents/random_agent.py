import random

from agents.base_agent import BaseAgent
from cards import Card, Suit


class RandomAgent(BaseAgent):

    def select_card(
        self,
        hand: list[Card],
        legal_cards: list[Card],
        played_cards: list[tuple[int, Card]],
        player_index: int,
        trump_suit: Suit,
        ) -> Card:
        
        return random.choice(legal_cards)
