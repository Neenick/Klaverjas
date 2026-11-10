
import html

import streamlit as st

from cards import Card, Rank, Suit


RANK_SYMBOLS = {
    Rank.SEVEN: "7",
    Rank.EIGHT: "8",
    Rank.NINE: "9",
    Rank.TEN: "10",
    Rank.JACK: "J",
    Rank.QUEEN: "Q",
    Rank.KING: "K",
    Rank.ACE: "A",
}

SUIT_SYMBOLS = {
    Suit.CLUBS: "♣",
    Suit.DIAMONDS: "♦",
    Suit.HEARTS: "♥",
    Suit.SPADES: "♠",
}


def format_card(card: Card) -> str:
    return f"{RANK_SYMBOLS[card.rank]}{SUIT_SYMBOLS[card.suit]}"


def format_card_button(card: Card) -> str:
    rank = RANK_SYMBOLS[card.rank]
    suit = SUIT_SYMBOLS[card.suit]

    if card.suit in (Suit.HEARTS, Suit.DIAMONDS):
        return f"{rank} :red[{suit}]"

    return f"{rank} {suit}"


def sort_hand(hand: tuple[Card, ...]) -> list[Card]:
    suit_order = {
        Suit.CLUBS: 0,
        Suit.DIAMONDS: 1,
        Suit.HEARTS: 2,
        Suit.SPADES: 3,
    }

    return sorted(
        hand,
        key=lambda card: (
            suit_order[card.suit],
            card.rank.value,
        ),
    )


def _card_html(card: Card | None, state: str = "") -> str:
    if card is None:
        return '<div class="played-card empty">·</div>'

    suit = SUIT_SYMBOLS[card.suit]
    rank = RANK_SYMBOLS[card.rank]

    color = (
        "red-card"
        if card.suit in (Suit.HEARTS, Suit.DIAMONDS)
        else "black-card"
    )

    return f"""
        <div class="played-card {color} {state}">
            <span>{rank}</span>
            <span>{suit}</span>
        </div>
    """


def _player_panel(
    player_index: int,
    game,
    player_types: list[str],
    reveal_hands: bool,
) -> str:
    player_type = player_types[player_index]

    team = "Team A" if player_index % 2 == 0 else "Team B"

    is_current = (
        game.current_player == player_index
        and not game.finished
    )

    status = "YOUR TURN" if is_current and player_type == "Human" else (
        "PLAYING" if is_current else "WAITING"
    )

    hand = game.hands[player_index]

    if reveal_hands:
        hand_info = " · ".join(format_card(card) for card in sort_hand(tuple(hand)))
    elif player_type == "Human" and player_index == 3:
        hand_info = "Your hand is below"
    else:
        hand_info = f"{len(hand)} cards hidden"

    active_class = "active" if is_current else ""

    return f"""
        <div class="player-panel seat-{player_index} {active_class}">
            <div class="player-name">PLAYER {player_index + 1}</div>
            <div class="player-type">{html.escape(player_type)}</div>
            <div class="player-team">{team}</div>
            <div class="player-status">{status}</div>
            <div class="player-hand-info">{html.escape(hand_info)}</div>
        </div>
    """


