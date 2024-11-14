import os
from elasticsearch import Elasticsearch
import PyPDF2

# Elasticsearch 설정
es = Elasticsearch("http://localhost:9200")

# PDF에서 텍스트 추출하는 함수
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# PDF 파일을 Elasticsearch에 인덱싱하는 함수
def index_pdf_text(pdf_path, document_id):
    # PDF에서 텍스트 추출
    text = extract_text_from_pdf(pdf_path)
    
    # 추출된 텍스트와 파일 경로를 Elasticsearch에 저장
    document = {
        "text": text,
        "file_path": pdf_path  # 파일 경로 저장
    }
    
    try:
        es.index(index="pdf_documents", id=document_id, document=document)
        print(f"PDF 문서 인덱싱 완료: {document_id}")
    except Exception as e:
        print(f"인덱싱 오류: {e}")

# 두 개의 PDF 파일을 처리하는 함수
def process_multiple_pdfs(pdf_files):
    for pdf_file in pdf_files:
        document_id = os.path.basename(pdf_file)  # 파일 이름을 document ID로 사용
        index_pdf_text(pdf_file, document_id)

if __name__ == "__main__":
    # pdfs 폴더에 있는 PDF 파일 목록을 가져옵니다
    pdf_folder = "pdfs/"
    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    
    # 두 개의 PDF 파일을 처리
    process_multiple_pdfs(pdf_files)
