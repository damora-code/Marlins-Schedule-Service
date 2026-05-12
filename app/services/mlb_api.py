import httpx

BASE_URL = "https://statsapi.mlb.com/api/v1"


async def get_affiliates():
    """
    Fetches affiliate teams for the specified team IDs and year
    """

    url = f"{BASE_URL}/teams/affiliates?teamIds=146&year=2026"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        response.raise_for_status()

        return response.json()


async def get_schedule(
    sport_ids: list[int],
    team_ids: list[int],
    date: str
):
    """
    Fetches schedule for the specified sport IDs, team IDs, and date.
    """

    url = build_schedule_url(sport_ids, team_ids, date)

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        response.raise_for_status()

        return response.json()


async def get_live_feed(game_pk: int):
    url = f"{BASE_URL}.1/game/{game_pk}/feed/live"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


def build_schedule_url(
    sport_ids: list[int],
    team_ids: list[int],
    date: str
) -> str:
    sport_id_string = ",".join(map(str, sport_ids))
    team_id_string = ",".join(map(str, team_ids))

    return (
        f"{BASE_URL}/schedule"
        f"?sportId={sport_id_string}"
        f"&teamId={team_id_string}"
        f"&date={date}"
        f"&hydrate=probablePitcher,decisions"
    )
