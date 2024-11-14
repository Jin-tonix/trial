from recommendation_service import get_recommendation
from index_metadata import index_metadata

# CMD 대화 인터페이스
def interact_with_ai():
    print("AI와의 대화를 시작합니다. 종료를 원하시면 '종료'를 입력하세요.")
    while True:
        user_question = input("질문: ")
        if user_question.lower() == '종료':
            print("대화를 종료합니다.")
            break
        try:
            recommendation = get_recommendation(user_question)
            print("AI 피드백 및 운동 추천:", recommendation["feedback_and_exercise"])
            print("추천 식단:", recommendation["diet_recommendation"])
            print("추천 영상 목록:", recommendation["recommended_videos"])
            print("메타데이터 참조 정보:", recommendation["metadata_reference"])
            print("PDF 참조 정보:", recommendation["pdf_reference"])

        except Exception as e:
            print(f"오류 발생: {e}")

if __name__ == "__main__":
    index_metadata()  # 인덱스화 실행
    interact_with_ai()  # AI 대화 인터페이스 시작
