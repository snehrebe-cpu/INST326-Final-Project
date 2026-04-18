import random

def generate_event(day, stress_level, relationship_tracker, apartment_status):
    """
    Generates a random, context-aware event based on the current game state.

    Parameters:
    - day (int): Current day in the semester.
    - stress_level (int): Player's current stress level (0–100).
    - relationship_scores (dict): Mapping of roommate names to relationship scores (0–100).
    - apartment_status (dict): Dictionary with keys like 'broken_items', 'upcoming_bills', 'roommate_moods'.

    Returns:
    - dict: A dictionary describing the selected event and its impact.
    """

    base_events = [
        {"name": "surprise_guest", 
         "trigger": lambda s: s < 60},

        {"name": "roommate_birthday", 
         "trigger": lambda s: True},

        {"name": "appliance_breaks", 
         "trigger": lambda s: "fridge" not in apartment_status.get("broken_items", [])},

        {"name": "bill_due", 
         "trigger": lambda s: day % 7 == 0},

        {"name": "roommate_argument", 
         "trigger": lambda s: any(score < 40 for score in relationship_tracker.values())},

        # NEW EVENT 1
        {"name": "unexpected_inspection",
         "trigger": lambda s: s > 40 or apartment_status.get("broken_items")},

        # NEW EVENT 2
        {"name": "group_movie_night",
         "trigger": lambda s: all(score > 50 for score in relationship_tracker.values())}
    ]

    # Collect valid events based on triggers
    valid_events = []
    for event in base_events:
        if event["trigger"](stress_level):
            valid_events.append(event["name"])

    if not valid_events:
        return {"event": "quiet_day", "description": "Nothing unusual happened today."}

    selected_event = random.choice(valid_events)

    # Event descriptions
    if selected_event == "surprise_guest":
        description = "A friend unexpectedly drops by. Roommates react based on their mood."

    elif selected_event == "roommate_birthday":
        description = "It's one roommate's birthday. Time to celebrate or forget—your choice matters."

    elif selected_event == "appliance_breaks":
        description = "The fridge breaks down. Who will fix it?"

    elif selected_event == "bill_due":
        description = "Rent is due today. Time to split the bill."

    elif selected_event == "roommate_argument":
        description = "Two roommates get into a heated argument. You’re caught in the middle."

    elif selected_event == "unexpected_inspection":
        description = "A sudden housing inspection is announced. Everyone scrambles to clean up."

    elif selected_event == "group_movie_night":
        description = "Roommates suggest a movie night. It could bring everyone closer… or lead to arguments over what to watch."

    else:
        description = "Nothing unusual happened today."

    return {
        "event": selected_event,
        "description": description,
        "day": day,
        "stress_level": stress_level,
        "relationship_tracker": relationship_tracker
    }


# Mock input for testing
day = 14
stress_level = 65
relationship_trackers = {
    "Jordan": 45,
    "Riley": 30,
    "Casey": 70
}
apartment_status = {
    "broken_items": ["sink"],
    "upcoming_bills": ["internet"],
    "roommate_moods": {"Jordan": "tense", "Riley": "happy", "Casey": "neutral"}
}

event = generate_event(day, stress_level, relationship_trackers, apartment_status)
print(event)
