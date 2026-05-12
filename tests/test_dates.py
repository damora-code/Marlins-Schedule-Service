import pytest
from fastapi import HTTPException

from app.utils.dates import resolve_date

def test_resolve_date_returns_given_valid_date():
    assert resolve_date("2026-05-12") == "2026-05-12"
    
def test_resolve_date_rejects_invalid_date_format():
    with pytest.raises(HTTPException) as exc:
        resolve_date("05-12-2026")

    assert exc.value.status_code == 400