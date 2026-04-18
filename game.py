import random
from update_stress_level import update_stress_level
from update_relationships import update_relationships
from generate_event import generate_event
from decision_impact import balance_decision_impact  # change if filename differs


# ----------------------------------------------------------
# GLOBAL VARIABLES (FILLED AFTER PLAYER INPUT)
# ----------------------------------------------------------

roommates = {}
stress_level = 30

apartment_status = {
    "broken_items": [],
    "upcoming_bills": ["electricity"],
    "roommate_moods": {}
}

history = []


# ----------------------------------------------------------
# PLAYER ACTIONS
# ----------------------------------------------------------

def choose_action():
    print("\nChoose an action:")
    print("1. Help with chores")
    print("2. Listen to a roommate")
    print("3. Ignore everyone")
    print("4. Argue with someone")

    choice = input("> ").strip()

    if choice == "1":
        return {"type": "help_chores", "target": "all", "magnitude": 1.0}
    if choice == "2":
        return {
            "type": "listen",
            "target": random.choice(list(roommates.keys())),
            "magnitude": 1.0,
        }
    if choice == "3":
        return {"type": "ignore", "target": "all", "magnitude": 1.0}
    if choice == "4":
        return {
            "type": "argue",
            "target": random.choice(list(roommates.keys())),
            "magnitude": 1.0,
        }

    print("Invalid choice — you did nothing this turn.")
    return {"type": "ignore", "target": "all", "magnitude": 1.0}


# ----------------------------------------------------------
# MOOD HELPER
# ----------------------------------------------------------

def update_mood(relationship_score: int) -> str:
    """Return a mood string based on a 0–100 relationship score."""
    if relationship_score <= 25:
        return "tense"
    elif relationship_score <= 60:
        return "neutral"
    else:
        return "happy"


# ----------------------------------------------------------
# STATUS DISPLAY
# ----------------------------------------------------------

def show_status(day, stress_level, roommates):
    print("\n--------------------------------")
    print(f"DAY {day} SUMMARY")
    print("--------------------------------")
    print(f"Your stress level: {stress_level}\n")

    print("Roommate relationships:")
    for name, data in roommates.items():
        print(f"  {name}: {data['relationship']} ({data['mood']})")


# ----------------------------------------------------------
# MAIN GAME LOOP
# ----------------------------------------------------------

def play_game(days=7):
    global stress_level, roommates, apartment_status

    # 1. Player name
    player_name = input("Enter your name: ").strip()
    while not player_name:
        player_name = input("Please enter a valid name: ").strip()

    print("\nName your 3 roommates. You cannot leave any blank.\n")

    # 2. Roommate names (NO DEFAULTS ALLOWED)
    roommate_names = []
    for i in range(1, 4):
        name = input(f"Enter name for roommate #{i}: ").strip()
        while not name:
            name = input("Name cannot be blank. Enter a roommate name: ").strip()
        roommate_names.append(name)

    # 3. Build roommate profiles (0–100 relationship scale)
    roommates = {
        roommate_names[0]: {"relationship": 60, "mood": "neutral", "traits": ["sensitive"]},
        roommate_names[1]: {"relationship": 75, "mood": "happy", "traits": ["chill"]},
        roommate_names[2]: {"relationship": 50, "mood": "tense", "traits": ["messy"]},
    }

    # Set initial moods based on relationship scores
    for name in roommates:
        roommates[name]["mood"] = update_mood(roommates[name]["relationship"])

    apartment_status["roommate_moods"] = {
        name: data["mood"] for name, data in roommates.items()
    }

    print(f"\nWelcome, {player_name}! Your roommates are {', '.join(roommates.keys())}.")
    print("Try to survive the next 7 days without losing your mind.\n")

    # ------------------------------------------------------
    # GAME DAYS
    # ------------------------------------------------------

    for day in range(1, days + 1):
        print(f"\n========== DAY {day} ==========")

        # Player action
        action = choose_action()
        history.append(action)

        # Decision balancing (works on 0–100 relationships)
        balance = balance_decision_impact(action, history, stress_level, roommates)

        # --------------------------------------------------
        # Relationship updates via group function
        # Convert 0–100 → -1..1, call update_relationships,
        # then convert -1..1 → 0–100 again.
        # --------------------------------------------------

        # 1) Build scaled roommates dict for the algorithm
        scaled_roommates = {}
        for name, info in roommates.items():
            rel_0_100 = info["relationship"]
            rel_scaled = (rel_0_100 - 50) / 50.0      # 0→-1, 50→0, 100→1
            rel_scaled = max(-1.0, min(1.0, rel_scaled))

            scaled_roommates[name] = {
                **info,
                "relationship": rel_scaled,
            }

        # 2) Call the group's algorithm on the scaled relationships
        scaled_updated = update_relationships(scaled_roommates, action, history)

        # 3) Convert back to 0–100 and store into roommates
        for name, info in scaled_updated.items():
            rel_scaled = info["relationship"]
            rel_0_100 = int(round(rel_scaled * 50 + 50))  # -1→0, 0→50, 1→100
            rel_0_100 = max(0, min(100, rel_0_100))

            roommates[name]["relationship"] = rel_0_100
            roommates[name]["traits"] = info.get("traits", roommates[name]["traits"])

        # Apply balancing relationship effects (on 0–100 scale)
        for name, delta in balance["relationship_deltas"].items():
            roommates[name]["relationship"] += delta
            roommates[name]["relationship"] = max(
                0, min(100, roommates[name]["relationship"])
            )

        # Update moods based on new relationship scores
        for name in roommates:
            roommates[name]["mood"] = update_mood(roommates[name]["relationship"])

        # Keep apartment mood dictionary in sync
        apartment_status["roommate_moods"] = {
            name: data["mood"] for name, data in roommates.items()
        }

        # Stress update
        sleep_hours = random.randint(4, 9)
        conflicts_today = [random.randint(1, 4)] if action["type"] == "argue" else []
        chores_done = action["type"] == "help_chores"

        stress_level = update_stress_level(
            stress=stress_level,
            sleep_hours=sleep_hours,
            conflicts=conflicts_today,
            chores_done=chores_done,
        )

        stress_level += balance["stress_delta"]
        stress_level = max(0, min(100, stress_level))

        # Build simple relationship dict for events (still 0–100)
        relationships_for_event = {
            name: data["relationship"] for name, data in roommates.items()
        }

        # Random event
        event = generate_event(day, stress_level, relationships_for_event, apartment_status)
        print(f"\nRandom Event Today: {event['event']}")
        print(event["description"])

        # Show daily status
        show_status(day, stress_level, roommates)

        # Lose conditions
        if stress_level >= 100:
            print(f"\n{player_name}, your stress maxed out. You couldn't survive the semester.")
            return

        if any(info["relationship"] <= 0 for info in roommates.values()):
            print(f"\n{player_name}, one of your roommates has had enough. You must move out.")
            return

    print(f"\nYou survived the week, {player_name}! Congrats.")


# ----------------------------------------------------------
# RUN GAME
# ----------------------------------------------------------

if __name__ == "__main__":
    play_game()


if __name__ == "__main__":
    play_game()