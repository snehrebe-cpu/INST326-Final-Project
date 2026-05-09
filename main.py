"""Run the completed Tradeoffs game."""

from __future__ import annotations

from game_state import GameState
from scenarios import build_scenarios, apply_choice
from scoring import build_final_summary
from ui import (
    get_choice,
    print_delayed_messages,
    print_final_summary,
    print_intro,
    print_result,
    print_round_header,
    print_scenario,
)


def run_game() -> None:
    """Run one full game session."""
    scenarios = build_scenarios()
    game_state = GameState(max_rounds=len(scenarios))

    print_intro()

    for scenario in scenarios:
        if game_state.is_game_over():
            break

        print_round_header(game_state)
        delayed_messages = game_state.resolve_pending_effects()
        print_delayed_messages(delayed_messages)
        print_scenario(scenario)

        selected_index = get_choice(len(scenario.choices))
        selected_choice = scenario.choices[selected_index]
        result_text = apply_choice(game_state, scenario, selected_choice)

        print_result(result_text, game_state)

        if game_state.is_depleted():
            print()
            print("A resource reached zero, so the simulation ends early.")
            break

        game_state.next_round()

    summary = build_final_summary(game_state)
    print_final_summary(summary, game_state)


def main() -> None:
    """Start the Tradeoffs game."""
    run_game()


if __name__ == "__main__":
    main()
    
