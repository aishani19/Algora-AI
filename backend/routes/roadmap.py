from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import RoadmapRequest
from backend import models
from backend.models import Roadmap
from backend.llm import call_llm
from backend.auth import get_current_user

router = APIRouter()


@router.post("/")
def generate_roadmap(data: RoadmapRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    goal = data.goal
    current_skills = data.current_skills or "Not specified"

    system_prompt = "You generate structured career roadmaps in JSON."
    user_prompt = f"""
You are an expert career mentor.

Generate a structured roadmap for becoming a {goal}.
The user's current skills are: {current_skills}.

IMPORTANT:
- Focus on bridging the gap between current skills and the target goal.
- Output MUST be in valid JSON format
- Do NOT add any explanation outside JSON
- Keep it clean and structured

Format:
{{
  "goal": "{goal}",
  "current_skills": "{current_skills}",
  "upskilling_advice": "Overall strategic advice for this transition",
  "phases": [
    {{
      "title": "Phase 1: Fundamentals",
      "duration": "1-2 months",
      "topics": ["Topic1", "Topic2"],
      "resources": ["Resource1", "Resource2"]
    }},
    {{
      "title": "Phase 2: Intermediate",
      "duration": "2-3 months",
      "topics": ["Topic1", "Topic2"],
      "resources": ["Resource1", "Resource2"]
    }}
  ]
}}

Make it detailed but concise.
"""

    response = call_llm(
        user_prompt=user_prompt, 
        system_prompt=system_prompt,
        response_format={"type": "json_object"}
    )

    if response.startswith("Error generating response:"):
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=response)

    new_roadmap = Roadmap(
        goal=goal,
        roadmap=response,
        user_id=current_user.id
    )

    db.add(new_roadmap)
    db.commit()
    db.refresh(new_roadmap)

    return {
        "id": new_roadmap.id,
        "goal": goal,
        "roadmap": response
    }