def update_stress_level(stress, sleep_hours, conflicts, chores_done):
    """
    Update the player's stress level for one day.

    Parameters:
        stress (int): Current stress level (0–100).
        sleep_hours (int): Hours of sleep the player got (0–12).
        conflicts (list): Conflict intensities throughout the day (e.g., [3, 5, 1]).
        chores_done (bool): Whether the player completed their chores today.

    Returns:
        int: The updated stress level (0–100).
    """

  
    if sleep_hours >= 8:
        stress -= 10
    elif sleep_hours >= 5:
        stress -= 5
    else:
        stress += 10

    for intensity in conflicts:
        stress += intensity

    if not chores_done:
        stress += 5

    stress = max(0, min(100, stress))

    return stress
