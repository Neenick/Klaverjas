
import streamlit as st

from agents.random_agent import RandomAgent
from agents.rule_based_agent import RuleBasedAgent
from cards import Suit
from game import Game
from rules import RuleVariant

from ui.rendering import (
    format_card,
    format_card_button,
    sort_hand,
    render_game_state,
)
from ui.controller import (
    advance_automated_turns,
    reveal_completed_trick,
)


AI_OPTIONS = ["Random", "Rule-based"]
PLAYER_FOUR_OPTIONS = ["Human", "Random", "Rule-based"]


def create_agents(player_types, seed):
    """Create the selected agents for all four players."""

    agents = []

    for player_index, player_type in enumerate(player_types):
        agent_seed = seed + player_index + 1

        if player_type == "Human":
            agents.append(None)

        elif player_type == "Random":
            agents.append(RandomAgent(seed=agent_seed))

        elif player_type == "Rule-based":
            agents.append(RuleBasedAgent(seed=agent_seed))

        else:
            raise ValueError(f"Unknown player type: {player_type}")

    return agents


def render_human_hand(
    game,
    board_placeholder,
    player_types,
    reveal_hands,
    card_delay,
    winner_delay,
    result_pause,
):
    """Display the human player's hand and process card selection."""

    observation = game.get_observation()

    st.subheader("Your hand · Player 4")
    st.caption("Choose one of the enabled cards to play.")

    hand = sort_hand(observation.hand)
    columns = st.columns(len(hand))

    for column, card in zip(columns, hand):
        legal = card in observation.legal_cards

        with column:
            clicked = st.button(
                format_card_button(card),
                key=(
                    f"play_{len(game.history.played_cards)}_"
                    f"{card.suit.value}_{card.rank.value}"
                ),
                disabled=not legal,
                type="primary" if legal else "secondary",
                use_container_width=True,
            )

        if clicked:
            previous_trick_count = len(game.tricks)

            game.play_card(card)

            trick_completed = len(game.tricks) > previous_trick_count

            if trick_completed:
                reveal_completed_trick(
                    game,
                    player_types,
                    reveal_hands,
                    board_placeholder,
                    winner_delay,
                    result_pause,
                )
            else:
                render_game_state(
                    board_placeholder,
                    game,
                    player_types,
                    reveal_hands,
                    show_last_trick=False,
                )

                if card_delay > 0:
                    import time
                    time.sleep(card_delay)

            advance_automated_turns(
                game,
                player_types,
                reveal_hands,
                board_placeholder,
                card_delay,
                winner_delay,
                result_pause,
            )

            st.rerun()


def render_game_history(game):
    """Display the completed tricks."""

    with st.expander(f"Game history ({len(game.tricks)}/8 tricks)"):

        for i, trick in enumerate(game.tricks):
            winner = trick.winner(game.trump_suit)

            points = trick.points(
                game.trump_suit,
                is_last_trick=(i == 7),
            )

            cards = " | ".join(
                f"P{player + 1}: {format_card(card)}"
                for player, card in trick.played_cards
            )

            st.markdown(
                f"**Trick {i + 1}** — "
                f"Player {winner + 1} wins ({points} points)"
            )

            st.caption(cards)


