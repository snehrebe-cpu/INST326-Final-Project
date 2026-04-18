"""Starter command-line loop for the Tradeoffs game draft."""

from __future__ import annotations

from game_state import GameState
from scenarios import apply_choice, build_sample_scenarios
from scoring import build_final_summary


def print_stats(game_state: GameState) -> None:
    """Display the current resource values."""
    stats = game_state.snapshot()
    print("\nCurrent stats:")
    for key, value in stats.items():
        print(f"  {key.title()}: {value}")


def choose_option(option_count: int) -> int:
    """Prompt the player until they enter a valid choice number."""
    while True:
        raw = input("Choose an option number: ").strip()
        if raw.isdigit():
            selected = int(raw)
            if 1 <= selected <= option_count:
                return selected - 1
        print("Invalid input. Enter a valid option number.")


def run_game() -> None:
    """Run a small playable draft loop."""
    game_state = GameState()
    scenarios = build_sample_scenarios()

    print("Welcome to Tradeoffs.")
    print("Your choices affect time, energy, money, and reputation.")

    for scenario in scenarios:
        if game_state.is_game_over():
            break

        print(f"\nRound {game_state.round_number}")
        triggered_notes = game_state.resolve_pending_effects()
        for note in triggered_notes:
            print(f"Delayed effect: {note}")

        print_stats(game_state)
        print(f"\nScenario: {scenario.prompt}")

        for index, choice in enumerate(scenario.choices, start=1):
            print(f"{index}. {choice.text}")

        selected_index = choose_option(len(scenario.choices))
        selected_choice = scenario.choices[selected_index]
        apply_choice(game_state, selected_choice)

        game_state.next_round()

    print("\nGame over.")
    print_stats(game_state)

    summary = build_final_summary(game_state)
    print("\nFinal summary:")
    for key, value in summary.items():
        label = key.replace("_", " ").title()
        print(f"{label}: {value}")


if __name__ == "__main__":
    run_game()
