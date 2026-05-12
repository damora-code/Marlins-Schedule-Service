from fastapi import APIRouter, Query

from app.utils.dates import resolve_date
from app.services.mlb_api import get_affiliates, get_schedule, get_live_feed
from app.services.schedule_service import (
    extract_affiliate_teams, 
    build_team_schedule_response)
from app.utils.game_state import normalize_game_state


router = APIRouter()


@router.get("/schedule")
async def get_schedule_route(date: str | None = Query(default=None)):
    resolved_date = resolve_date(date)

    affiliates = await get_affiliates()

    affiliate_teams = extract_affiliate_teams(affiliates)

    sport_ids = list({
        team["sport_id"]
        for team in affiliate_teams
    })

    team_ids = [
        team["team_id"]
        for team in affiliate_teams]

    schedule_data = await get_schedule(
        sport_ids=sport_ids,
        team_ids=team_ids,
        date=resolved_date
    )
    
    games = schedule_data.get("dates", [{}])[0].get("games", [])

    live_feeds = {}

    for game in games:
        raw_state = game.get("status", {}).get("detailedState", "")
        state = normalize_game_state(raw_state)

    if state == "In Progress":
        game_pk = game.get("gamePk")
        live_feeds[game_pk] = await get_live_feed(game_pk)


    #transformer
    transformed_schedule = build_team_schedule_response(
        affiliate_teams=affiliate_teams,
        schedule_payload=schedule_data,
        live_feeds=live_feeds
    )

    return {
        "date": resolved_date,
        "teams": transformed_schedule
    }
