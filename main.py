from recommendation_service import get_recommendation
from index_metadata import index_metadata
from index_json import index_json_files_from_folder

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
            print("Json 참조 정보:", recommendation["json_reference"])

        except Exception as e:
            print(f"오류 발생: {e}")

if __name__ == "__main__":
    # 인덱싱 작업 실행
    index_metadata()  # 메타데이터 인덱싱
    json_folder = "json"  # JSON 파일이 있는 폴더
    index_json_files_from_folder(json_folder)  # JSON 파일 인덱싱
    # pdf_files 리스트를 정의하여 여러 PDF 파일 처리
    # process_multiple_pdfs(pdf_files)
    interact_with_ai()  # AI 대화 인터페이스 시작
