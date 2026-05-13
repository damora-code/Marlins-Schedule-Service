from app.services.schedule_service import (
    extract_affiliate_teams,
    find_game_for_team,
    build_team_schedule_response,
)


def test_extract_affiliate_teams_excludes_non_playable_org_entries():
    payload = {
        "teams": [
            {
                "id": 146,
                "name": "Miami Marlins",
                "sport": {"id": 1, "name": "Major League Baseball"}
            },
            {
                "id": 3277,
                "name": "Marlins Organization",
                "sport": {"id": 11, "name": "Minor League Baseball"}
            }
        ]
    }

    teams = extract_affiliate_teams(payload)

    assert len(teams) == 1
    assert teams[0]["team_id"] == 146


def test_find_game_for_team_returns_matching_game():
    games = [
        {
            "gamePk": 123,
            "teams": {
                "away": {"team": {"id": 146}},
                "home": {"team": {"id": 142}}
            }
        }
    ]

    game = find_game_for_team(146, games)

    assert game["gamePk"] == 123


def test_find_game_for_team_returns_none_when_no_game():
    games = [
        {
            "gamePk": 123,
            "teams": {
                "away": {"team": {"id": 100}},
                "home": {"team": {"id": 200}}
            }
        }
    ]

    assert find_game_for_team(146, games) is None


def test_build_response_returns_empty_object_when_team_has_no_game():
    affiliate_teams = [
        {
            "team_id": 619,
            "sport_id": 16,
            "team_name": "DSL Marlins",
            "level": "Rookie"
        }
    ]

    schedule_payload = {
        "dates": [
            {
                "games": []
            }
        ]
    }

    response = build_team_schedule_response(affiliate_teams, schedule_payload)

    assert response == [
        {
            "619": {}
        }
    ]