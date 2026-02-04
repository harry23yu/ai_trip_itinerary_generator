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
    # User chooses between Option A (discover) and Option B (known)
    trip_mode: Literal["discover", "known"] = Field(
        ..., description="discover = user does not know destination; known = user knows destination"
    )

    # ---------- Core trip info ----------
    destination: Optional[str] = Field(
        None, description="City/area and optional dates (required if trip_mode='known')"
    )

    days: Optional[int] = Field(
        None, ge=1, le=30, description="Trip length in days"
    )

    people: int = Field(..., ge=1)

    # ---------- Option A: discovery-specific ----------
    discovery_intent: Optional[str] = None          # A Q1 (OE)
    knows_trip_length: Optional[bool] = None        # A Q2 (MC)
    origin_location: Optional[str] = None           # A Q6 (OE)
    transport_mode: Optional[str] = None            # A Q5 (MC)
    area_structure: Optional[
        Literal["one_area", "multiple_areas"]
    ] = None  # Option A Q11 (MC)

    distance_preference: Optional[
        Literal["<10 miles", "10-20 miles", "20-50 miles", "50-100 miles", "100-200 miles", "200-500 miles", ">500 miles", "no preference"]
    ] = None                                        # A Q7 (MC)

    international_travel: Optional[bool] = None     # A Q8 (MC)

    preferred_countries: Optional[List[str]] = None # A Q9 (OE, conditional)

    travel_months: Optional[List[str]] = None       # A Q10 (CATA)

    weather_preferences: Optional[List[str]] = None # A Q10 (CATA)
    weather_avoidance: Optional[List[str]] = None   # A Q11 (CATA)

    # ---------- Shared preferences (A & B) ----------
    activities_interest: Optional[List[str]] = None # A Q8 / B Q5 (CATA)

    budget_concern: Optional[bool] = None            # A Q9 / B Q6 (MC)
    budget_amount: Optional[int] = None              # A Q10 / B Q7 (NUM)

    food_interest_level: Optional[int] = Field(None, ge=1, le=10)     # A Q11 / B Q8
    cuisine_preferences: Optional[List[str]] = None                  # A Q12 / B Q9

    shopping_interest_level: Optional[int] = Field(None, ge=1, le=10) # A Q13 / B Q10
    shopping_preferences: Optional[List[str]] = None                 # A Q14 / B Q11

    preferred_times_outside: Optional[
        List[Literal["day", "evening", "night"]]
    ] = None                                                          # A Q15 / B Q12

    trip_purpose: Optional[str] = None                                # A Q16 / B Q13

    schedule_style: Optional[
        Literal["packed", "relaxed"]
    ] = None                                                          # A Q17 / B Q14

    must_do: Optional[List[str]] = None                               # A Q18 / B Q15
    must_avoid: Optional[List[str]] = None                            # A Q19 / B Q16

    physical_activity_level: Optional[int] = Field(None, ge=1, le=10) # A Q20 / B Q17

    visited_before: Optional[bool] = None                             # B Q18

    highlights_vs_hidden: Optional[
        Literal["highlights", "hidden"]
    ] = None                                                          # A Q21 / B Q19

    public_transit_comfort: Optional[int] = Field(None, ge=1, le=10)  # A Q22 / B Q20

    nightlife: Optional[bool] = None                                  # A Q23 / B Q21

    photography_importance: Optional[int] = Field(None, ge=1, le=10)  # A Q24 / B Q22

    desired_feelings: Optional[List[str]] = None                      # A Q25 / B Q23

    rest_days: Optional[int] = Field(None, ge=0, le=30)               # A Q26 / B Q24

    travel_vs_depth: Optional[
        Literal["travel_more", "fewer_places"]
    ] = None                                                          # A Q27 / B Q25

    excluded_places: Optional[List[str]] = None                       # A Q28 / B Q26

    start_time_preference: Optional[
        Literal["early", "midday", "late"]
    ] = None                                                          # A Q29 / B Q27

    end_time_preference: Optional[
        Literal["early", "midnight", "late"]
    ] = None                                                          # A Q30 / B Q28

    special_group_needs: Optional[
        List[Literal["children", "elderly", "disabled"]]
    ] = None                                                          # A Q31 / B Q29

    accessibility_needs: Optional[bool] = None                        # A Q32 / B Q30

    has_time_constraints: bool                                        # A Q33 / B Q31
    time_constraints_detail: Optional[str] = None                     # A Q34 / B Q32

    experience_preference: Optional[
        Literal["iconic_views", "immersive_local"]
    ] = None                                                          # A Q35 / B Q33

