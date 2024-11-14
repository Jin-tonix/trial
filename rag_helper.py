from elasticsearch import Elasticsearch

# RAGHelper 클래스
class RAGHelper:
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")

    def search_documents(self, query):
        # exercise_videos 인덱스에서 콘텐츠 검색
        results = self.es.search(index="exercise_videos", body={
            "query": {
                "match": {
                    "content": query
                }
            }
        })
        return [hit["_source"]["content"] for hit in results["hits"]["hits"]]

    def search_metadata(self, query):
        # Elasticsearch에서 메타데이터 검색 (title, description, keywords를 포함)
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

    def search_pdf_documents(self, query):
        # Elasticsearch에서 PDF 문서에서 텍스트 검색
        results = self.es.search(index="pdf_documents", body={
            "query": {
                "match": {
                    "text": query
                }
            }
        })
        return [hit["_source"]["text"] for hit in results["hits"]["hits"]]  # PDF에서 추출한 텍스트를 반환
