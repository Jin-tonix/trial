import openai
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from rag_helper import RAGHelper  # Import the helper to handle Elasticsearch queries

# 환경 변수 로드 및 OpenAI API 설정
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = "gpt-4o-mini"  # 모델 이름 수정 (gpt-4로 변경)

# YouTube에서 운동 영상 URL을 검색하는 함수 (YouTube API 사용)
def get_youtube_video_urls(query, max_results=5):
    youtube_api_key = "AIzaSyC8d1QRyB46bLvDRzo95YxJX7HzZrsKkZc"  # Your API key here
    youtube = build("youtube", "v3", developerKey=youtube_api_key)

    # 한국어로 우선 검색
    try:
        search_response = youtube.search().list(
            q=query,
            type="video",
            part="id,snippet",
            maxResults=max_results,
            relevanceLanguage='ko'  # 한국어로 우선 검색
        ).execute()

        video_urls = []
        for item in search_response['items']:
            video_id = item['id']['videoId']
            video_urls.append(f"https://www.youtube.com/watch?v={video_id}")

        # 한국어 영상이 없으면 영어로 다시 검색
        if not video_urls:
            search_response_en = youtube.search().list(
                q=query,
                type="video",
                part="id,snippet",
                maxResults=max_results,
                relevanceLanguage='en'  # 영어로 다시 검색
            ).execute()

            for item in search_response_en['items']:
                video_id = item['id']['videoId']
                video_urls.append(f"https://www.youtube.com/watch?v={video_id}")

        return video_urls if video_urls else ["No videos found."]
    except Exception as e:
        print(f"Error fetching YouTube videos: {e}")
        return ["No videos found."]

# AI 모델을 이용한 추천 생성 함수
def get_recommendation(question):
    rag_helper = RAGHelper()

    # Elasticsearch에서 메타데이터 검색
    metadata_results = rag_helper.search_metadata(question)
    context_metadata = "\n".join([md.get("description", "") for md in metadata_results])

    # PDF 문서에서 정보 검색
    pdf_extraction = rag_helper.search_pdf_documents(question)
    context_pdf = "\n".join(pdf_extraction) if pdf_extraction else "No relevant PDF content found."

    # JSON 문서에서 정보 검색
    json_results = rag_helper.search_json_documents(question)
    context_json = "\n".join(json_results) if json_results else "No relevant JSON content found."

    # AI 모델에서 운동 추천과 피드백 생성
    response = openai.ChatCompletion.create(
        model=model_engine,  # 모델 이름을 model 파라미터로 설정
        messages=[{
            "role": "system", "content": "You are a helpful assistant. You provide feedback on exercises and recommend new exercises based on user questions."
        }, {
            "role": "user", "content": question
        }, {
            "role": "assistant", "content": context_metadata + "\n" + context_pdf + "\n" + context_json
        }],
        max_tokens=300  # 글자 수 제한을 늘림
    )
    feedback_and_exercise = response['choices'][0]['message']['content'].strip()

    # 운동과 관련된 키워드 추출
    def extract_exercise_keywords(feedback):
        # 운동과 관련된 키워드를 추출합니다 (운동의 종류, 목적 등을 포함)
        keywords = ["운동", "스트레칭", "근력", "운동법", "피지컬", "근육", "체중감량", "다이어트"]  # 예시 키워드
        return [keyword for keyword in keywords if keyword in feedback]

    # 피드백에서 운동 키워드 추출
    exercise_keywords = extract_exercise_keywords(feedback_and_exercise)

    # 운동 관련 키워드를 사용하여 YouTube에서 운동 영상 검색
    youtube_video_urls = get_youtube_video_urls(' '.join(exercise_keywords))

    # 식단 추천 추가 (max_tokens를 더 크게 설정하여 긴 식단 추천 받기)
    diet_response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[{
            "role": "system", "content": "You are a helpful assistant."
        }, {
            "role": "user", "content": f"질문에 대한 답변을 제공한 후 아침, 점심, 저녁, 간식으로 구성된 적합한 식단을 추천해줘: {question}"
        }],
        max_tokens=500  # 식단을 길게 추천하기 위해 토큰 수 증가
    )
    diet_recommendation = diet_response['choices'][0]['message']['content'].strip()

    return {
        "feedback_and_exercise": feedback_and_exercise,
        "diet_recommendation": diet_recommendation,
        "recommended_videos": youtube_video_urls,  # YouTube 동영상 URL 리스트
        "metadata_reference": metadata_results,
        "pdf_reference": pdf_extraction if pdf_extraction else ["No relevant PDF content found."], # PDF에서 추출한 내용
        "json_reference": json_results if json_results else ["No relevant JSON content found."]  # JSON에서 추출한 내용
    }
