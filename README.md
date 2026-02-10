# AI Trip Itinerary Generator

An AI-powered travel itinerary generator that creates **realistic, preference-aware itineraries** by asking users structured, constraint-first questions.

Unlike generic AI travel planners, this project is designed to reduce hallucinations, avoid rushed schedules, and respect uncertainty by explicitly separating **hard constraints** from **soft preferences**.

---

## Project Status

**In active development.**

- Backend logic is partially implemented and functional
- Both trip modes (discover + known destination) work end-to-end
- Generated itineraries are realistic, paced, and preference-aware
- Frontend has not been implemented yet
- Output structure and validation are still evolving

The current focus is **backend correctness, question design, and itinerary quality**, not UI polish.

---

## Trip Modes

### Option A: Discover a Destination
For users who **don’t know where they want to go yet**.

The system:
- Interprets high-level intent (e.g. “relaxing,” “nature,” “not rushed”)
- Applies distance, transport, budget, and pacing constraints
- Suggests a coherent trip with specific destinations

### Option B: Known Destination
For users who **already know where they’re going**.

The system:
- Builds a day-by-day itinerary for a fixed location
- Respects time constraints, rest days, accessibility, and schedule style
- Avoids overloading days or repeating similar activities

---

## Core Design Principles

- **Constraint-first questioning**  
  Required constraints (dates, duration, mobility, transport, time limits) are collected before preferences.

- **Explicit uncertainty handling**  
  Optional or unanswered questions are treated as unknown rather than guessed.

- **Preference-weighted, not preference-dominated**  
  Interests like food, shopping, nightlife, and photography influence decisions proportionally.

- **Realistic pacing**  
  Supports relaxed schedules, early evenings, rest days, and partial days.

- **Avoids generic or unverifiable attractions**  
  Prioritizes well-known, accessible locations and realistic travel flow.

---

## How It Works (High Level)

1. User selects a trip mode (discover or known destination)
2. System asks structured questions to gather:
   - Constraints (required)
   - Preferences (optional)
3. Inputs normalize into a single itinerary context
4. The model generates a day-by-day itinerary that:
   - Respects constraints and exclusions
   - Accounts for uncertainty
   - Balances activity, rest, and travel time

---

## Repository Structure

```text
AI_TRIP_ITINERARY_GENERATOR/
├── backend/        # Backend logic (in progress)
├── frontend/       # Frontend (not implemented yet)
├── .env            # Environment variables (ignored)
├── .gitignore
└── README.md
```

---

## Current Capabilities

- Two fully defined trip modes (discover + known)
- Structured constraint and preference capture
- Preference-aware itinerary generation
- Support for:
  - Time constraints
  - Rest days
  - Activity level
  - Accessibility considerations
  - Early/late schedule preferences
- Outputs realistic, named locations and coherent daily flow

---

## Sample JSON Request (Option B, Known Destination)

```text
{
  "trip_mode": "known",

  "destination": "Oregon Coast (Cannon Beach, Newport, Florence)",
  "days": 5,
  "people": 2,

  "origin_location": "Portland, Oregon",
  "transport_mode": "driving",

  "international_travel": false,
  "preferred_countries": null,
  "distance_preference": null,

  "has_dates": true,
  "date_range": "July 10 to July 15",

  "area_structure": "multiple_areas",

  "has_time_constraints": false,
  "time_constraints_detail": null,

  "budget_concern": true,
  "budget_amount": 1800,

  "weather_avoidance": ["heavy rain", "strong winds"],

  "food_interest_level": 6,
  "cuisine_preferences": ["seafood", "local cuisine"],

  "shopping_interest_level": 2,
  "shopping_preferences": null,

  "trip_purpose": "Relaxing coastal road trip with scenic views, nature, and small towns",
  "schedule_style": "relaxed",

  "must_do": [
    "Visit Cannon Beach and Haystack Rock",
    "See tide pools",
    "Drive scenic coastal highways",
    "Watch sunsets over the ocean"
  ],

  "must_avoid": [
    "Crowded nightlife",
    "Overly packed daily schedules"
  ],

  "physical_activity_level": 4,
  "public_transit_comfort": 1,

  "nightlife": false,

  "photography_importance": 7,

  "desired_feelings": ["relaxed", "refreshed", "grounded"],

  "rest_days": 1,

  "travel_vs_depth": "balanced",

  "excluded_places": ["Seaside"],

  "start_time_preference": "midday",
  "end_time_preference": "early",

  "special_group_needs": [],
  "accessibility_needs": false,

  "additional_notes": "Prefer shorter drives between stops and time to explore each town without rushing."
}
```

---

## Sample Output (Generated Itinerary)

```text
{
  "itinerary": {
    "days": [
      {
        "day": 1,
        "sections": {
          "morning": [
            "Arrive in Cannon Beach",
            "Check into your accommodation"
          ],
          "afternoon": [
            "Visit Cannon Beach and Haystack Rock",
            "Explore local shops and galleries"
          ],
          "evening": [
            "Have dinner at a seafood restaurant",
            "Watch the sunset over the ocean"
          ]
        }
      },
      {
        "day": 2,
        "sections": {
          "morning": [
            "Drive to Ecola State Park for scenic views",
            "Hike along the trails to see the coastline"
          ],
          "afternoon": [
            "Enjoy a picnic lunch at the park",
            "Drive to Newport along the scenic highway"
          ],
          "evening": [
            "Check into your Newport accommodation",
            "Dine at a local seafood restaurant"
          ]
        }
      },
      {
        "day": 3,
        "sections": {
          "morning": [
            "Visit the Oregon Coast Aquarium",
            "Explore the nearby Yaquina Head Outstanding Natural Area"
          ],
          "afternoon": [
            "Have lunch at a local cafe",
            "See tide pools at low tide"
          ],
          "evening": [
            "Enjoy dinner at a waterfront restaurant",
            "Watch the sunset from the beach"
          ]
        }
      },
      {
        "day": 4,
        "sections": {
          "morning": [
            "Drive to Florence",
            "Visit the Sea Lion Caves"
          ],
          "afternoon": [
            "Walk along the beach and enjoy the scenery",
            "Have lunch at a local diner"
          ],
          "evening": [
            "Check into your accommodation in Florence",
            "Relax and enjoy a quiet evening"
          ]
        }
      },
      {
        "day": 5,
        "sections": {
          "morning": [
            "Spend a leisurely morning at the beach",
            "Take photographs of the coastal views"
          ],
          "afternoon": [
            "Begin your drive back, stopping at scenic overlooks",
            "Have lunch along the way"
          ],
          "evening": [
            "Arrive back home"
          ]
        }
      }
    ],
    "summary": "This 5-day itinerary offers a relaxed coastal road trip along the Oregon Coast, focusing on scenic views, nature, and local cuisine while allowing time for exploration and photography."
  }
}
```

---

## Planned Improvements

- Finalize backend constraint normalization
- Improve output structure consistency
- Add **PDF itinerary export (backend)**
- Build minimal frontend (question flow + itinerary view)
- Add export and sharing options

---

## Important Note

Frontend work will begin after backend behavior stabilizes.