
from .cards import Card, Suit, create_deck, shuffle_deck
from .rules import RuleVariant, get_legal_cards, get_trick_winner
from .scoring import get_trick_points


class Game:

    def __init__(
        self,
        agents,
        trump_suit: Suit,
        variant: RuleVariant = RuleVariant.AMSTERDAM,
        seed: int | None = None,
    ):
        if len(agents) != 4:
            raise ValueError("A Klaverjas game requires exactly 4 agents.")

        self.agents = agents
        self.trump_suit = trump_suit
        self.variant = variant
        self.seed = seed

        self.hands = []
        self.tricks = []
        self.scores = [0, 0]

    def deal_cards(self):
        """Shuffle and distribute 32 cards to four players."""

        deck = shuffle_deck(create_deck(), self.seed)

        self.hands = [
            deck[i * 8:(i + 1) * 8]
            for i in range(4)
        ]

    def play_trick(self, leader: int, trick_number: int):
        """Play one complete trick."""

        played_cards = []

        for offset in range(4):
            player_index = (leader + offset) % 4
            hand = self.hands[player_index]

            legal_cards = get_legal_cards(
                hand,
                played_cards,
                player_index,
                self.trump_suit,
                self.variant,
            )

            card = self.agents[player_index].select_card(
                hand.copy(),
                legal_cards.copy(),
                played_cards.copy(),
                player_index,
                self.trump_suit,
            )

            if card not in legal_cards:
                raise ValueError(
                    f"Player {player_index} played an illegal card: {card}"
                )

            hand.remove(card)
            played_cards.append((player_index, card))

        winner = get_trick_winner(played_cards, self.trump_suit)

        cards = [card for _, card in played_cards]

        points = get_trick_points(
            cards,
            self.trump_suit,
            is_last_trick=(trick_number == 7),
        )

        self.scores[winner % 2] += points

        self.tricks.append({
            "leader": leader,
            "played_cards": played_cards,
            "winner": winner,
            "points": points,
        })

        return winner

    def play(self):
        """Play a complete game of Klaverjas."""

        self.deal_cards()

        leader = 0

        for trick_number in range(8):
            leader = self.play_trick(leader, trick_number)

        return {
            "scores": self.scores.copy(),
            "winner": (
                0 if self.scores[0] > self.scores[1]
                else 1 if self.scores[1] > self.scores[0]
                else None
            ),
            "tricks": self.tricks.copy(),
        }
