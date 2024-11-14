import openai
import os

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 세션 새로 시작하기 (기본적으로 새 요청 시 새로 시작됨)
def reset_openai_session():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    print("OpenAI 세션을 새로 시작했습니다.")

reset_openai_session()
