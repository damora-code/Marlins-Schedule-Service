from datetime import datetime
from fastapi import HTTPException


def resolve_date(date_str: str | None) -> str:
    """
    Resolves and validates the incoming date parameter
    If no date is provided, the function defaults to today's date
    Expected date format is YYYY-MM-DD 
    If the format is invalid, an HTTP 400 error is raised
    """

    if date_str is None:
        return datetime.now().strftime("%Y-%m-%d")

    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Expected YYYY-MM-DD.")