CSS = """
<style>
.game-shell {
    width: 100%;
    margin-bottom: 1rem;
}

.game-meta {
    color: var(--text-color);
    opacity: 0.7;
    text-align: center;
    margin-bottom: 12px;
    font-size: 0.85rem;
}

.score-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
}

.team-score {
    background: var(--secondary-background-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.team-score.team-winning {
    border: 2px solid #16a34a;
}

.team-label {
    font-size: 0.85rem;
    font-weight: 600;
}

.score-value {
    font-size: 1.8rem;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
}

.klaverjas-board {
    background: #145b43;
    border: 5px solid #0d4030;
    border-radius: 32px;
    padding: 18px;
    display: grid;
    grid-template-columns: minmax(110px, 1fr) minmax(150px, 1.5fr) minmax(110px, 1fr);
    grid-template-rows: auto minmax(190px, 1fr) auto;
    grid-template-areas:
        ". top ."
        "left center right"
        ". bottom .";
    gap: 12px;
    min-height: 440px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.18);
}

.player-panel {
    border-radius: 14px;
    background: rgba(255,255,255,0.94);
    color: #17231d;
    padding: 10px 8px;
    text-align: center;
    border: 3px solid transparent;
    min-width: 0;
    align-self: center;
    overflow-wrap: anywhere;
}

.player-panel.seat-0 {
    grid-area: left;
}

.player-panel.seat-1 {
    grid-area: top;
}

.player-panel.seat-2 {
    grid-area: right;
}

.player-panel.seat-3 {
    grid-area: bottom;
}

.player-panel.active {
    border-color: #facc15;
    box-shadow: 0 0 12px rgba(250,204,21,0.65);
}

.player-name {
    font-weight: 800;
    font-size: 0.9rem;
}

.player-type, .player-team {
    font-size: 0.75rem;
    margin-top: 2px;
}

.player-team {
    color: #52645a;
}

.player-status {
    font-size: 0.7rem;
    font-weight: 700;
    margin-top: 5px;
    color: #65756a;
}

.player-panel.active .player-status {
    color: #15803d;
}

.player-hand-info {
    font-size: 0.68rem;
    margin-top: 5px;
    line-height: 1.4;
    color: #48554c;
}

.trick-area {
    grid-area: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border-radius: 25px;
    border: 1px dashed rgba(255,255,255,0.35);
    background: rgba(0,0,0,0.09);
    padding: 8px;
    min-width: 0;
}

.trick-heading {
    color: white;
    font-size: 0.8rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.trick-grid {
    width: 100%;
    max-width: 250px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(3, 1fr);
    gap: 5px;
    justify-items: center;
    align-items: center;
}

.trick-card-top {
    grid-area: 1 / 2;
}

.trick-card-left {
    grid-area: 2 / 1;
}

.trick-card-right {
    grid-area: 2 / 3;
}

.trick-card-bottom {
    grid-area: 3 / 2;
}

.played-card {
    width: 54px;
    height: 72px;
    border-radius: 7px;
    background: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-size: 1.2rem;
    font-weight: 800;
    line-height: 1.2;
    border: 2px solid #d1d5db;
    box-shadow: 0 3px 5px rgba(0,0,0,0.2);
}

.played-card.red-card {
    color: #dc2626;
}

.played-card.black-card {
    color: #111827;
}

.played-card.empty {
    background: rgba(255,255,255,0.08);
    border: 1px dashed rgba(255,255,255,0.3);
    color: rgba(255,255,255,0.4);
    box-shadow: none;
}

.played-card.current-leader {
    border: 3px solid #facc15;
}

.played-card.winner {
    background: #dcfce7;
    border: 3px solid #16a34a;
    transform: scale(1.08);
}

.played-card.loser {
    background: #fee2e2;
    border: 2px solid #dc2626;
}

.trick-result {
    font-size: 0.82rem;
    font-weight: 700;
    color: white;
    text-align: center;
    margin-top: 10px;
}

.result-team-a {
    color: #bbf7d0;
}

.result-team-b {
    color: #fecaca;
}

@media (max-width: 650px) {
    .klaverjas-board {
        padding: 8px;
        gap: 6px;
        grid-template-columns: minmax(80px, 1fr) minmax(100px, 1.3fr) minmax(80px, 1fr);
        min-height: 370px;
        border-radius: 20px;
    }

    .player-panel {
        padding: 7px 4px;
    }

    .player-name {
        font-size: 0.75rem;
    }

    .played-card {
        width: 42px;
        height: 59px;
        font-size: 1rem;
    }
}
</style>
"""


