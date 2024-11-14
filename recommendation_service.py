import openai
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from googleapiclient.discovery import build

# 환경 변수 로드 및 OpenAI API 설정
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = "gpt-4"  # 모델 이름 수정 (gpt-4로 변경)

# Elasticsearch 설정
es = Elasticsearch("http://localhost:9200")

class RAGHelper:
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")

    def search_metadata(self, query):
        # Elasticsearch에서 메타데이터 검색
        results = self.es.search(index="metadata", body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "description", "keywords"]
                }
            }
        })
        return [hit["_source"] for hit in results["hits"]["hits"]]

# YouTube에서 운동 영상 URL을 검색하는 함수 (YouTube API 사용)
def get_youtube_video_urls(query, max_results=5):
    youtube_api_key = "AIzaSyC8d1QRyB46bLvDRzo95YxJX7HzZrsKkZc"  # Your API key
    youtube = build("youtube", "v3", developerKey=youtube_api_key)

    # 한국어로 우선 검색
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

# AI 모델을 이용한 추천 생성 함수
def get_recommendation(question):
    rag_helper = RAGHelper()
    
    # Elasticsearch에서 메타데이터 검색
    metadata_results = rag_helper.search_metadata(question)
    context_metadata = "\n".join([md.get("description", "") for md in metadata_results])

    # AI 모델에서 운동 추천과 피드백 생성
    response = openai.ChatCompletion.create(
        model=model_engine,  # 모델 이름을 model 파라미터로 설정
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You provide feedback on exercises and recommend new exercises based on user questions."},
            {"role": "user", "content": question},
            {"role": "assistant", "content": context_metadata}
        ],
        max_tokens=300  # 글자 수 제한을 늘림
    )
    feedback_and_exercise = response['choices'][0]['message']['content'].strip()

    # 식단 추천 추가 (max_tokens를 더 크게 설정하여 긴 식단 추천 받기)
    diet_response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"질문에 대한 답변을 제공한 후 아침, 점심, 저녁, 간식으로 구성된 적합한 식단을 추천해줘: {question}"}
        ],
        max_tokens=500  # 식단을 길게 추천하기 위해 토큰 수 증가
    )
    diet_recommendation = diet_response['choices'][0]['message']['content'].strip()

    # YouTube에서 운동 영상 URL을 검색
    youtube_video_urls = get_youtube_video_urls(feedback_and_exercise)

    return {
        "feedback_and_exercise": feedback_and_exercise,
        "diet_recommendation": diet_recommendation,
        "recommended_videos": youtube_video_urls,  # YouTube 동영상 URL 리스트
        "metadata_reference": metadata_results
    }

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
        except Exception as e:
            print(f"오류 발생: {e}")

if __name__ == "__main__":
    interact_with_ai()
