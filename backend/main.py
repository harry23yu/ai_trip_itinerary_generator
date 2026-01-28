import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI(title="AI Trip Itinerary Generator")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ---------- Models ----------

from typing import Optional, List, Literal

class TripContext(BaseModel):
    mode: Literal["explore", "known_trip"]

    destination: Optional[str] = Field(None, example="Tokyo, Japan")
    days: Optional[int] = Field(None, ge=1, le=30)
    people: Optional[int] = Field(None, ge=1)

    interests: Optional[List[str]] = None
    weather_preferences: Optional[List[str]] = None

    budget_concern: Optional[bool] = None
    budget_amount: Optional[int] = None

    lodging_area: Optional[str] = None
    food_interest: Optional[bool] = None
    shopping_interest: Optional[bool] = None

    schedule_style: Optional[Literal["packed", "relaxed"]] = None
    time_preference: Optional[List[Literal["day", "evening", "night"]]] = None

    trip_purpose: Optional[str] = None
    must_do: Optional[List[str]] = None

class TripResponse(BaseModel):
    itinerary: str

# ---------- Prompt ----------

def build_prompt(ctx: TripContext) -> str:
    return f"""
You are an expert travel planner.

Create the best possible travel itinerary using the information below.
Some details may be missing — make reasonable assumptions when needed.

Trip mode: {ctx.mode}
Destination: {ctx.destination or "Not specified"}
Trip length (days): {ctx.days or "Not specified"}
Number of people: {ctx.people or "Not specified"}

Interests: {", ".join(ctx.interests) if ctx.interests else "Not specified"}
Weather preferences: {", ".join(ctx.weather_preferences) if ctx.weather_preferences else "Not specified"}

Budget concern: {ctx.budget_concern}
Budget amount: {ctx.budget_amount or "Not specified"}

Lodging area: {ctx.lodging_area or "Not specified"}
Food interest: {ctx.food_interest}
Shopping interest: {ctx.shopping_interest}

Schedule style: {ctx.schedule_style or "Not specified"}
Preferred time of day: {", ".join(ctx.time_preference) if ctx.time_preference else "Not specified"}

Trip purpose: {ctx.trip_purpose or "Not specified"}
Must-do activities: {", ".join(ctx.must_do) if ctx.must_do else "Not specified"}

Constraints:
- Break each day into Morning, Afternoon, Evening
- Recommend specific places
- Include food suggestions when relevant
- Keep pacing realistic
- Avoid filler language

Format:
Day 1:
Morning:
Afternoon:
Evening:
""".strip()

# ---------- Endpoint ----------

@app.post("/generate-itinerary", response_model=TripResponse)
def generate_itinerary(ctx: TripContext):
    try:
        prompt = build_prompt(ctx)

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You create high-quality, practical travel itineraries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200
        )

        itinerary_text = completion.choices[0].message.content

        return TripResponse(itinerary=itinerary_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))