"""Text interface helpers for Tradeoffs."""

from __future__ import annotations

from game_state import GameState
from scenarios import Scenario


def print_divider() -> None:
    """Print a visual divider."""
    print("-" * 55)


def print_intro() -> None:
    """Print the game introduction."""
    print_divider()
    print("TRADEOFFS")
    print_divider()
    print("You will make choices across school, work, money, and relationships.")
    print("Each choice changes four resources:")
    print("time, energy, money, and reputation.")
    print("Some choices also create delayed consequences.")
    print_divider()


def print_stats(game_state: GameState) -> None:
    """Print resource values."""
    stats = game_state.snapshot()
    print("Current resources:")
    for metric, value in stats.items():
        print(f"  {metric.title():<12} {value:>3}/100")


def print_pending_count(game_state: GameState) -> None:
    """Print the number of unresolved delayed effects."""
    count = len(game_state.pending_effects)
    if count == 1:
        print("Pending consequence: 1")
    else:
        print(f"Pending consequences: {count}")


def print_scenario(scenario: Scenario) -> None:
    """Print a scenario and its choices."""
    print(f"Scenario: {scenario.prompt}")
    for index, choice in enumerate(scenario.choices, start=1):
        print(f"  {index}. {choice.text}")


def get_choice(option_count: int) -> int:
    """Ask the user for a valid choice number."""
    while True:
        raw_choice = input("Choose 1 or 2: ").strip()

        if raw_choice.isdigit():
            selected = int(raw_choice)
            if 1 <= selected <= option_count:
                return selected - 1

        print("Please enter a valid option number.")


def print_final_summary(summary: dict) -> None:
    """Print the final report."""
    print_divider()
    print("FINAL SUMMARY")
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
