def balance_decision_impact(action, history, stress_level, roommates):
    """
    Balance the impact of the current decision so that repeated strategies
    have diminishing returns and risky choices have extra trade-offs.

    Parameters:
        action (dict): Current action, e.g. {"type": "help_chores", "target": "Mike", "magnitude": 1.0}
        history (list): List of previous actions (each an action dict).
        stress_level (int): Current stress level before applying today's effects (0–100).
        roommates (dict): Roommate data with relationship scores, e.g.
                          {
                              "Mike": {"relationship": 60, "mood": "neutral"},
                              "Riley": {"relationship": 75, "mood": "happy"}
                          }

    Returns:
        dict: {
            "stress_delta": int,
            "relationship_deltas": {roommate_name: int, ...}
        }
    """

    # Start with no extra impact
    stress_delta = 0
    relationship_deltas = {name: 0 for name in roommates}

    # 1. Detect repeated strategies ("grinding"):
    #    If the same action type is used 3 times in a row, add a small penalty.
    recent_actions = history[-3:]  # last up to 3 actions
    same_type_count = 0
    for past_action in recent_actions:
        if past_action.get("type") == action.get("type"):
            same_type_count += 1

    if same_type_count >= 3:
        # Repeating the same choice too much feels less effective
        stress_delta += 5
        for name in relationship_deltas:
            relationship_deltas[name] -= 1

    # 2. If stress is very high and the player chooses to argue,
    #    make the consequences harsher.
    if stress_level > 80 and action.get("type") == "argue":
        stress_delta += 10
        target = action.get("target")
        if target in relationship_deltas:
            relationship_deltas[target] -= 5

    # 3. If average relationships are low and the player chooses something positive,
    #    give a small bonus so recovery feels fair.
    total_relationship = 0
    for data in roommates.values():
        total_relationship += data.get("relationship", 0)

    avg_relationship = total_relationship / len(roommates) if roommates else 0

    if avg_relationship < 40 and action.get("type") in ("help_chores", "listen"):
        stress_delta -= 3
        for name in relationship_deltas:
            relationship_deltas[name] += 3

    return {
        "stress_delta": stress_delta,
        "relationship_deltas": relationship_deltas
    }
