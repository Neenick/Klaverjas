
from cards import Card, Suit, Rank
from observation import Observation
from agents.rule_based_agent import RuleBasedAgent


def create_observation(
    hand,
    legal_cards,
    current_trick=(),
    played_history=(),
    player_index=0,
    trump_suit=Suit.SPADES,
):
    return Observation(
        hand=tuple(hand),
        legal_cards=tuple(legal_cards),
        current_trick=tuple(current_trick),
        played_history=tuple(played_history),
        void_suits=(frozenset(),) * 4,
        player_index=player_index,
        trump_suit=trump_suit,
    )


def test_leads_master_card():
    agent = RuleBasedAgent()

    ace = Card(Suit.HEARTS, Rank.ACE)
    seven = Card(Suit.HEARTS, Rank.SEVEN)
    trump_jack = Card(Suit.SPADES, Rank.JACK)

    observation = create_observation(
        hand=[ace, seven, trump_jack],
        legal_cards=[ace, seven, trump_jack],
    )

    assert agent.select_card(observation) == ace


def test_prefers_low_value_card_when_no_master_available():
    agent = RuleBasedAgent()

    seven = Card(Suit.HEARTS, Rank.SEVEN)
    ten = Card(Suit.HEARTS, Rank.TEN)

    observation = create_observation(
        hand=[seven, ten],
        legal_cards=[seven, ten],
    )

    assert agent.select_card(observation) == seven


def test_preserves_cards_when_partner_is_winning():
    agent = RuleBasedAgent()

    low_card = Card(Suit.CLUBS, Rank.SEVEN)
    high_card = Card(Suit.SPADES, Rank.JACK)

    observation = create_observation(
        hand=[low_card, high_card],
        legal_cards=[low_card, high_card],
        current_trick=[
            (0, Card(Suit.HEARTS, Rank.ACE)),
        ],
        player_index=2,
    )

    assert agent.select_card(observation) == low_card


def test_wins_with_cheapest_possible_card():
    agent = RuleBasedAgent()

    ten = Card(Suit.HEARTS, Rank.TEN)
    ace = Card(Suit.HEARTS, Rank.ACE)

    observation = create_observation(
        hand=[ten, ace],
        legal_cards=[ten, ace],
        current_trick=[
            (0, Card(Suit.HEARTS, Rank.QUEEN)),
            (1, Card(Suit.HEARTS, Rank.SEVEN)),
        ],
        player_index=2,
    )

    assert agent.select_card(observation) == ten


def test_chooses_lowest_card_when_trick_cannot_be_won():
    agent = RuleBasedAgent()

    seven = Card(Suit.HEARTS, Rank.SEVEN)
    nine = Card(Suit.HEARTS, Rank.NINE)

    observation = create_observation(
        hand=[seven, nine],
        legal_cards=[seven, nine],
        current_trick=[
            (0, Card(Suit.HEARTS, Rank.ACE)),
            (1, Card(Suit.HEARTS, Rank.KING)),
        ],
        player_index=2,
    )

    assert agent.select_card(observation) == seven


def test_leads_remaining_master_card():
    agent = RuleBasedAgent()

    seven = Card(Suit.HEARTS, Rank.SEVEN)
    ten = Card(Suit.HEARTS, Rank.TEN)
    ace = Card(Suit.HEARTS, Rank.ACE)

    observation = create_observation(
        hand=[seven, ten],
        legal_cards=[seven, ten],
        played_history=[(1, ace)],
    )

    assert agent.select_card(observation) == ten