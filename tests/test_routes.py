from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_schedule_endpoint_rejects_invalid_date():
    response = client.get("/schedule?date=invalid-date")

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid date format. Expected YYYY-MM-DD."
    }