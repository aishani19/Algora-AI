from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models
from backend.schemas import ApproachRequest
from backend.llm import call_llm
from backend.auth import get_current_user


router = APIRouter()

@router.post("/")
def analyze(req: ApproachRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    system_prompt = "You are a strict, top-tier tech company DSA interviewer."
    user_prompt = f"""
You are rigorously evaluating a candidate's approach to a Data Structures and Algorithms problem.

Problem: {req.problem}
Candidate Approach: {req.approach}

Provide a structured, critical evaluation covering:
1. **Correctness**: Is the approach fundamentally correct for the problem?
2. **Time & Space Complexity**: What is the precise Big-O for BOTH time and space for their approach?
3. **Optimization Check**: Is the candidate's approach the MOST optimal one? If there is a more optimal algorithm or if space complexity can be reduced, strictly point it out, explain its complexity, and describe the intuition behind it.

Be rigorous but constructive. Do not give away the final code. Use clear Markdown headers.
"""

    result = call_llm(user_prompt=user_prompt, system_prompt=system_prompt)
    
    if result.startswith("Error generating response:"):
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=result)
        
    new_analysis = models.Analysis(
        problem=req.problem,
        approach=req.approach,
        analysis=result,
        user_id=current_user.id
    )

    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return {"analysis": result, "id": new_analysis.id}