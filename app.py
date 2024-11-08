from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm_module import generate_feedback, generate_recommendation

app = FastAPI()

class UserGoal(BaseModel):
    reps: int
    sets: int
    target_area: str  # 운동 목표 부위 예: "하체", "상체", "전신" 등

@app.post("/exercise_recommendation/")
async def exercise_recommendation(goal: UserGoal):
    try:
        # 운동 추천 생성
        recommendation = generate_recommendation(goal.target_area)
        
        # 피드백 생성
        feedback = generate_feedback({
            "reps": goal.reps,
            "sets": goal.sets,
            "target_area": goal.target_area
        })
        
        return {
            "recommendation": recommendation,
            "feedback": feedback,
            "message": f"{goal.sets}세트에 {goal.reps}회 목표로 {goal.target_area} 부위를 운동하도록 추천합니다."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
