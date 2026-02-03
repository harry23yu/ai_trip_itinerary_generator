import os
from typing import Optional, List, Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI(title="AI Trip Itinerary Generator")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- Models ----------

class TripContext(BaseModel):
    # Required core inputs
    destination: str = Field(..., description="City/area and optional dates")
    days: int = Field(..., ge=1, le=30)
    people: int = Field(..., ge=1)

    # Optional preferences
    weather_preferences: Optional[List[str]] = None                  # Q3 (CATA)
    activities_interest: Optional[List[str]] = None                  # Q5 (CATA)

    budget_concern: Optional[bool] = None                             # Q6 (MC)
    budget_amount: Optional[int] = None                               # Q7 (NUM)

    food_interest_level: Optional[int] = Field(None, ge=1, le=10)     # Q8 (NUM)
    cuisine_preferences: Optional[List[str]] = None                  # Q9 (CATA)

    shopping_interest_level: Optional[int] = Field(None, ge=1, le=10) # Q10 (NUM)
    shopping_preferences: Optional[List[str]] = None                 # Q11 (CATA)

    preferred_times_outside: Optional[
        List[Literal["day", "evening", "night"]]
    ] = None                                                          # Q12 (CATA)

    trip_purpose: Optional[str] = None                                # Q13 (OE)

    schedule_style: Optional[
        Literal["packed", "relaxed"]
    ] = None                                                          # Q14 (MC)

    must_do: Optional[List[str]] = None                               # Q15 (OE)
    must_avoid: Optional[List[str]] = None                            # Q16 (OE)

    physical_activity_level: Optional[int] = Field(None, ge=1, le=10) # Q17 (NUM)

    visited_before: Optional[bool] = None                             # Q18 (MC)

    highlights_vs_hidden: Optional[
        Literal["highlights", "hidden"]
    ] = None                                                          # Q19 (MC)

    public_transit_comfort: Optional[int] = Field(None, ge=1, le=10)  # Q20 (NUM)

    nightlife: Optional[bool] = None                                  # Q21 (MC)

    photography_importance: Optional[int] = Field(None, ge=1, le=10)  # Q22 (NUM)

    desired_feelings: Optional[List[str]] = None                     # Q23 (CATA)

    rest_days: Optional[int] = Field(None, ge=0, le=30)               # Q24 (NUM)

    travel_vs_depth: Optional[
        Literal["travel_more", "fewer_places"]
    ] = None                                                          # Q25 (MC)

    excluded_places: Optional[List[str]] = None                       # Q26 (MC / OE)

    start_time_preference: Optional[
        Literal["early", "midday", "late"]
    ] = None                                                          # Q27 (MC)

    end_time_preference: Optional[
        Literal["early", "midnight", "late"]
    ] = None                                                          # Q28 (MC)

    special_group_needs: Optional[
        List[Literal["children", "elderly", "disabled"]]
    ] = None                                                          # Q29 (CATA)

    accessibility_needs: Optional[bool] = None                        # Q30 (MC)

    has_time_constraints: bool                                        # Q31 (R, MC)
    time_constraints_detail: Optional[str] = None                     # Q32 (OE)

    experience_preference: Optional[
        Literal["iconic_views", "immersive_local"]
    ] = None                                                          # Q33 (MC)


class TripResponse(BaseModel):
    itinerary: str

# ---------- Prompt ----------

def build_prompt(ctx: TripContext) -> str:
    return f"""
You are an expert travel planner.

Create the best possible itinerary using the information below.
Some details may be missing — make reasonable assumptions.

Destination: {ctx.destination}
Trip length (days): {ctx.days}
Number of people: {ctx.people}

Interests: {ctx.activities_interest or "Not specified"}
Food interest level: {ctx.food_interest_level or "Not specified"}
Shopping interest level: {ctx.shopping_interest_level or "Not specified"}

Schedule style: {ctx.schedule_style or "Not specified"}
Physical activity level: {ctx.physical_activity_level or "Not specified"}

Must-do activities: {ctx.must_do or "None"}
Things to avoid: {ctx.must_avoid or "None"}

Accessibility needs: {ctx.accessibility_needs}
Special group needs: {ctx.special_group_needs or "None"}

Constraints:
- Break each day into Morning, Afternoon, Evening
- Keep pacing realistic
- Respect accessibility and time constraints
- Avoid places the user wants to avoid
- Use reasonable defaults where information is missing
- Prioritize activities based on stated interest levels; do not overemphasize low-interest categories
- Treat meals as logistical necessities unless food interest is high; avoid destination dining when food interest is low
- Minimize unnecessary backtracking; group activities by neighborhood or proximity when possible.
- Prefer well-known, widely documented locations over obscure or unverifiable venues
- Match walking, hiking, and activity intensity to the stated physical activity level
- For first-time visitors, emphasize core highlights; for repeat visitors, prioritize less obvious experiences
- Avoid repeating the same or too similar activities across multiple days unless explicitly requested.
- Keep descriptions concise and practical; avoid long historical explanations unless explicitly requested

Numeric preference interpretation rules:

- 1-3: low interest → minimize mentions; include only when unavoidable
- 4-6: moderate interest → include occasionally but not as a focus
- 7-10: high interest → make this a central theme

Apply these rules strictly for:
- food interest
- shopping interest
- physical activity
- nightlife
- photography

When food interest is low (1-3), mention meals generically (e.g., “grab a quick bite nearby”) and avoid naming specific restaurants unless it is extremely popular in the area or they directly support a higher-priority activity.

“Extremely popular” means widely recognized city landmarks (e.g., Pike Place Market, Times Square), not niche or reservation-only restaurants or shops.

Narrative priority order (highest to lowest):
1. activities_interest and sports-related experiences
2. outdoor and physical activities (within stated limits)
3. iconic views / highlights vs hidden preference
4. shopping (if interest ≥ 4)
5. food and dining (only if interest ≥ 4)

Format:
Day 1:
Morning:
Afternoon:
Evening:
""".strip()

# ---------- Endpoint ----------

@app.post("/generate-itinerary", response_model=TripResponse)
def generate_itinerary(ctx: TripContext):
    if ctx.has_time_constraints and not ctx.time_constraints_detail:
        raise HTTPException(
            status_code=400,
            detail="Time constraints details required when has_time_constraints is true."
        )

    prompt = build_prompt(ctx)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate realistic, practical travel itineraries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1200
    )

    return TripResponse(
        itinerary=completion.choices[0].message.content
    )