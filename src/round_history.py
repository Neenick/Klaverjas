from cards import Card, Suit, create_deck


class RoundHistory:

    def __init__(self):
        # Cards played, stored together with the player index.
        self.played_cards: list[tuple[int, Card]] = []

        # Cards played by each individual player.
        self.played_cards_by_player: list[list[Card]] = [
            [] for _ in range(4)
        ]

        # Suits that each player no longer has.
        self.void_suits: list[set[Suit]] = [
            set() for _ in range(4)
        ]

    def record_card(
        self,
        player_index: int,
        card: Card,
        lead_suit: Suit,
    ):
        """Record a played card and update the player's known void suits."""

        if player_index not in range(4):
            raise ValueError("Player index must be between 0 and 3.")

        if any(played_card == card for _, played_card in self.played_cards):
            raise ValueError(f"Card has already been played: {card}")

        self.played_cards.append((player_index, card))
        self.played_cards_by_player[player_index].append(card)

        # Playing another suit means the player has no cards of the lead suit.
        if card.suit != lead_suit:
            self.void_suits[player_index].add(lead_suit)

    def get_cards_played_by(self, player_index: int) -> list[Card]:
        """Return all cards played by a specific player."""

        if player_index not in range(4):
            raise ValueError("Player index must be between 0 and 3.")

        return self.played_cards_by_player[player_index].copy()

    def is_void_in_suit(self, player_index: int, suit: Suit) -> bool:
        """Check whether a player is known to have no cards of a suit."""

        if player_index not in range(4):
            raise ValueError("Player index must be between 0 and 3.")

        return suit in self.void_suits[player_index]

    def get_unplayed_cards(self) -> list[Card]:
        """Return all cards that have not yet been played."""

        played = {card for _, card in self.played_cards}

        return [
            card for card in create_deck()
            if card not in played
        ]

    def get_unplayed_cards_in_suit(self, suit: Suit) -> list[Card]:
        """Return all unplayed cards of a specific suit."""

        return [
            card for card in self.get_unplayed_cards()
            if card.suit == suit
        ]
