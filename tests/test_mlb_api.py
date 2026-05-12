from app.services.mlb_api import build_schedule_url


def test_build_schedule_url_includes_sport_ids_team_ids_and_date():
    url = build_schedule_url(
        sport_ids=[1, 11, 12],
        team_ids=[146, 564, 479],
        date="2026-05-12"
    )

    assert "sportId=1,11,12" in url
    assert "teamId=146,564,479" in url
    assert "date=2026-05-12" in url
    assert "hydrate=probablePitcher,decisions" in url