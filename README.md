# Marlins Schedule Service

## Overview

The Marlins Schedule Service is a FastAPI backend service that provides a single `/schedule` endpoint for viewing Miami Marlins and affiliate team schedules/results for a given calendar date.

The service acts as an abstraction layer over MLB Stats API. It first retrieves the Marlins organization’s affiliate teams, extracts the required `sportId` and `teamId` values, requests schedule data for the selected date, and transforms the MLB response into a frontend-friendly format keyed by team ID.

The endpoint accepts an optional `date` query parameter in `YYYY-MM-DD` format. If no date is provided, the service defaults to the current date.

The response includes:
- An empty object for affiliate teams without a game on the selected date
- Not Started game details: game time, opponent, venue, and probable pitchers when available
- In Progress game details: opponent, venue, score, inning, outs, runners, current pitcher, and batter when available
- Completed game details: final score, winning pitcher, losing pitcher, and save pitcher when applicable

--- 

## Features
- Single `/schedule` endpoint for retrieving Miami Marlins and affiliate schedules/results
- Optional `date` query parameter in `YYYY-MM-DD` format
- Defaults to the current date when no date parameter is provided
- Automatic affiliate discovery using MLB Stats API
- Aggregates MLB and affiliate schedules into a single normalized response
- State-specific game response formatting:
  - Not Started
  - In Progress
  - Completed
- Returns empty objects for affiliates without games on the selected date
- Includes probable pitchers when available from MLB Stats API
- Includes completed game decisions:
  - Winning pitcher
  - Losing pitcher
  - Save pitcher
- Separation of concerns between:
  - API routes
  - MLB API communication
  - Transformation logic
  - Utility helpers
- Automated tests using `pytest`
- Interactive API documentation provided by FastAPI Swagger UI

---

## Tech Stack
- Python 3.12
- FastAPI
- Uvicorn
- HTTPX
- Pytest

--- 
## Project Structure
```text
app/
├── api/
│   └── routes.py
├── services/
│   ├── mlb_api.py
│   └── schedule_service.py
├── utils/
│   ├── dates.py
│   └── game_state.py
├── main.py

tests/
├── test_dates.py
├── test_mlb_api.py
├── test_schedule_service.py
```


## Directory Overview
- `api/`
    - FastAPI route definitions and endpoint handlers
- `services/`
    - External MLB API communication and schedule transformation logic
- `utils/`
    - Shared utility helpers for validation and game state normalization
- `tests/`
    - Automated unit tests for validation, URL construction, and response transformation

---

## Setup Instructions
- Python 3.12+
- pip
- virtual environment support (`venv`)

### Clone the Repository

```bash
git clone <repository-url>
cd marlins-schedule-service
```

### Create and Activate a Virtual Environment
#### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
#### Windows (Git Bash)
```bash
python -m venv venv
source venv/Scripts/activate
```
#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```
---

## API Usage
### Get Today's Schedule

```http
GET /schedule
```

Example:

```text
http://127.0.0.1:8000/schedule
```

---

### Get Schedule for a Specific Date

```http
GET /schedule?date=YYYY-MM-DD
```

Example:

```text
http://127.0.0.1:8000/schedule?date=2026-05-06
```

---

### Invalid Date Format

If an invalid date format is provided, the service returns:

```json
{
  "detail": "Invalid date format. Expected YYYY-MM-DD."
}
```

---

## Example Response
Example:
```text
http://127.0.0.1:8000/schedule?date=2026-05-06
```

