"""Game state and resource logic for the Tradeoffs project."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


MetricMap = Dict[str, int]


@dataclass
class DelayedEffect:
    """Store a delayed consequence.

    Attributes:
        trigger_round: Round when the effect should happen.
        changes: Resource changes caused by the effect.
        note: Message shown when the effect happens.
    """

    trigger_round: int
    changes: MetricMap
    note: str


@dataclass
class DecisionRecord:
    """Store one player decision.

    Attributes:
        round_number: Round when the player made the choice.
        scenario_title: Title of the scenario.
        choice_text: Text of the selected option.
        result_text: Message shown after the option.
    """

    round_number: int
    scenario_title: str
    choice_text: str
    result_text: str


@dataclass
class GameState:
    """Track player resources, rounds, decisions, and delayed effects.

    Attributes:
        time: Player's available time resource.
        energy: Player's energy resource.
        money: Player's money resource.
        reputation: Player's reputation resource.
        round_number: Current round number.
        max_rounds: Total number of rounds in the game.
        history: List of player decisions.
        pending_effects: Delayed effects waiting for later rounds.
        triggered_effects: Notes from delayed effects that already happened.
    """


    time: int = 60
    energy: int = 60
    money: int = 60
    reputation: int = 60
    round_number: int = 1
    max_rounds: int = 12
    history: List[DecisionRecord] = field(default_factory=list)
    pending_effects: List[DelayedEffect] = field(default_factory=list)
    triggered_effects: List[str] = field(default_factory=list)

    def snapshot(self) -> MetricMap:
        """Return all current resource values.

        Returns:
            Dictionary with resource names and values.
        """
        return {
            "time": self.time,
            "energy": self.energy,
            "money": self.money,
            "reputation": self.reputation,
        }

    def apply_changes(self, changes: MetricMap) -> None:
        """Apply resource changes and clamp values from 0 to 100.

        Args:
            changes: Dictionary of resource changes.

        Raises:
            ValueError: If a change uses an unknown resource name.
        """
        for metric, amount in changes.items():
            if metric not in self.snapshot():
                raise ValueError(f"Unknown resource: {metric}")

            current_value = getattr(self, metric)
            new_value = current_value + amount
            new_value = max(0, min(100, new_value))
            setattr(self, metric, new_value)

    def record_decision(self, scenario_title: str, choice_text: str, result_text: str) -> None:
        """Save the player's decision.

        Args:
            scenario_title: Title of the current scenario.
            choice_text: Option chosen by the player.
            result_text: Result message for the choice.
        """
        self.history.append(
            DecisionRecord(
                round_number=self.round_number,
                scenario_title=scenario_title,
                choice_text=choice_text,
                result_text=result_text,
            )
        )

    def add_pending_effect(self, delay_rounds: int, changes: MetricMap, note: str) -> None:
        """Schedule a delayed effect.

        Args:
            delay_rounds: Number of rounds before the effect happens.
            changes: Resource changes caused by the effect.
            note: Message shown when the effect happens.

        Raises:
            ValueError: If delay_rounds is less than 1.
        """
        if delay_rounds < 1:
            raise ValueError("Delayed effects must trigger at least one round later.")

        self.pending_effects.append(
            DelayedEffect(
                trigger_round=self.round_number + delay_rounds,
                changes=changes,
                note=note,
            )
        )

    def resolve_pending_effects(self) -> List[str]:
        """Apply delayed effects due this round and return their notes."""
        triggered_notes = []
        remaining_effects = []

        for effect in self.pending_effects:
            if effect.trigger_round <= self.round_number:
                self.apply_changes(effect.changes)
                triggered_notes.append(effect.note)
                self.triggered_effects.append(effect.note)
            else:
                remaining_effects.append(effect)

        self.pending_effects = remaining_effects
        return triggered_notes

    def next_round(self) -> None:
        """Advance the game by one round."""
        self.round_number += 1

    def is_depleted(self) -> bool:
        """Return True if any resource reaches zero."""
        return any(value <= 0 for value in self.snapshot().values())

    def is_game_over(self) -> bool:
        """Return True if the game has ended.

        Returns:
            True when the player has no resources or no rounds remain.
        """
        return self.round_number > self.max_rounds or self.is_depleted()

    def lowest_resource(self) -> str:
        """Return the name of the lowest resource.

        Returns:
            Resource name with the lowest value.
        """
        stats = self.snapshot()
        return min(stats, key=stats.get)

    def highest_resource(self) -> str:
        """Return the name of the highest resource.

        Returns:
            Resource name with the highest value.
        """
        stats = self.snapshot()
        return max(stats, key=stats.get)
