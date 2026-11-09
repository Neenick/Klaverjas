from cards import Card, Suit, create_deck, shuffle_deck
from rules import RuleVariant, get_legal_cards
from trick import Trick


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

        self.hands: list[list[Card]] = []
        self.tricks: list[Trick] = []
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

        trick = Trick(leader)

        while not trick.is_complete():
            player_index = trick.to_play()
            hand = self.hands[player_index]

            legal_cards = get_legal_cards(
                hand,
                trick.played_cards,
                player_index,
                self.trump_suit,
                self.variant,
            )

            card = self.agents[player_index].select_card(
                hand.copy(),
                legal_cards.copy(),
                trick.played_cards,
                player_index,
                self.trump_suit,
            )

            if card not in legal_cards:
                raise ValueError(
                    f"Player {player_index} played an illegal card: {card}"
                )

            hand.remove(card)
            trick.add_card(card)

        winner = trick.winner(self.trump_suit)

        points = trick.points(
            self.trump_suit,
            is_last_trick=(trick_number == 7),
        )

        self.scores[winner % 2] += points
        self.tricks.append(trick)

        return winner

    def play(self):
        """Play a complete game of Klaverjas."""

        self.deal_cards()
        self.tricks = []
        self.scores = [0, 0]

        leader = 0

        for trick_number in range(8):
            leader = self.play_trick(leader, trick_number)

        trick_results = [
            {
                "leader": trick.starting_player,
                "played_cards": trick.played_cards,
                "winner": trick.winner(self.trump_suit),
                "points": trick.points(
                    self.trump_suit,
                    is_last_trick=(i == 7),
                ),
            }
            for i, trick in enumerate(self.tricks)
        ]

        return {
            "scores": self.scores.copy(),
            "winner": (
                0 if self.scores[0] > self.scores[1]
                else 1 if self.scores[1] > self.scores[0]
                else None
            ),
            "tricks": trick_results,
        }
