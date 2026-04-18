"""Scoring and end-of-game summary helpers for the Tradeoffs game draft."""

from __future__ import annotations

from typing import Dict

from game_state import GameState


def calculate_balance_score(game_state: GameState) -> int:
    """Score the player based on remaining resources and balance across metrics."""
    stats = list(game_state.snapshot().values())
    average = sum(stats) / len(stats)
    spread_penalty = max(stats) - min(stats)
    return max(0, int(average * 2 - spread_penalty))


def describe_play_style(game_state: GameState) -> str:
    """Generate a rough summary of the player's decision style."""
    stats = game_state.snapshot()

    highest_metric = max(stats, key=stats.get)
    lowest_metric = min(stats, key=stats.get)

    if stats["money"] >= 70 and stats["energy"] < 40:
        return "You prioritized income, but your well-being took a hit."
    if stats["reputation"] >= 70 and stats["time"] < 40:
        return "You invested in relationships and image, often at the cost of time."
    if stats["energy"] >= 70:
        return "You protected your well-being and avoided burnout better than most players."

    return (
        f"Your strongest area was {highest_metric}, "
        f"but {lowest_metric} needs more attention."
    )


def build_final_summary(game_state: GameState) -> Dict[str, str | int]:
    """Create a lightweight final report for the player."""
    return {
        "score": calculate_balance_score(game_state),
        "play_style": describe_play_style(game_state),
        "rounds_completed": game_state.round_number - 1,
        "history_count": len(game_state.history),
    }
