"""Text interface helpers for Tradeoffs."""

from __future__ import annotations

from game_state import GameState
from scenarios import Scenario


def print_divider() -> None:
    """Print a divider line."""
    print("-" * 58)


def print_intro() -> None:
    """Print the game introduction."""
    print_divider()
    print("TRADEOFFS")
    print_divider()
    print("A decision-making simulation game")
    print()
    print("You will face 12 student-life scenarios.")
    print("Each choice affects time, energy, money, and reputation.")
    print("Some choices create delayed consequences in later rounds.")
    print("Try to finish with balanced resources.")
    print_divider()


def print_stats(game_state: GameState) -> None:
    """Print resource values.

    Args:
        game_state: Current game state.
    """
    print("Resources:")
    for metric, value in game_state.snapshot().items():
        print(f"  {metric.title():<12} {value:>3}/100")


def print_pending_count(game_state: GameState) -> None:
    """Print the number of unresolved delayed effects.

    Args:
        game_state: Current game state.
    """
    count = len(game_state.pending_effects)
    print(f"Pending delayed consequences: {count}")


def print_round_header(game_state: GameState) -> None:
    """Print the round header.

    Args:
        game_state: Current game state.
    """
    print()
    print_divider()
    print(f"Round {game_state.round_number} of {game_state.max_rounds}")
    print_divider()
    print_stats(game_state)
    print_pending_count(game_state)
    print()


def print_delayed_messages(messages: list[str]) -> None:
    """Print delayed consequence messages.

    Args:
        messages: Messages from delayed effects.
    """
    for message in messages:
        print(f"Delayed consequence: {message}")

    if messages:
        print()


def print_scenario(scenario: Scenario) -> None:
    """Print a scenario and its choices.

    Args:
        scenario: Scenario shown to the player.
    """
    print(scenario.title)
    print(scenario.prompt)
    print()

    for index, choice in enumerate(scenario.choices, start=1):
        print(f"{index}. {choice.text}")


def get_choice(option_count: int) -> int:
    """Ask for a valid choice number.

    Args:
        option_count: Number of choices.

    Returns:
        Zero-based index of the selected choice.
    """
    while True:
        raw_choice = input("Enter your choice number: ").strip()

        if raw_choice.isdigit():
            selected = int(raw_choice)
            if 1 <= selected <= option_count:
                return selected - 1

        print(f"Invalid choice. Enter a number from 1 to {option_count}.")


def print_result(result_text: str, game_state: GameState) -> None:
    """Print the result and updated resources.

    Args:
        result_text: Result for the player's choice.
        game_state: Current game state.
    """
    print()
    print(f"Result: {result_text}")
    print()
    print_stats(game_state)


def print_decision_history(game_state: GameState) -> None:
    """Print the player's decision history.

    Args:
        game_state: Current game state.
    """
    print()
    print("Decision history:")

    if not game_state.history:
        print("  No decisions recorded.")
        return

    for record in game_state.history:
        print(f"  Round {record.round_number}: {record.scenario_title}")
        print(f"    Choice: {record.choice_text}")
        print(f"    Result: {record.result_text}")


def print_final_summary(summary: dict, game_state: GameState) -> None:
    """Print the final summary screen.

    Args:
        summary: Final summary dictionary.
        game_state: Current game state.
    """
    print()
    print_divider()
    print("FINAL SUMMARY")
    print_divider()
    print(f"Score: {summary['score']}/100")
    print(f"Rating: {summary['rating']}")
    print(f"Rounds completed: {summary['rounds_completed']}")
    print(f"Decision records: {summary['decision_count']}")
    print(f"Delayed effects triggered: {summary['delayed_effects_triggered']}")
    print()
    print(summary["play_style"])
    print()
    print("Final resources:")

    for metric, value in summary["final_stats"].items():
        print(f"  {metric.title():<12} {value:>3}/100")

    print()
    print("Warnings:")
    for warning in summary["warnings"]:
        print(f"  - {warning}")

    print_decision_history(game_state)
    print_divider()
    print(f"Score: {summary['score']}/100")
    print(f"Rating: {summary['rating']}")
    print(f"Rounds completed: {summary['rounds_completed']}")
    print(f"Decision records: {summary['decision_count']}")
    print()
    print(summary["play_style"])
    print()
    print("Final stats:")
    for metric, value in summary["final_stats"].items():
        print(f"  {metric.title():<12} {value:>3}/100")
    print()
    print("Warnings:")
    for warning in summary["warnings"]:
        print(f"  - {warning}")
    print_divider()
