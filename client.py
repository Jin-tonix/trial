import requests

# 서버 URL
url = "http://127.0.0.1:8000/exercise_recommendation/"

# 사용자 입력을 받는 부분
user_input = input("운동 목표를 설명해 주세요 (예: '하체 강화를 위해 15회씩 3세트'):\n")

# 입력을 분석하여 데이터 구성
print("입력 데이터를 분석하고 있습니다...")
# 분석된 데이터 예시
data = {
    "goal_description": user_input
}

# 데이터 요청 보내기
print(f"서버로 요청을 보내는 중: {data}")
try:
    response = requests.post(url, json=data)
    response.raise_for_status()  # HTTP 오류가 발생하면 예외를 일으킵니다.
    print("응답을 성공적으로 받았습니다.")

    # 응답 확인 및 출력
    result = response.json()
    print("\n--- 추천 운동 ---")
    print(result.get("recommendation", "추천 운동을 가져올 수 없습니다."))
    print("\n--- 피드백 ---")
    print(result.get("feedback", "피드백을 가져올 수 없습니다."))
    print("\n--- 권장 강도 ---")
    print(result.get("intensity", "강도 정보를 가져올 수 없습니다."))

except requests.exceptions.RequestException as e:
    print("요청에 문제가 발생했습니다:", e)
