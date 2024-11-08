import requests

url = "http://127.0.0.1:8000/exercise_recommendation/"
data = {
    "reps": 15,
    "sets": 5,
    "target_area": "체력단련"  # 또는 상체, 전신 등
}

response = requests.post(url, json=data)
print(response.json())
