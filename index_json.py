import os
import json
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import RequestError

# Elasticsearch 설정
es = Elasticsearch("http://localhost:9200")

# 인덱스가 없다면 생성하는 함수
def create_index_if_not_exists(index_name):
    if not es.indices.exists(index=index_name):
        mapping = {
            "properties": {
                "MBER_SEQ_NO_VALUE": {"type": "text"},
                "MESURE_SEQ_NO": {"type": "text"},
                "CNTER_NM": {"type": "text"},
                "AGRDE_FLAG_NM": {"type": "text"},
                "MESURE_PLACE_FLAG_NM": {"type": "text"},
                "MESURE_AGE_CO": {"type": "integer"},
                "INPT_FLAG_NM": {"type": "text"},
                "CRTFC_FLAG_NM": {"type": "text"},
                "MESURE_DE": {"type": "date", "format": "yyyyMMdd"},
                "SEXDSTN_FLAG_CD": {"type": "text"},
                "MESURE_IEM_001_VALUE": {"type": "float"},
            }
        }
        es.indices.create(index=index_name, body={"mappings": mapping})
        print(f"'{index_name}' 인덱스가 생성되었습니다.")

# JSON 파일을 Elasticsearch에 인덱싱하는 함수
def index_json_file(file_path, index_name="json_data"):
    try:
        if os.path.getsize(file_path) == 0:
            print(f"File {file_path} is empty. Skipping.")
            return

        print(f"Opening file: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                documents = json.load(f)
                if not documents:
                    print(f"No relevant JSON content found in {file_path}.")
                    return

                print(f"Loaded JSON data from {file_path}. Document count: {len(documents)}")
                if not isinstance(documents, list):
                    print(f"Error: JSON data in {file_path} is not a list. Skipping file.")
                    return
            except json.JSONDecodeError as e:
                print(f"Invalid JSON in file {file_path}: {e}")
                return

        create_index_if_not_exists(index_name)

        actions = []
        new_docs_count = 0
        for i, doc in enumerate(documents):
            document_id = doc.get("MBER_SEQ_NO_VALUE")
            if document_id is None:
                continue

            action = {
                "_index": index_name,
                "_id": document_id,
                "_source": doc
            }
            actions.append(action)

            # 1000개마다 bulk 인덱싱
            if len(actions) == 1000:
                helpers.bulk(es, actions)
                new_docs_count += len(actions)
                actions = []
                print(f"Indexed {new_docs_count} documents so far...")

        # 남은 문서들 인덱싱
        if actions:
            helpers.bulk(es, actions)
            new_docs_count += len(actions)

        print(f"'{file_path}' 인덱싱 완료 - 총 인덱싱된 문서: {new_docs_count}개")

    except Exception as e:
        print(f"파일을 여는 중 오류가 발생했습니다: {e}")

# JSON 폴더에 있는 JSON 파일 목록을 가져옵니다
def index_json_files_from_folder(json_folder, index_name="json_data"):
    try:
        json_files = [os.path.join(json_folder, f) for f in os.listdir(json_folder) if f.endswith(".json")]
        if not json_files:
            print(f"No JSON files found in folder {json_folder}.")
            return

        for json_file in json_files:
            print(f"Processing file: {json_file}")
            index_json_file(json_file, index_name)
    except Exception as e:
        print(f"폴더에서 JSON 파일을 가져오는 중 오류 발생: {e}")

if __name__ == "__main__":
    json_folder = "json"  # JSON 파일이 있는 폴더
    index_json_files_from_folder(json_folder)
