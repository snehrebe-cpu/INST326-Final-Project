"""Scenario definitions and helpers for the Tradeoffs game draft."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from game_state import GameState, MetricMap


@dataclass
class Choice:
    text: str
    immediate_changes: MetricMap
    delayed_changes: Optional[MetricMap] = None
    delayed_rounds: int = 0
    delayed_note: str = ""


@dataclass
class Scenario:
    id: str
    prompt: str
    choices: List[Choice]


def build_sample_scenarios() -> List[Scenario]:
    """Return a small starter set of scenarios for early testing."""
    return [
        Scenario(
            id="late_study_session",
            prompt="You have an exam tomorrow. Do you stay up late to study or sleep early?",
            choices=[
                Choice(
                    text="Stay up late and cram",
                    immediate_changes={"time": -10, "energy": -20, "reputation": 5},
                    delayed_changes={"energy": -10},
                    delayed_rounds=1,
                    delayed_note="Lack of sleep hits you the next day.",
                ),
                Choice(
                    text="Sleep early and review lightly",
                    immediate_changes={"time": -5, "energy": 10, "reputation": 0},
                ),
            ],
        ),
        Scenario(
            id="extra_work_shift",
            prompt="Your manager offers you an extra shift during a busy school week.",
            choices=[
                Choice(
                    text="Take the shift for extra cash",
                    immediate_changes={"time": -15, "energy": -10, "money": 20},
                    delayed_changes={"reputation": -5},
                    delayed_rounds=1,
                    delayed_note="You miss a group meeting and frustrate your team.",
                ),
                Choice(
                    text="Turn it down and focus on school",
                    immediate_changes={"money": -5, "time": 10, "energy": 5},
                ),
            ],
        ),
        Scenario(
            id="friend_needs_help",
            prompt="A close friend asks for help moving on the same day you planned to rest.",
            choices=[
                Choice(
                    text="Help your friend",
                    immediate_changes={"time": -10, "energy": -10, "reputation": 10},
                ),
                Choice(
                    text="Protect your downtime",
                    immediate_changes={"energy": 15, "reputation": -5},
                ),
            ],
        ),
    ]


def apply_choice(game_state: GameState, choice: Choice) -> None:
    """Apply the selected choice to the current game state."""
    game_state.apply_changes(choice.immediate_changes, source=choice.text)

    if choice.delayed_changes:
        game_state.add_pending_effect(
            delay_rounds=choice.delayed_rounds,
            changes=choice.delayed_changes,
            note=choice.delayed_note or "A delayed consequence occurs.",
        )
