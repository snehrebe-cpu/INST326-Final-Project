"""Core data model for the Tradeoffs game draft."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


MetricMap = Dict[str, int]


@dataclass
class GameState:
    """Stores player resources, history, and round state."""

    time: int = 50
    energy: int = 50
    money: int = 50
    reputation: int = 50
    round_number: int = 1
    max_rounds: int = 5
    history: List[str] = field(default_factory=list)
    pending_effects: List[dict] = field(default_factory=list)

    def apply_changes(self, changes: MetricMap, source: str = "") -> None:
        """Apply immediate stat changes and clamp each value to 0..100."""
        for metric, amount in changes.items():
            if not hasattr(self, metric):
                raise ValueError(f"Unknown metric: {metric}")
            current_value = getattr(self, metric)
            new_value = max(0, min(100, current_value + amount))
            setattr(self, metric, new_value)

        if source:
            self.history.append(source)

    def add_pending_effect(self, delay_rounds: int, changes: MetricMap, note: str) -> None:
        """Schedule a delayed consequence for a future round."""
        self.pending_effects.append(
            {
                "trigger_round": self.round_number + delay_rounds,
                "changes": changes,
                "note": note,
            }
        )

    def resolve_pending_effects(self) -> List[str]:
        """Apply any delayed effects due this round and return their notes."""
        triggered_notes: List[str] = []
        remaining_effects: List[dict] = []

        for effect in self.pending_effects:
            if effect["trigger_round"] <= self.round_number:
                self.apply_changes(effect["changes"], source=effect["note"])
                triggered_notes.append(effect["note"])
            else:
                remaining_effects.append(effect)

        self.pending_effects = remaining_effects
        return triggered_notes

    def next_round(self) -> None:
        """Advance the game by one round."""
        self.round_number += 1

    def is_game_over(self) -> bool:
        """Return True when the player reaches the final round or crashes a stat."""
        depleted = any(
            value <= 0
            for value in [self.time, self.energy, self.money, self.reputation]
        )
        return self.round_number > self.max_rounds or depleted

    def snapshot(self) -> MetricMap:
        """Return the current stats as a dictionary."""
        return {
            "time": self.time,
            "energy": self.energy,
            "money": self.money,
            "reputation": self.reputation,
        }