class TripResponse(BaseModel):
    itinerary: str

# ---------- Prompt ----------

def build_prompt(ctx: TripContext) -> str:
    if ctx.trip_mode == "discover":
        destination_block = f"""
Trip mode: Destination discovery (Option A)

User intent / high-level preferences: {ctx.discovery_intent}
Current location (city, country): {ctx.origin_location}
Preferred distance from origin: {ctx.distance_preference or "Not specified"}
Willing to travel internationally: {ctx.international_travel}
Preferred countries (if international): {ctx.preferred_countries or "Not specified"}
Planned travel months: {ctx.travel_months}
Transportation mode to destination: {ctx.transport_mode}
Planned trip structure (one area vs multiple areas): {ctx.area_structure or "Not specified"}
"""
    else:
        destination_block = f"""
Trip mode: Known destination (Option B)

Destination details (including dates if provided): {ctx.destination}
"""

    return f"""
You are an expert travel planner.

Create the best possible itinerary using the information below.
All fields reflect explicit user answers. If a value is "Not specified",
make reasonable, conservative assumptions while respecting constraints.

{destination_block}

Trip length (days): {ctx.days or "Not specified"}
Trip length certainty: {"Known" if ctx.days else "Unknown"}
Number of people: {ctx.people}

Weather preferences: {ctx.weather_preferences or "Not specified"}
Weather conditions to avoid: {ctx.weather_avoidance or "Not specified"}

General activity interests: {ctx.activities_interest or "Not specified"}

Budget sensitivity: {ctx.budget_concern}
Budget amount: {ctx.budget_amount or "Not specified"}

Food interest level (1–10): {ctx.food_interest_level or "Not specified"}
Cuisine preferences: {ctx.cuisine_preferences or "Not specified"}

Shopping interest level (1–10): {ctx.shopping_interest_level or "Not specified"}
Shopping preferences: {ctx.shopping_preferences or "Not specified"}

Preferred times to be outside: {ctx.preferred_times_outside or "Not specified"}

Main purpose of trip: {ctx.trip_purpose or "Not specified"}

Schedule style: {ctx.schedule_style or "Not specified"}

Must-do activities: {ctx.must_do or "None"}
Things to avoid: {ctx.must_avoid or "None"}

Physical activity level (1–10): {ctx.physical_activity_level or "Not specified"}

Visited destination before: {ctx.visited_before}

Preference for famous vs hidden places: {ctx.highlights_vs_hidden or "Not specified"}

Public transportation comfort (1–10): {ctx.public_transit_comfort or "Not specified"}

Nightlife included: {ctx.nightlife}

Photography importance (1–10): {ctx.photography_importance or "Not specified"}

Desired feelings at end of trip: {ctx.desired_feelings or "Not specified"}

Number of rest days desired: {ctx.rest_days or "Not specified"}

Travel vs depth preference: {ctx.travel_vs_depth or "Not specified"}

Excluded places or attractions: {ctx.excluded_places or "None"}

Preferred daily start time: {ctx.start_time_preference or "Not specified"}
Preferred daily end time: {ctx.end_time_preference or "Not specified"}

Special group considerations (children, elderly, etc.): {ctx.special_group_needs or "None"}

Accessibility or mobility needs: {ctx.accessibility_needs}

Has strict time constraints: {ctx.has_time_constraints}
Time constraint details: {ctx.time_constraints_detail or "None"}

Experience preference (iconic vs immersive): {ctx.experience_preference or "Not specified"}

Constraints and interpretation rules:

General structure and feasibility:
- Break each day into Morning, Afternoon, and Evening.
- Keep pacing realistic given trip length, rest days, physical activity level, and transit time.
- Respect all accessibility, mobility, and time constraints strictly.
- Avoid any places the user explicitly wants to avoid.
- When information is missing, make conservative, low-risk assumptions.

Preference strength and priority:
- Treat explicit user preferences as higher priority than default travel norms.
- When preferences conflict, resolve them by the following order:
  1. Safety, accessibility, and time constraints
  2. Explicit exclusions and hard constraints
  3. Strong numeric preferences (7-10)
  4. Moderate numeric preferences (4-6)
  5. Weak numeric preferences (1-3)
  6. Generic travel conventions

Numeric preference interpretation (apply consistently across all numeric questions):
- 1-3: low interest → minimize mentions; include only if unavoidable for logistics
- 4-6: moderate interest → include selectively, not as a focal theme
- 7-10: high interest → make this a central organizing theme

Apply numeric interpretation rules strictly for:
- food interest
- shopping interest
- physical activity
- nightlife
- photography

Food and dining:
- When food interest is low (1-3), treat meals as logistical necessities and avoid naming specific restaurants unless they are extremely popular landmarks or directly support a higher-priority activity.
- When food interest is moderate or high (≥4), include dining experiences proportional to the stated interest level.
- “Extremely popular” refers to widely recognized, casual landmarks (e.g., markets or famous food streets), not reservation-only or niche venues.

Hidden vs iconic experiences:
- If the user prefers iconic views or highlights, prioritize major landmarks and widely recognized attractions.
- If the user prefers hidden or immersive local experiences, avoid major tourist landmarks even if they are famous, and instead prioritize:
  - everyday local environments
  - neighborhood walks
  - public coastal or park access points
  - small towns, local districts, and residential areas
- Hidden experiences must still be well-documented and publicly accessible; avoid obscure, unverifiable, or speculative venues.

First-time vs repeat visitors:
- For first-time visitors, default to highlights only if the user has not expressed a preference for hidden or immersive experiences.
- For repeat visitors, prioritize less obvious experiences unless the user explicitly prefers highlights.

Transportation and movement:
- Match activity density and walking distance to the stated physical activity level.
- Use public transportation primarily when comfort level is moderate or high; otherwise favor walkable clusters or short transfers.
- Minimize unnecessary backtracking and group activities by neighborhood or proximity.

Nightlife:
- If nightlife is false or low (1-3), do not include bars, clubs, or late-night activities.
- If nightlife interest is moderate or high (≥4), include it proportionally and without overwhelming daytime plans.

Shopping:
- Include shopping only if shopping interest is ≥4.
- Tailor shopping experiences to stated preferences (e.g., local crafts vs malls).

Photography:
- If photography importance is high (≥7), prioritize visually distinctive locations and timing (golden hour, scenic viewpoints).
- If photography importance is low (1-3), do not optimize the itinerary around photo opportunities.

Accuracy and realism:
- Only suggest places that are generally accessible to the public.
- Avoid inventing or guessing venue names.
- Prefer real, verifiable locations, but allow lesser-known local places when they align with stated preferences.
- Keep descriptions concise and practical; avoid long historical explanations unless explicitly requested.

Narrative emphasis order (highest to lowest):
1. Explicit hard constraints and exclusions
2. Strong numeric preferences (7-10)
3. Hidden vs iconic experience preference
4. Moderate numeric preferences (4-6)
5. Logistics (meals, transit, rest)
6. Weak preferences (1-3), only when unavoidable

Format:
Day 1:
Morning:
Afternoon:
Evening:
""".strip()

# ---------- Endpoint ----------

@app.post("/generate-itinerary", response_model=TripResponse)
def generate_itinerary(ctx: TripContext):

    # ---- Trip mode validation ----
    if ctx.trip_mode == "known":
        if not ctx.destination:
            raise HTTPException(400, "destination is required when trip_mode='known'")
        if not ctx.days:
            raise HTTPException(400, "days is required when trip_mode='known'")
    if ctx.trip_mode == "discover":
        if not ctx.discovery_intent:
            raise HTTPException(400, "discovery_intent is required when trip_mode='discover'")
        if not ctx.origin_location:
            raise HTTPException(400, "origin_location is required when trip_mode='discover'")
        if ctx.knows_trip_length and not ctx.days:
            raise HTTPException(400, "days required when knows_trip_length is true")
    if ctx.has_time_constraints and not ctx.time_constraints_detail:
        raise HTTPException(
            status_code=400,
            detail="Time constraints details required when has_time_constraints is true."
        )
    
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