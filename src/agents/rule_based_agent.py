from agents.base_agent import BaseAgent
from cards import Card, Suit, create_deck
from observation import Observation
from rules import get_card_strength, get_trick_winner
from scoring import get_card_points


ALL_CARDS = tuple(create_deck())


class RuleBasedAgent(BaseAgent):

    def __init__(self, seed: int | None = None):
        self.seed = seed

    def select_card(self, observation: Observation) -> Card:
        """Select a card using a simple rule-based strategy."""

        if not observation.legal_cards:
            raise ValueError("No legal cards available.")

        if not observation.current_trick:
            return self._choose_lead_card(observation)

        return self._choose_follow_card(observation)

    def _choose_lead_card(self, observation: Observation) -> Card:
        """Lead a strong remaining card, otherwise a cheap card."""

        trump_suit = observation.trump_suit

        # Prefer non-trump cards when leading.
        non_trumps = [
            card for card in observation.legal_cards
            if card.suit != trump_suit
        ]

        candidates = non_trumps or list(observation.legal_cards)

        played_cards = {
            card for _, card in observation.played_history
        }

        # Find the strongest unplayed card in each suit.
        strongest_remaining = {}

        for suit in Suit:
            remaining = [
                card for card in ALL_CARDS
                if card.suit == suit and card not in played_cards
            ]

            if remaining:
                strongest_remaining[suit] = max(
                    remaining,
                    key=lambda card: get_card_strength(
                        card, suit, trump_suit
                    ),
                )

        # Prefer cards that are currently the strongest remaining in their suit.
        master_cards = [
            card for card in candidates
            if strongest_remaining.get(card.suit) == card
        ]

        if master_cards:
            return max(
                master_cards,
                key=lambda card: get_card_points(card, trump_suit),
            )

        # No master card available: preserve high-value cards.
        return min(
            candidates,
            key=lambda card: (
                get_card_points(card, trump_suit),
                get_card_strength(
                    card, card.suit, trump_suit
                ),
            ),
        )

    def _choose_follow_card(self, observation: Observation) -> Card:
        """Choose whether to win, support a teammate or discard."""

        played_cards = list(observation.current_trick)
        trump_suit = observation.trump_suit
        player_index = observation.player_index

        lead_suit = played_cards[0][1].suit
        current_winner = get_trick_winner(
            played_cards, trump_suit
        )

        winning_card = next(
            card for player, card in played_cards
            if player == current_winner
        )

        partner_winning = (
            current_winner % 2 == player_index % 2
        )

        # If our partner wins, avoid wasting strong cards.
        if partner_winning:
            return self._cheapest_card(
                observation.legal_cards,
                lead_suit,
                trump_suit,
            )

        winning_strength = get_card_strength(
            winning_card, lead_suit, trump_suit
        )

        # Find cards that can take over the trick.
        winning_cards = [
            card for card in observation.legal_cards
            if get_card_strength(
                card, lead_suit, trump_suit
            ) > winning_strength
        ]

        if winning_cards:
            # Win using the cheapest possible card.
            return self._cheapest_card(
                winning_cards,
                lead_suit,
                trump_suit,
            )

        # Cannot win: avoid giving away unnecessary points.
        return self._cheapest_card(
            observation.legal_cards,
            lead_suit,
            trump_suit,
        )

    @staticmethod
    def _cheapest_card(
        cards: tuple[Card, ...] | list[Card],
        lead_suit: Suit,
        trump_suit: Suit,
    ) -> Card:
        """Return the card with the lowest point value and strength."""

        return min(
            cards,
            key=lambda card: (
                get_card_points(card, trump_suit),
                get_card_strength(card, lead_suit, trump_suit),
            ),
        )
