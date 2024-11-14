from elasticsearch import Elasticsearch

# RAGHelper 클래스
class RAGHelper:
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")

    def search_documents(self, query):
        results = self.es.search(index="exercise_videos", body={"query": {"match": {"content": query}}})
        return [hit["_source"]["content"] for hit in results["hits"]["hits"]]

def search_metadata(self, query):
    # Elasticsearch에서 메타데이터 검색 (title과 description을 모두 포함)
    results = self.es.search(index="metadata", body={
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "description", "keywords"]
            }
        },
        "_source": ["title", "description", "keywords"]  # 필요한 필드만 검색
    })
    return [hit["_source"] for hit in results["hits"]["hits"]]
