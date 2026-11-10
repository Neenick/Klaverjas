
from agents.base_agent import BaseAgent
from cards import Card, Suit, create_deck, shuffle_deck
from rules import RuleVariant, get_legal_cards
from trick import Trick
from round_history import RoundHistory
from observation import Observation


class Game:

    def __init__(
        self,
        agents: list[BaseAgent | None],
        trump_suit: Suit,
        variant: RuleVariant = RuleVariant.AMSTERDAM,
        seed: int | None = None,
    ):
        if len(agents) != 4:
            raise ValueError("A Klaverjas game requires exactly 4 agents.")

        human_seats = [
            index for index, agent in enumerate(agents)
            if agent is None
        ]

        if len(human_seats) > 1:
            raise ValueError("Only one human player is allowed.")

        if human_seats and human_seats[0] != 3:
            raise ValueError("The human player must be player 4.")

        self.agents = agents
        self.trump_suit = trump_suit
        self.variant = variant
        self.seed = seed

        self.hands: list[list[Card]] = []
        self.tricks: list[Trick] = []
        self.scores = [0, 0]

        self.history = RoundHistory()
        self.current_trick: Trick | None = None

        self.started = False
        self.finished = False

    def deal_cards(self):
        """Shuffle and distribute 32 cards to four players."""

        deck = shuffle_deck(create_deck(), self.seed)

        self.hands = [
            deck[i * 8:(i + 1) * 8]
            for i in range(4)
        ]

    def start(self):
        """Initialize a new game."""

        self.deal_cards()

        self.tricks = []
        self.scores = [0, 0]
        self.history = RoundHistory()

        self.current_trick = Trick(starting_player=0)

        self.started = True
        self.finished = False

    @property
    def current_player(self) -> int | None:
        """Return the current player index."""

        if not self.started or self.finished:
            return None

        return self.current_trick.to_play()

    def get_observation(self) -> Observation:
        """Create an observation for the current player."""

        if not self.started or self.finished:
            raise RuntimeError("There is no active turn.")

        player_index = self.current_player
        hand = self.hands[player_index]

        legal_cards = get_legal_cards(
            hand,
            self.current_trick.played_cards,
            player_index,
            self.trump_suit,
            self.variant,
        )

        return Observation(
            hand=tuple(hand),
            legal_cards=tuple(legal_cards),
            current_trick=tuple(self.current_trick.played_cards),
            played_history=tuple(self.history.played_cards),
            void_suits=tuple(
                frozenset(suits)
                for suits in self.history.void_suits
            ),
            player_index=player_index,
            trump_suit=self.trump_suit,
        )

    def play_card(self, card: Card):
        """Play one card for the current player."""

        observation = self.get_observation()

        player_index = observation.player_index

        if card not in observation.legal_cards:
            raise ValueError(
                f"Player {player_index} cannot play {card}."
            )

        lead_suit = self.current_trick.leading_suit() or card.suit

        self.hands[player_index].remove(card)

        self.history.record_card(
            player_index,
            card,
            lead_suit,
        )

        self.current_trick.add_card(card)

        # Resolve the trick when all four players have played.
        if self.current_trick.is_complete():
            winner = self.current_trick.winner(self.trump_suit)

            points = self.current_trick.points(
                self.trump_suit,
                is_last_trick=(len(self.tricks) == 7),
            )

            self.scores[winner % 2] += points
            self.tricks.append(self.current_trick)

            if len(self.tricks) == 8:
                self.finished = True
            else:
                self.current_trick = Trick(
                    starting_player=winner
                )

    def play_agent_turn(self) -> Card:
        """Let the current automated agent select and play a card."""

        player_index = self.current_player

        if player_index is None:
            raise RuntimeError("There is no active turn.")

        agent = self.agents[player_index]

        if agent is None:
            raise ValueError(
                f"Player {player_index} is a human player."
            )

        observation = self.get_observation()
        card = agent.select_card(observation)

        self.play_card(card)

        return card

    def get_result(self) -> dict:
        """Return the completed game results."""

        if not self.finished:
            raise RuntimeError("The game is not finished.")

        winner = (
            0 if self.scores[0] > self.scores[1]
            else 1 if self.scores[1] > self.scores[0]
            else None
        )

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
            "winner": winner,
            "tricks": trick_results,
        }

    def play(self) -> dict:
        """Play a complete game using automated agents only."""

        if any(agent is None for agent in self.agents):
            raise ValueError(
                "Game.play() requires four automated agents. "
                "Use start() and play_card() for human players."
            )

        self.start()

        while not self.finished:
            self.play_agent_turn()

        return self.get_result()
