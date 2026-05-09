"""Tests for the completed Tradeoffs project."""

from game_state import GameState
from scenarios import apply_choice, build_scenarios
from scoring import build_final_summary, calculate_balance_score, get_rating


def test_game_has_exactly_12_scenarios():
    scenarios = build_scenarios()

    assert len(scenarios) == 12


def test_each_scenario_has_two_choices():
    scenarios = build_scenarios()

    for scenario in scenarios:
        assert len(scenario.choices) == 2


def test_resources_clamp_between_0_and_100():
    game_state = GameState(time=95, energy=5)

    game_state.apply_changes({"time": 20, "energy": -20})

    assert game_state.time == 100
    assert game_state.energy == 0


def test_delayed_effect_triggers_on_future_round():
    game_state = GameState()

    game_state.add_pending_effect(1, {"energy": -10}, "test delay")
    game_state.next_round()
    messages = game_state.resolve_pending_effects()

    assert game_state.energy == 50
    assert messages == ["test delay"]


def test_apply_choice_records_history():
    game_state = GameState()
    scenario = build_scenarios()[0]
    choice = scenario.choices[0]

    apply_choice(game_state, scenario, choice)

    assert len(game_state.history) == 1
    assert game_state.history[0].scenario_title == scenario.title


def test_apply_choice_schedules_delayed_effect():
    game_state = GameState()
    scenario = build_scenarios()[0]
    choice = scenario.choices[1]

    apply_choice(game_state, scenario, choice)

    assert len(game_state.pending_effects) == 1


def test_score_stays_in_range():
    game_state = GameState(time=100, energy=0, money=60, reputation=60)
    score = calculate_balance_score(game_state)

    assert 0 <= score <= 100


def test_rating_values():
    assert get_rating(90) == "Excellent"
    assert get_rating(72) == "Strong"
    assert get_rating(57) == "Stable"
    assert get_rating(42) == "Risky"
    assert get_rating(10) == "Unstable"


def test_final_summary_contains_expected_keys():
    game_state = GameState()
    summary = build_final_summary(game_state)

    assert "score" in summary
    assert "rating" in summary
    assert "play_style" in summary
    assert "warnings" in summary
    assert "final_stats" in summary