def render_game_state(
    placeholder,
    game,
    player_types: list[str],
    reveal_hands: bool = False,
    show_last_trick: bool = True,
    reveal_winner: bool = True,
):
    """Render the scoreboard and four-player table."""

    # Select the active or most recently completed trick.
    if game.current_trick.cards:
        trick = game.current_trick
    elif show_last_trick and game.tricks:
        trick = game.tricks[-1]
    else:
        trick = None

    trick_complete = trick is not None and trick.is_complete()

    winner = trick.winner(game.trump_suit) if trick else None

    if trick_complete:
        trick_number = len(game.tricks)
    else:
        trick_number = len(game.tricks) + 1

    # Render the four played-card positions.
    played_by_player = (
        dict(trick.played_cards) if trick else {}
    )

    positions = {
        0: "trick-card-left",
        1: "trick-card-top",
        2: "trick-card-right",
        3: "trick-card-bottom",
    }

    card_elements = []

    for player_index in range(4):
        card = played_by_player.get(player_index)
        state = ""

        if card is not None:
            if trick_complete and reveal_winner:
                state = "winner" if player_index == winner else "loser"
            elif not trick_complete and player_index == winner:
                state = "current-leader"

        card_elements.append(
            f'<div class="{positions[player_index]}">'
            f'{_card_html(card, state)}'
            f'</div>'
        )

    # Build trick status.
    if trick_complete and reveal_winner:
        points = trick.points(
            game.trump_suit,
            is_last_trick=(len(game.tricks) == 8),
        )

        team = "A" if winner % 2 == 0 else "B"
        result_class = "result-team-a" if team == "A" else "result-team-b"

        trick_status = (
            f'<div class="trick-result {result_class}">'
            f'Player {winner + 1} wins · Team {team} +{points} points'
            f'</div>'
        )

    elif trick_complete:
        trick_status = (
            '<div class="trick-result">Resolving trick...</div>'
        )

    elif trick and trick.cards:
        trick_status = (
            f'<div class="trick-result">'
            f'{len(trick.cards)}/4 cards · Player {winner + 1} currently leads'
            f'</div>'
        )

    else:
        trick_status = (
            '<div class="trick-result">Waiting for the first card</div>'
        )

    # Render player panels.
    players_html = {
        i: _player_panel(i, game, player_types, reveal_hands)
        for i in range(4)
    }

    trump_symbol = SUIT_SYMBOLS[game.trump_suit]
    trump_name = game.trump_suit.value.capitalize()
    variant_name = game.variant.value.capitalize()

    completed_winner = (
        winner if trick_complete and reveal_winner else None
    )

    team_a_class = (
        "team-winning"
        if completed_winner is not None and completed_winner % 2 == 0
        else ""
    )

    team_b_class = (
        "team-winning"
        if completed_winner is not None and completed_winner % 2 == 1
        else ""
    )

    board_html = CSS + f"""
        <div class="game-shell">

            <div class="game-meta">
                Trump: {trump_symbol} {html.escape(trump_name)}
                &nbsp; · &nbsp;
                Rules: {html.escape(variant_name)}
                &nbsp; · &nbsp;
                Trick {trick_number}/8
            </div>

            <div class="score-row">
                <div class="team-score {team_a_class}">
                    <div>
                        <div class="team-label">TEAM A</div>
                        <div style="font-size:0.72rem;opacity:0.65">
                            Players 1 & 3
                        </div>
                    </div>
                    <div class="score-value">{game.scores[0]}</div>
                </div>

                <div class="team-score {team_b_class}">
                    <div>
                        <div class="team-label">TEAM B</div>
                        <div style="font-size:0.72rem;opacity:0.65">
                            Players 2 & 4
                        </div>
                    </div>
                    <div class="score-value">{game.scores[1]}</div>
                </div>
            </div>

            <div class="klaverjas-board">

                {players_html[1]}
                {players_html[0]}

                <div class="trick-area">
                    <div class="trick-heading">PLAYING AREA</div>

                    <div class="trick-grid">
                        {''.join(card_elements)}
                    </div>

                    {trick_status}
                </div>

                {players_html[2]}
                {players_html[3]}

            </div>
        </div>
    """

    # Remove indentation and empty lines to prevent Markdown
    # from interpreting the HTML as a code block.
    renderable_html = "\n".join(
        line.strip()
        for line in board_html.splitlines()
        if line.strip()
    )

    placeholder.markdown(
        renderable_html,
        unsafe_allow_html=True,
    )
