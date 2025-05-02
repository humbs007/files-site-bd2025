from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_status_code():
    payload = {
        "tables": ["table_enel"],
        "field": "PN_CPF",
        "operator": "=",
        "term": "28545840829"
    }
    response = client.post("/search/option1", json=payload)
    assert response.status_code in [200, 404]

def test_search_valid_result_structure():
    payload = {
        "tables": ["table_enel"],
        "field": "PN_CPF",
        "operator": "=",
        "term": "28545840829"
    }
    response = client.post("/search/option1", json=payload)
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, dict)
        assert "results" in data
