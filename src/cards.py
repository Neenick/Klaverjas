
from dataclasses import dataclass
from enum import Enum
import random


class Suit(Enum):
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"


class Rank(Enum):
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank

    def __str__(self) -> str:
        return f"{self.rank.name} of {self.suit.value}"


def create_deck() -> list[Card]:
    return [Card(suit, rank) for suit in Suit for rank in Rank]


def shuffle_deck(deck: list[Card], seed: int | None = None) -> list[Card]: 
    shuffled_deck = deck.copy()

    rng = random.Random(seed)
    rng.shuffle(shuffled_deck)

    return shuffled_deck
