from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models
from backend.auth import get_current_user

router = APIRouter()


# 📊 Get all saved roadmaps
@router.get("/")
def get_dashboard(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    roadmaps = db.query(models.Roadmap).filter(models.Roadmap.user_id == current_user.id).all()

    return {
        "total_roadmaps": len(roadmaps),
        "data": [
            {
                "id": r.id,
                "goal": r.goal,
                "roadmap": r.roadmap
            }
            for r in roadmaps
        ]
    }


# 📈 Count roadmaps by goal
@router.get("/stats")
def get_stats(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    roadmaps = db.query(models.Roadmap).filter(models.Roadmap.user_id == current_user.id).all()

    goal_count = {}

    for r in roadmaps:
        goal = r.goal.lower()
        goal_count[goal] = goal_count.get(goal, 0) + 1

    return {
        "total": len(roadmaps),
        "goal_distribution": goal_count
    }


# 🔍 Get single roadmap
@router.get("/{roadmap_id}")
def get_roadmap(roadmap_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    roadmap = db.query(models.Roadmap).filter(models.Roadmap.id == roadmap_id, models.Roadmap.user_id == current_user.id).first()

    if not roadmap:
        return {"error": "Roadmap not found"}

    return {
        "id": roadmap.id,
        "goal": roadmap.goal,
        "roadmap": roadmap.roadmap
    }


# ❌ Delete roadmap
@router.delete("/{roadmap_id}")
def delete_roadmap(roadmap_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    roadmap = db.query(models.Roadmap).filter(models.Roadmap.id == roadmap_id, models.Roadmap.user_id == current_user.id).first()

    if not roadmap:
        return {"error": "Roadmap not found"}

    db.delete(roadmap)
    db.commit()

    return {"message": "Roadmap deleted successfully"}
