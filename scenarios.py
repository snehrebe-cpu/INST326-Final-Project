"""Scenario data and choice logic for Tradeoffs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from game_state import GameState, MetricMap


@dataclass
class Choice:
    """Represent one choice inside a scenario.

    Attributes:
        text: Choice text shown to the player.
        result_text: Result shown after the choice.
        immediate_changes: Resource changes applied right away.
        delayed_changes: Optional resource changes applied later.
        delayed_rounds: Number of rounds before delayed changes happen.
        delayed_note: Message shown when delayed changes happen.
    """

    text: str
    result_text: str
    immediate_changes: MetricMap
    delayed_changes: Optional[MetricMap] = None
    delayed_rounds: int = 0
    delayed_note: str = ""


@dataclass
class Scenario:
    """Represent one game scenario.

    Attributes:
        title: Scenario title.
        prompt: Situation shown to the player.
        choices: List of available choices.
    """

    title: str
    prompt: str
    choices: List[Choice]


def build_scenarios() -> List[Scenario]:
    """Build all 12 scenarios for the completed game.

    Returns:
        List of 12 playable scenarios.
    """
    return [
        Scenario(
            title="Exam Night",
            prompt="You have an exam tomorrow, but your friends invite you out.",
            choices=[
                Choice(
                    text="Stay home and study.",
                    result_text="You feel more prepared, but you miss the night out.",
                    immediate_changes={
                        "time": -12,
                        "energy": -8,
                        "money": 0,
                        "reputation": 4,
                    },
                ),
                Choice(
                    text="Go out for a few hours.",
                    result_text="You have fun, but your study time gets cut short.",
                    immediate_changes={
                        "time": -16,
                        "energy": -12,
                        "money": -8,
                        "reputation": 8,
                    },
                    delayed_changes={"reputation": -5, "energy": -4},
                    delayed_rounds=1,
                    delayed_note="The rushed exam hurts your confidence the next day.",
                ),
            ],
        ),
        Scenario(
            title="Extra Work Shift",
            prompt="Your manager offers you an extra shift during a busy school week.",
            choices=[
                Choice(
                    text="Take the shift.",
                    result_text="You earn more money, but your schedule gets tighter.",
                    immediate_changes={
                        "time": -18,
                        "energy": -12,
                        "money": 24,
                        "reputation": 2,
                    },
                    delayed_changes={"energy": -8},
                    delayed_rounds=1,
                    delayed_note="The extra shift leaves you worn out.",
                ),
                Choice(
                    text="Decline the shift.",
                    result_text="You protect your school schedule, but lose extra income.",
                    immediate_changes={
                        "time": 8,
                        "energy": 5,
                        "money": -5,
                        "reputation": 0,
                    },
                ),
            ],
        ),
        Scenario(
            title="Group Project",
            prompt="Your group project has poor communication, and the deadline is close.",
            choices=[
                Choice(
                    text="Take charge and organize the group.",
                    result_text="Your group gets moving, and others respect your effort.",
                    immediate_changes={
                        "time": -14,
                        "energy": -10,
                        "money": 0,
                        "reputation": 15,
                    },
                ),
                Choice(
                    text="Only finish your assigned section.",
                    result_text="You save time, but the group still lacks direction.",
                    immediate_changes={
                        "time": -6,
                        "energy": -4,
                        "money": 0,
                        "reputation": -6,
                    },
                    delayed_changes={"reputation": -8},
                    delayed_rounds=2,
                    delayed_note="The weak group coordination lowers the final grade.",
                ),
            ],
        ),
        Scenario(
            title="Dinner Choice",
            prompt="You need dinner. You are tired and low on time.",
            choices=[
                Choice(
                    text="Cook a simple meal.",
                    result_text="You spend time cooking, but save money and feel better.",
                    immediate_changes={
                        "time": -10,
                        "energy": 8,
                        "money": 7,
                        "reputation": 0,
                    },
                ),
                Choice(
                    text="Order takeout.",
                    result_text="You save time, but spend more money.",
                    immediate_changes={
                        "time": 6,
                        "energy": 2,
                        "money": -16,
                        "reputation": 0,
                    },
                ),
            ],
        ),
        Scenario(
            title="Friend Support",
            prompt="A close friend asks to talk after a rough day.",
            choices=[
                Choice(
                    text="Make time for them.",
                    result_text="Your friend feels supported, and the friendship grows stronger.",
                    immediate_changes={
                        "time": -8,
                        "energy": -6,
                        "money": 0,
                        "reputation": 11,
                    },
                ),
                Choice(
                    text="Tell them you need space tonight.",
                    result_text="You recover some energy, but your friend feels brushed off.",
                    immediate_changes={
                        "time": 6,
                        "energy": 9,
                        "money": 0,
                        "reputation": -5,
                    },
                ),
            ],
        ),
        Scenario(
            title="Club Event",
            prompt="A campus club asks you to help run an event.",
            choices=[
                Choice(
                    text="Volunteer at the event.",
                    result_text="You build connections and help the event succeed.",
                    immediate_changes={
                        "time": -12,
                        "energy": -8,
                        "money": 0,
                        "reputation": 13,
                    },
                ),
                Choice(
                    text="Skip it and work on assignments.",
                    result_text="You make progress on schoolwork, but miss a networking chance.",
                    immediate_changes={
                        "time": 8,
                        "energy": 3,
                        "money": 0,
                        "reputation": -5,
                    },
                ),
            ],
        ),
        Scenario(
            title="Broken Laptop",
            prompt="Your laptop starts crashing while you work on assignments.",
            choices=[
                Choice(
                    text="Pay for a quick repair.",
                    result_text="The repair costs money, but prevents bigger problems.",
                    immediate_changes={
                        "time": 8,
                        "energy": 4,
                        "money": -22,
                        "reputation": 0,
                    },
                ),
                Choice(
                    text="Ignore it for now.",
                    result_text="You avoid paying now, but the issue remains risky.",
                    immediate_changes={
                        "time": -4,
                        "energy": -2,
                        "money": 5,
                        "reputation": 0,
                    },
                    delayed_changes={"time": -15, "energy": -8},
                    delayed_rounds=2,
                    delayed_note="Your laptop crashes during a later assignment.",
                ),
            ],
        ),
        Scenario(
            title="Office Hours",
            prompt="You are confused in a class, and office hours are open today.",
            choices=[
                Choice(
                    text="Go to office hours.",
                    result_text="You get help and show your professor effort.",
                    immediate_changes={
                        "time": -8,
                        "energy": -3,
                        "money": 0,
                        "reputation": 6,
                    },
                    delayed_changes={"energy": 5, "reputation": 5},
                    delayed_rounds=1,
                    delayed_note="The extra help makes the next assignment easier.",
                ),
                Choice(
                    text="Try to figure it out alone.",
                    result_text="You work alone, but lose time and focus.",
                    immediate_changes={
                        "time": -12,
                        "energy": -8,
                        "money": 0,
                        "reputation": 0,
                    },
                ),
            ],
        ),
        Scenario(
            title="Side Project",
            prompt="You have an idea for a small project, but your schedule is full.",
            choices=[
                Choice(
                    text="Start it this week.",
                    result_text="You make progress on something meaningful.",
                    immediate_changes={
                        "time": -15,
                        "energy": -10,
                        "money": 0,
                        "reputation": 8,
                    },
                ),
                Choice(
                    text="Save the idea for later.",
                    result_text="You keep your schedule stable and avoid adding pressure.",
                    immediate_changes={
                        "time": 8,
                        "energy": 6,
                        "money": 0,
                        "reputation": -1,
                    },
                ),
            ],
        ),
        Scenario(
            title="Burnout Warning",
            prompt="You feel worn down after several packed days.",
            choices=[
                Choice(
                    text="Take a full rest night.",
                    result_text="You recover and avoid burning out.",
                    immediate_changes={
                        "time": -5,
                        "energy": 18,
                        "money": 0,
                        "reputation": -2,
                    },
                ),
                Choice(
                    text="Push through more work.",
                    result_text="You finish more work, but your energy drops.",
                    immediate_changes={
                        "time": -12,
                        "energy": -16,
                        "money": 0,
                        "reputation": 7,
                    },
                    delayed_changes={"energy": -10},
                    delayed_rounds=1,
                    delayed_note="Ignoring burnout makes the next day harder.",
                ),
            ],
        ),
        Scenario(
            title="Budget Choice",
            prompt="You want new headphones, but your budget is tight.",
            choices=[
                Choice(
                    text="Buy them now.",
                    result_text="You enjoy the purchase, but lose financial room.",
                    immediate_changes={
                        "time": 0,
                        "energy": 4,
                        "money": -18,
                        "reputation": 0,
                    },
                ),
                Choice(
                    text="Wait until next month.",
                    result_text="You delay the purchase and keep more money saved.",
                    immediate_changes={
                        "time": 0,
                        "energy": -2,
                        "money": 8,
                        "reputation": 0,
                    },
                ),
            ],
        ),
        Scenario(
            title="Final Weekend",
            prompt="The semester is ending. You have one free weekend before finals.",
            choices=[
                Choice(
                    text="Use the weekend to prepare.",
                    result_text="You finish strong and reduce future stress.",
                    immediate_changes={
                        "time": -16,
                        "energy": -8,
                        "money": 0,
                        "reputation": 11,
                    },
                ),
                Choice(
                    text="Use the weekend to reset.",
                    result_text="You recover, but finals prep becomes tighter.",
                    immediate_changes={
                        "time": 5,
                        "energy": 16,
                        "money": 0,
                        "reputation": -3,
                    },
                ),
            ],
        ),
    ]


def apply_choice(game_state: GameState, scenario: Scenario, choice: Choice) -> str:
    """Apply a selected choice to the game state."""
    game_state.apply_changes(choice.immediate_changes)

    if hasattr(game_state, "record_decision"):
        game_state.record_decision(scenario.title, choice.text, choice.result_text)
    elif hasattr(game_state, "add_decision"):
        game_state.add_decision(scenario.title, choice.text, choice.result_text)
    else:
        game_state.history.append(choice.text)

    if choice.delayed_changes:
        game_state.add_pending_effect(
            delay_rounds=choice.delayed_rounds,
            changes=choice.delayed_changes,
            note=choice.delayed_note,
        )

    return choice.result_text
