"""Scoring and final summary functions for Tradeoffs."""

from __future__ import annotations

from typing import Dict, List, Union

from game_state import GameState, MetricMap


SummaryValue = Union[str, int, MetricMap, List[str]]


def calculate_balance_score(game_state: GameState) -> int:
    """Calculate the player's final score.

    Args:
        game_state: Current game state.

    Returns:
        Score from 0 to 100.
    """
    stats = list(game_state.snapshot().values())
    average = sum(stats) / len(stats)
    spread = max(stats) - min(stats)
    score = round((average * 1.7) - (spread * 0.55))
    return max(0, min(100, score))


def get_rating(score: int) -> str:
    """Convert a score into a rating.

    Args:
        score: Final numeric score.

    Returns:
        Rating label.
    """
    if score >= 85:
        return "Excellent"
    if score >= 70:
        return "Strong"
    if score >= 55:
        return "Stable"
    if score >= 40:
        return "Risky"
    return "Unstable"


def describe_play_style(game_state: GameState) -> str:
    """Describe the player's decision pattern.

    Args:
        game_state: Current game state.

    Returns:
        Sentence describing the player's pattern.
    """
    stats = game_state.snapshot()

    if stats["money"] >= 75 and stats["energy"] <= 45:
        return "You focused on money, but your energy dropped."
    if stats["reputation"] >= 75 and stats["time"] <= 45:
        return "You supported people and built trust, but your schedule suffered."
    if stats["energy"] >= 75 and stats["reputation"] <= 45:
        return "You protected your well-being, but avoided some social responsibilities."
    if stats["time"] >= 75:
        return "You kept control of your schedule and avoided taking on too much."

    return (
        f"Your strongest resource was {game_state.highest_resource()}. "
        f"Your weakest resource was {game_state.lowest_resource()}."
    )


def build_warnings(game_state: GameState) -> List[str]:
    """Build warnings based on low resources.

    Args:
        game_state: Current game state.

    Returns:
        List of warning messages.
    """
    warnings = []
    stats = game_state.snapshot()

    if stats["time"] < 35:
        warnings.append("Time fell low. Your schedule became overloaded.")
    if stats["energy"] < 35:
        warnings.append("Energy fell low. Burnout became a serious risk.")
    if stats["money"] < 35:
        warnings.append("Money fell low. Spending or lost income created pressure.")
    if stats["reputation"] < 35:
        warnings.append("Reputation fell low. Trust and visibility took damage.")

    if not warnings:
        warnings.append("No resource ended in the danger zone.")

    return warnings


def list_major_warnings(game_state: GameState) -> list[str]:
    """Return warning messages based on low resources."""
    warnings = []
    stats = game_state.snapshot()

    if stats["time"] < 35:
        warnings.append(
            "Time was low. You took on more than your schedule supported."
        )

    if stats["energy"] < 35:
        warnings.append(
            "Energy was low. Burnout became a serious risk."
        )

    if stats["money"] < 35:
        warnings.append(
            "Money was low. Spending created financial pressure."
        )

    if stats["reputation"] < 35:
        warnings.append(
            "Reputation was low. Relationships and trust suffered."
        )

    if not warnings:
        warnings.append(
            "No resource fell into a danger zone."
        )

    return warnings


def calculate_survival_rating(game_state: GameState) -> str:
    """Return a rating based on the final score."""
    score = calculate_balance_score(game_state)

    if score >= 85:
        return "Excellent"
    if score >= 70:
        return "Strong"
    if score >= 55:
        return "Stable"
    if score >= 40:
        return "Risky"
    return "Unstable"


def build_final_summary(game_state: GameState) -> dict:
    """Create the final report."""
    score = calculate_balance_score(game_state)

    return {
        "score": score,
        "rating": calculate_survival_rating(game_state),
        "play_style": describe_play_style(game_state),
        "warnings": list_major_warnings(game_state),
        "rounds_completed": game_state.round_number - 1,
        "final_stats": game_state.snapshot(),
        "decision_count": len(game_state.history),
        "delayed_effects_triggered": len(game_state.triggered_effects),
    }