def main():
    st.set_page_config(
        page_title="Klaverjas Agents",
        page_icon="🃏",
        layout="wide",
    )

    st.title("🃏 Klaverjas Agents")
    st.caption("Play against AI agents or watch them play against each other.")

    # --------------------------------------------------
    # SIDEBAR: GAME SETTINGS
    # --------------------------------------------------
    board_placeholder = st.empty()

    with st.sidebar:
        st.header("Game setup")

        st.markdown("**Player positions**")

        player_1 = st.selectbox(
            "Player 1 · Left",
            AI_OPTIONS,
            index=0,
            key="setup_player_1",
        )

        player_2 = st.selectbox(
            "Player 2 · Top",
            AI_OPTIONS,
            index=0,
            key="setup_player_2",
        )

        player_3 = st.selectbox(
            "Player 3 · Right",
            AI_OPTIONS,
            index=1,
            key="setup_player_3",
        )

        player_4 = st.selectbox(
            "Player 4 · Bottom",
            PLAYER_FOUR_OPTIONS,
            index=0,
            key="setup_player_4",
        )

        player_types = [
            player_1,
            player_2,
            player_3,
            player_4,
        ]

        st.divider()

        trump_name = st.selectbox(
            "Trump suit",
            [suit.value for suit in Suit],
            index=2,
        )

        variant_name = st.selectbox(
            "Rule variant",
            [variant.value for variant in RuleVariant],
            index=0,
        )

        seed = st.number_input(
            "Random seed",
            min_value=0,
            value=42,
            step=1,
        )

        st.divider()

        st.markdown("**Animation settings**")

        card_delay = st.slider(
            "Delay between AI cards",
            min_value=0.0,
            max_value=1.5,
            value=0.35,
            step=0.05,
            help="Time between individual AI card plays.",
        )

        winner_delay = st.slider(
            "Winner reveal delay",
            min_value=0.0,
            max_value=2.0,
            value=0.65,
            step=0.05,
        )

        result_pause = st.slider(
            "Trick result pause",
            min_value=0.0,
            max_value=2.0,
            value=0.8,
            step=0.05,
        )

        st.divider()

        reveal_hands = st.checkbox(
            "Reveal all players' cards",
            value=False,
            help="Debug option. Reveals every player's hand.",
        )

        if reveal_hands:
            st.warning(
                "Debug mode enabled. All hands are visible, "
                "but agents still only receive their own observation."
            )

        start_game = st.button(
            "Start new game",
            type="primary",
            use_container_width=True,
        )

    # --------------------------------------------------
    # START NEW GAME
    # --------------------------------------------------

    if start_game:
        agents = create_agents(player_types, int(seed))

        game = Game(
            agents=agents,
            trump_suit=Suit(trump_name),
            variant=RuleVariant(variant_name),
            seed=int(seed),
        )

        game.start()

        st.session_state.game = game
        st.session_state.player_types = player_types.copy()
        st.session_state.reveal_hands = reveal_hands

    # --------------------------------------------------
    # LOAD GAME
    # --------------------------------------------------

    game = st.session_state.get("game")

    if game is None:
        st.info("Configure the players and start a new game.")
        return

    active_player_types = st.session_state.player_types

    # Keep the current game configuration stable.
    st.session_state.reveal_hands = reveal_hands
    st.session_state.player_types = active_player_types

    st.session_state.board_placeholder = st.empty()

    board_placeholder = st.session_state.board_placeholder

    # --------------------------------------------------
    # INITIAL RENDER AND AUTOMATED TURNS
    # --------------------------------------------------

    render_game_state(
        board_placeholder,
        game,
        active_player_types,
        reveal_hands,
        show_last_trick=True,
    )

    advance_automated_turns(
        game,
        active_player_types,
        reveal_hands,
        board_placeholder,
        card_delay,
        winner_delay,
        result_pause,
    )

    # Render the final state after automated turns.
    render_game_state(
        board_placeholder,
        game,
        active_player_types,
        reveal_hands,
        show_last_trick=True,
    )

    # --------------------------------------------------
    # HUMAN PLAYER
    # --------------------------------------------------

    if not game.finished and game.current_player == 3:
        render_human_hand(
            game,
            board_placeholder,
            active_player_types,
            reveal_hands,
            card_delay,
            winner_delay,
            result_pause,
        )

    # --------------------------------------------------
    # GAME RESULT
    # --------------------------------------------------

    if game.finished:
        result = game.get_result()

        st.subheader("Game finished!")

        if result["winner"] == 0:
            st.success("Team A wins!")
        elif result["winner"] == 1:
            st.success("Team B wins!")
        else:
            st.info("The game ended in a draw.")

        st.write(
            f"Final score: {result['scores'][0]} - "
            f"{result['scores'][1]}"
        )

    # --------------------------------------------------
    # GAME HISTORY
    # --------------------------------------------------

    render_game_history(game)


if __name__ == "__main__":
    main()
