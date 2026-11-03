from klaverjas.cards import create_deck, Suit, Rank


def test_create_deck():
    deck = create_deck()

    assert len(deck) == 32
    assert len(set(deck)) == 32


def test_all_suits_present():
    deck = create_deck()

    assert {card.suit for card in deck} == set(Suit)


def test_all_ranks_present():
    deck = create_deck()

    assert {card.rank for card in deck} == set(Rank)
