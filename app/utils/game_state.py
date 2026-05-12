def normalize_game_state(state: str) -> str:
    """
    Normalizes the game state string to the format required
    """

    if state in ["Scheduled", "Pre-Game"]:
        return "Not Started"

    if state == "In Progress":
        return "In Progress"

    if state == "Final":
        return "Completed"

    return state
