import json
import xml.etree.ElementTree as ET
from elasticsearch import Elasticsearch

# Elasticsearch 설정
es = Elasticsearch("http://localhost:9200")

# XML을 JSON으로 변환하는 함수
def parse_xml_to_json(xml_string):
    ns = {
        'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        'foaf': "http://xmlns.com/foaf/0.1/",
        'dct': "http://purl.org/dc/terms/",
        'dcat': "http://www.w3.org/ns/dcat#",
        'vcard': "http://www.w3.org/2006/vcard/ns#",
        'xml': "http://www.w3.org/XML/1998/namespace"
    }
    root = ET.fromstring(xml_string)
    data = {
        "title_kr": root.find('.//dct:title[@xml:lang="kr"]', ns).text,
        "title_en": root.find('.//dct:title[@xml:lang="en"]', ns).text,
        "description_kr": root.find('.//dct:description[@xml:lang="kr"]', ns).text,
        "description_en": root.find('.//dct:description[@xml:lang="en"]', ns).text,
        "issued_date": root.find('.//dct:issued', ns).text,
        "modified_date": root.find('.//dct:modified', ns).text,
        "publisher": root.find('.//foaf:name', ns).text,
        "contact_phone": root.find('.//vcard:hasTelephone', ns).attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'],
        "theme": root.find('.//dcat:theme', ns).text,
        "keywords_kr": root.find('.//dcat:keyword[@xml:lang="kr"]', ns).text,
        "keywords_en": root.find('.//dcat:keyword[@xml:lang="en"]', ns).text,
        "accrual_periodicity": root.find('.//dct:accrualPeriodicity', ns).text,
        "distribution_format": root.find('.//dcat:format', ns).text
    }
    return data

# Elasticsearch에 인덱싱하는 함수
def index_metadata():
    xml_data = '''<rdf:RDF xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:dct="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dcat="http://www.w3.org/ns/dcat#" xmlns:vcard="http://www.w3.org/2006/vcard/ns#">
    <dcat:Catalog>
    <dcat:dataset>
    <dcat:Dataset>
    <dcat:contactPoint>
    <vcard:Individual>
    <vcard:hasTelephone rdf:resource="tel:02-410-1114"/>
    </vcard:Individual>
    </dcat:contactPoint>
    <dct:description xml:lang="kr">데이터 소개</dct:description>
    <dct:description xml:lang="en">Data Introduction</dct:description>
    <dct:title xml:lang="kr">체력측정 및 운동처방 종합 데이터</dct:title>
    <dct:title xml:lang="en">Comprehensive data on physical fitness measurement and exercise prescription</dct:title>
    <dct:issued rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2022-03-23</dct:issued>
    <dct:modified rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2024-08-19</dct:modified>
    <dct:publisher>
    <foaf:Organization>
    <foaf:name>국민체육진흥공단</foaf:name>
    </foaf:Organization>
    </dct:publisher>
    <dcat:theme>문화관광</dcat:theme>
    <dcat:keyword xml:lang="kr">운동처방,체력측정,체육</dcat:keyword>
    <dcat:keyword xml:lang="en">Exercise prescription, physical fitness test, physical education</dcat:keyword>
    <dct:accrualPeriodicity>수시</dct:accrualPeriodicity>
    <dcat:distribution>
    <dcat:Distribution>
    <dcat:format>json</dcat:format>
    <dcat:title>체력측정 및 운동처방 종합 데이터</dcat:title>
    </dcat:Distribution>
    </dcat:distribution>
    </dcat:Dataset>
    </dcat:dataset>
    </dcat:Catalog>
    </rdf:RDF>'''

    json_data = parse_xml_to_json(xml_data)
    try:
        es.index(index="metadata", document=json_data)
        print("메타데이터 인덱싱 완료")
    except Exception as e:
        print(f"인덱싱 오류: {e}")

if __name__ == "__main__":
    index_metadata()
