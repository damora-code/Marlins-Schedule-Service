from app.utils.game_state import normalize_game_state

# exclude names that aren't relevant for the schedule response
EXCLUDED_TEAM_NAMES = {
    "Miami Marlins Prospects",
    "Marlins Alternate Training Site",
    "Marlins Organization",
}


def extract_affiliate_teams(affiliates_payload: dict) -> list[dict]:
    """
    Extracts affiliate team information from the MLB API response
    """

    teams = affiliates_payload.get("teams", [])

    affiliate_teams = []

    for team in teams:
        team_id = team.get("id")
        sport_id = team.get("sport", {}).get("id")
        team_name = team.get("name")
        level = team.get("sport", {}).get("name")

        if team_name in EXCLUDED_TEAM_NAMES:
            continue

        if not team_id or not sport_id:
            continue

        affiliate_teams.append({
            "team_id": team_id,
            "sport_id": sport_id,
            "team_name": team_name,
            "level": level,
        })

    return affiliate_teams


def get_games_from_schedule(schedule_payload: dict) -> list[dict]:
    """
    Extract game information from the MLB API schedule response
    """

    dates = schedule_payload.get("dates", [])

    if not dates:
        return []

    return dates[0].get("games", [])


def find_game_for_team(team_id: int, games: list[dict]) -> dict | None:
    """
    Find the game for a specific team ID from the list of games
    """

    for game in games:
        away_id = game.get("teams", {}).get(
            "away", {}).get("team", {}).get("id")
        home_id = game.get("teams", {}).get(
            "home", {}).get("team", {}).get("id")

        if team_id in [away_id, home_id]:
            return game

    return None


def get_opponent(team_id: int, game: dict) -> dict:
    """
    Get opponent team information for a specific team ID from the game data
    """

    teams = game.get("teams", {})

    away = teams.get("away", {}).get("team", {})
    home = teams.get("home", {}).get("team", {})

    if away.get("id") == team_id:
        return home

    return away


def build_team_schedule_response(affiliate_teams: list[dict], schedule_payload: dict, live_feeds: dict[int, dict] | None = None) -> list[dict]:
    """
    Build a response containing team and game information for the specified affiliate teams and schedule data
    """

    games = get_games_from_schedule(schedule_payload)
    response = []
    live_feeds = live_feeds or {}

    for team in affiliate_teams:
        team_id = team["team_id"]
        game = find_game_for_team(team_id, games)

        if not game:
            response.append({
                str(team_id): {}
            })
            continue

        game_pk = game.get("gamePk")
        live_feed = live_feeds.get(game_pk)

        game_details = build_game_details(team_id, game, live_feed)

        response.append({
            str(team_id): {
                "teamName": team["team_name"],
                "level": team["level"],
                **game_details,
            }
        })
    return response


def get_team_side(team_id: int, game: dict) -> str:
    """
    Determines if the specified team is the home or away team in the given game data
    """

    away_id = game.get("teams", {}).get("away", {}).get("team", {}).get("id")
    return "away" if away_id == team_id else "home"


def get_score(game: dict) -> dict:
    """
    Extracts the current score for both teams from the game data
    """

    away = game.get("teams", {}).get("away", {})
    home = game.get("teams", {}).get("home", {})

    return {
        "away": {
            "team": away.get("team", {}).get("name"),
            "runs": away.get("score"),
        },
        "home": {
            "team": home.get("team", {}).get("name"),
            "runs": home.get("score"),
        }
    }


def build_pitcher(pitcher: dict | None) -> dict | None:
    """
    Extracts the pitcher's name from the pitcher data
    """

    if not pitcher:
        return None

    return {
        "id": pitcher.get("id"),
        "name": pitcher.get("fullName")
    }


def build_probable_pitchers(game: dict) -> dict:
    """
    Extracts the probable pitchers for both teams from the game data
    """

    teams = game.get("teams", {})

    return {
        "away": build_pitcher(
            teams.get("away", {}).get("probablePitcher")),
        "home": build_pitcher(
            teams.get("home", {}).get("probablePitcher"))
    }


def build_not_started_game(team_id: int, game: dict) -> dict:
    """
    Builds a response for a game that has not started yet, including Game time, opponent, venue, and probable pitchers
    """
    opponent = get_opponent(team_id, game)

    return {
        "state": "Not Started",
        "gameTime": game.get("gameDate"),
        "opponent": {
            "id": opponent.get("id"),
            "name": opponent.get("name"),
            "parentClub": None
        },
        "venue": game.get("venue", {}).get("name"),
        "probablePitchers": build_probable_pitchers(game)
    }


def get_live_game_details(live_feed: dict | None) -> dict:
    if not live_feed:
        return {
            "inning": None,
            "outs": None,
            "runnersOnBase": [],
            "currentPitcher": None,
            "batterUp": None,
        }

    live_data = live_feed.get("liveData", {})
    linescore = live_data.get("linescore", {})
    plays = live_data.get("plays", {})
    current_play = plays.get("currentPlay", {})
    matchup = current_play.get("matchup", {})

    offense = linescore.get("offense", {})

    runners = []

    for base in ["first", "second", "third"]:
        runner = offense.get(base)

        if runner:
            runners.append({
                "base": base,
                "id": runner.get("id"),
                "name": runner.get("fullName")
            })

    return {
        "inning": {
            "number": linescore.get("currentInning"),
            "half": linescore.get("inningHalf")
        },
        "outs": linescore.get("outs"),
        "runnersOnBase": runners,
        "currentPitcher": build_pitcher(matchup.get("pitcher")),
        "batterUp": build_pitcher(matchup.get("batter")),
    }


def build_in_progress_game(team_id: int, game: dict, live_feed: dict | None = None) -> dict:
    """
    Builds a response for a game that is currently in progress, including Opponent, venue, current score, inning, outs, runners on base, current pitcher, and batter up-to-bat
    """

    opponent = get_opponent(team_id, game)
    live_details = get_live_game_details(live_feed)

    return {
        "state": "In Progress",
        "opponent": {
            "id": opponent.get("id"),
            "name": opponent.get("name"),
            "parentClub": None
        },
        "venue": game.get("venue", {}).get("name"),
        "score": get_score(game),
        **live_details
    }


def build_completed_game(team_id: int, game: dict) -> dict:
    """
    Builds a response for a game that has completed, including Final score, winning pitcher, losing pitcher, and save pitcher
    """

    decisions = game.get("decisions", {})

    return {
        "state": "Completed",
        "finalScore": get_score(game),
        "winningPitcher": build_pitcher(decisions.get("winner")),
        "losingPitcher": build_pitcher(decisions.get("loser")),
        "savePitcher": build_pitcher(decisions.get("save"))
    }


def build_game_details(team_id: int, game: dict, live_feed: dict | None = None) -> dict:
    """
    Builds a response containing detailed game information based on the game state for the specified team ID and game data
    """

    raw_state = game.get("status", {}).get("detailedState", "")
    state = normalize_game_state(raw_state)

    if state == "Not Started":
        return build_not_started_game(team_id, game)
    if state == "In Progress":
        return build_in_progress_game(team_id, game, live_feed)
    if state == "Completed":
        return build_completed_game(team_id, game)

    return {
        "state": state
    }
