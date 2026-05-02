"""Basic tests for the Tradeoffs draft project."""

from game_state import GameState
from scenarios import apply_choice, build_scenarios
from scoring import build_final_summary, calculate_balance_score


def test_apply_changes_clamps_stats():
    state = GameState(time=95)
    state.apply_changes({"time": 20}, "test increase")
    assert state.time == 100

    state.apply_changes({"time": -200}, "test decrease")
    assert state.time == 0


def test_delayed_effect_triggers_later():
    state = GameState()
    state.add_pending_effect(1, {"energy": -10}, "tired later")

    assert state.energy == 60
    state.next_round()
    notes = state.resolve_pending_effects()

    assert state.energy == 50
    assert notes == ["tired later"]


def test_scenarios_exist():
    scenarios = build_scenarios()

    assert len(scenarios) == 12
    assert len(scenarios[0].choices) == 2


def test_apply_choice_updates_state():
    state = GameState()
    scenario = build_scenarios()[0]
    choice = scenario.choices[0]

    apply_choice(state, choice)

    assert state.time < 60
    assert len(state.history) == 1


def test_score_is_in_range():
    state = GameState()
    score = calculate_balance_score(state)

    assert 0 <= score <= 100


def test_final_summary_has_expected_keys():
    state = GameState()
    summary = build_final_summary(state)

    assert "score" in summary
    assert "rating" in summary
    assert "final_stats" in summary
    assert "warnings" in summary