```json
{
  "date": "2026-05-06",
  "teams": [
    {
      "146": {
        "teamName": "Miami Marlins",
        "level": "Major League Baseball",
        "state": "Completed",
        "finalScore": {
          "away": {
            "team": "Baltimore Orioles",
            "runs": 7
          },
          "home": {
            "team": "Miami Marlins",
            "runs": 4
          }
        },
        "winningPitcher": {
          "id": 687064,
          "name": "Brandon Young"
        },
        "losingPitcher": {
          "id": 691587,
          "name": "Eury Pérez"
        },
        "savePitcher": {
          "id": 670329,
          "name": "Rico Garcia"
        }
      }
    },
    {
      "467": {

      }
    },
    {
      "564": {
        "teamName": "Jacksonville Jumbo Shrimp",
        "level": "Triple-A",
        "state": "Completed",
        "finalScore": {
          "away": {
            "team": "Charlotte Knights",
            "runs": 6
          },
          "home": {
            "team": "Jacksonville Jumbo Shrimp",
            "runs": 7
          }
        },
        "winningPitcher": {
          "id": 676604,
          "name": "Tyler Zuber"
        },
        "losingPitcher": {
          "id": 803035,
          "name": "Riley Gowens"
        },
        "savePitcher": null
      }
    },
    {
      "554": {
        "teamName": "Beloit Sky Carp",
        "level": "High-A",
        "state": "Completed",
        "finalScore": {
          "away": {
            "team": "Beloit Sky Carp",
            "runs": 0
          },
          "home": {
            "team": "Fort Wayne TinCaps",
            "runs": 5
          }
        },
        "winningPitcher": {
          "id": 702584,
          "name": "Isaiah Lowe"
        },
        "losingPitcher": {
          "id": 830894,
          "name": "Carson Laws"
        },
        "savePitcher": null
      }
    },
    {
      "619": {

      }
    },
    {
      "4124": {
        "teamName": "Pensacola Blue Wahoos",
        "level": "Double-A",
        "state": "Completed",
        "finalScore": {
          "away": {
            "team": "Rocket City Trash Pandas",
            "runs": 10
          },
          "home": {
            "team": "Pensacola Blue Wahoos",
            "runs": 1
          }
        },
        "winningPitcher": {
          "id": 683681,
          "name": "Jose Gonzalez"
        },
        "losingPitcher": {
          "id": 677354,
          "name": "Alex Williams"
        },
        "savePitcher": null
      }
    },
    {
      "479": {
        "teamName": "Jupiter Hammerheads",
        "level": "Single-A",
        "state": "Completed",
        "finalScore": {
          "away": {
            "team": "Palm Beach Cardinals",
            "runs": 0
          },
          "home": {
            "team": "Jupiter Hammerheads",
            "runs": 1
          }
        },
        "winningPitcher": {
          "id": 806466,
          "name": "Braulio Salas"
        },
        "losingPitcher": {
          "id": 834989,
          "name": "Kaden Echeman"
        },
        "savePitcher": null
      }
    },
    {
      "2127": {

      }
    }
  ]
}
```

---
## Testing

The project includes automated unit tests using `pytest`.

The current test suite focuses on validation logic and deterministic transformation behavior that can be tested independently from live MLB game availability.

### Run Tests

```bash
pytest
```

---

### Current Test Coverage

The automated tests currently validate:

- Date validation logic
- Invalid date handling
- MLB schedule URL generation
- Affiliate extraction logic
- Team/game matching
- Empty game response handling
- Response transformation behavior

Example successful test execution:

```text
================== 8 passed in 0.22s ==================
```

---

## Assumptions

- The service is designed specifically for the Miami Marlins organization and its affiliates using MLB team ID `146`.

- Affiliate teams are dynamically retrieved from MLB Stats API rather than hardcoded into the application.

- Organizational/non-playable entries returned by the affiliate endpoint (such as alternate training sites or organizational placeholders) are excluded from the response.

- Dominican Summer League (DSL) affiliates are retained in the response even when no game exists for the selected date.

- If an affiliate team does not have a scheduled game for the requested date, the response returns an empty object for that team ID as specified in the requirements.

- Probable pitchers are included only when available from MLB Stats API. Some games and levels of competition may not provide probable pitcher information.

- Save pitchers are returned only when a save is officially awarded for the completed game.

- The service assumes MLB Stats API availability and does not currently implement caching, retries, or rate limiting.

- In-progress game data is enriched using MLB live feed endpoints when a game is currently live.

- Dates are expected in `YYYY-MM-DD` format and are interpreted using the server’s local date context when omitted.

- Game states outside the three primary required states, such as postponed games or manager challenges, are returned with their source state so the frontend can handle them explicitly.

## Design Decisions

- The service uses FastAPI to align with the backend stack discussed during the interview process.

- The `/schedule` route is kept intentionally thin. Request handling, MLB API communication, and response transformation are separated into dedicated modules.

- MLB Stats API communication is isolated in `mlb_api.py` so external API details are not mixed into route or transformation logic.

- Schedule transformation logic is handled in `schedule_service.py` to keep the response formatting easy to test and maintain.

- The response is returned as a list of team-ID-keyed objects to match the requested response format.

- Game responses are built conditionally based on normalized game state:
  - `Not Started`
  - `In Progress`
  - `Completed`

- Missing optional data from MLB Stats API is returned as `null` rather than causing the request to fail.

- Teams without games return an empty object, matching the functional requirements.

- Utility functions are used for date validation and game state normalization to keep reusable logic outside the route layer.

- Tests focus on business logic that can be validated without depending on live MLB game availability.

---

## Future Improvements

- Expand live game handling for additional edge cases such as delays, postponed games, or unavailable live-feed data.

- Add caching for affiliate and schedule responses to reduce repeated calls to MLB Stats API.

- Add retry and timeout handling for external MLB API requests.

- Add structured logging for debugging and monitoring.

- Add Pydantic response models for stronger response validation and improved API documentation.

- Add integration tests for the `/schedule` endpoint.

- Add mocked live-feed tests for in-progress game scenarios.

- Add Docker support for consistent local and deployment environments.

- Add configurable season/year values instead of using a fixed `2026` season.

- Add optional support for other MLB organizations if the service needs to expand beyond the Marlins.
