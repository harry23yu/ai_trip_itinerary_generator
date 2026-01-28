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

class TripRequest(BaseModel):
    destination: str = Field(..., example="Tokyo, Japan")
    days: int = Field(..., ge=1, le=14)
    interests: list[str] = Field(..., example=["food", "culture", "walking"])

class TripResponse(BaseModel):
    itinerary: str

# ---------- Prompt ----------

def build_prompt(req: TripRequest) -> str:
    return f"""
You are an expert travel planner.

Create a detailed {req.days}-day travel itinerary.

Destination: {req.destination}
Traveler interests: {", ".join(req.interests)}

Constraints:
- Break each day into Morning, Afternoon, Evening
- Recommend specific places (not generic categories)
- Include food and dining suggestions
- Keep pacing realistic (no rushing across the city)
- Prefer walkable or transit-efficient plans
- Avoid filler language

Format exactly like this:

Day 1:
Morning:
Afternoon:
Evening:

Day 2:
...
""".strip()

# ---------- Endpoint ----------

@app.post("/generate-itinerary", response_model=TripResponse)
def generate_itinerary(req: TripRequest):
    try:
        prompt = build_prompt(req)

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