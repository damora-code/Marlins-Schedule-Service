def normalize_game_state(state: str) -> str:
    """
    Normalizes the game state string to the format required
    """

    if state in ["Scheduled", "Pre-Game", "Preview"]:
        return "Not Started"

    if state in ["In Progress","Manager Challenge"]:
        return "In Progress"

    if state == "Final":
        return "Completed"
    
    if state in ["Postponed", "Suspended", "Cancelled"]:
        return state

    return state
