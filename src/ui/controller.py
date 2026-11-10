
import time

from ui.rendering import render_game_state


def reveal_completed_trick(
    game,
    player_types,
    reveal_hands,
    board_placeholder,
    winner_delay: float = 0.65,
    result_pause: float = 0.8,
):
    """Show all four cards before highlighting the trick winner."""

    # First show the completed trick without a winner highlight.
    render_game_state(
        board_placeholder,
        game,
        player_types,
        reveal_hands,
        show_last_trick=True,
        reveal_winner=False,
    )

    if winner_delay > 0:
        time.sleep(winner_delay)

    # Now reveal the winner.
    render_game_state(
        board_placeholder,
        game,
        player_types,
        reveal_hands,
        show_last_trick=True,
        reveal_winner=True,
    )

    if result_pause > 0:
        time.sleep(result_pause)


def advance_automated_turns(
    game,
    player_types,
    reveal_hands,
    board_placeholder,
    card_delay: float = 0.35,
    winner_delay: float = 0.65,
    result_pause: float = 0.8,
):
    """Let automated players play until a human turn or game end."""

    while not game.finished:

        player_index = game.current_player

        if player_index is None:
            break

        # Stop when it is the human player's turn.
        if game.agents[player_index] is None:
            break

        previous_trick_count = len(game.tricks)

        game.play_agent_turn()

        # Check whether the agent completed a trick.
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
            # Show the newly played card.
            render_game_state(
                board_placeholder,
                game,
                player_types,
                reveal_hands,
                show_last_trick=False,
            )

            if card_delay > 0:
                time.sleep(card_delay)
