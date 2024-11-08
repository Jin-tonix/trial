from transformers import pipeline

# LLM 모델 로드
llm = pipeline("text-generation", model="Bllossom/llama-3.2-Korean-Bllossom-3B")

def generate_feedback(goal_details):
    # 피드백 생성 텍스트
    prompt = f"사용자가 {goal_details['target_area']} 부위를 대상으로 {goal_details['sets']}세트, {goal_details['reps']}회 목표로 운동을 계획하고 있습니다. 올바른 운동 방법에 대한 피드백을 제공해주세요."
    feedback = llm(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]
    return feedback

def generate_recommendation(target_area):
    # 추천 운동 생성 텍스트
    prompt = f"{target_area} 부위 강화를 위해 적절한 운동을 추천해주세요."
    recommendation = llm(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]
    return recommendation
