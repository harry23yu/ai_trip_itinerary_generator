from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class TripContext(BaseModel):
    mode: Literal["explore", "known_trip"]

    destination: Optional[str] = None
    days: Optional[int] = Field(None, ge=1, le=30)
    people: Optional[int] = Field(None, ge=1)

    weather_preferences: Optional[List[str]] = None
    interests: Optional[List[str]] = None

    budget_concern: Optional[bool] = None
    budget_amount: Optional[int] = None

    lodging_area: Optional[str] = None
    food_interest: Optional[bool] = None
    shopping_interest: Optional[bool] = None

    time_preference: Optional[List[Literal["day", "evening", "night"]]] = None
    schedule_style: Optional[Literal["packed", "relaxed"]] = None

    trip_purpose: Optional[str] = None
    must_do: Optional[List[str]] = None