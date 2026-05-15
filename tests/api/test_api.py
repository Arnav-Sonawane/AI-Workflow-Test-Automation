import pytest
from fastapi.testclient import TestClient
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json
import os
from app.main import app
from utils.config import get_setting

client = TestClient(app)

# Load schemas
SCHEMAS_DIR = get_setting("paths.schemas_dir", "schemas")

with open(os.path.join(SCHEMAS_DIR, "ingest_schema.json")) as f:
    ingest_schema = json.load(f)

with open(os.path.join(SCHEMAS_DIR, "predict_schema.json")) as f:
    predict_schema = json.load(f)

@pytest.mark.api
@pytest.mark.schema
def test_ingest_success_and_schema():
    payload = [{"name": "Alice", "age": 20, "score": 88}]
    response = client.post("/api/v1/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # Schema validation
    try:
        validate(instance=data, schema=ingest_schema)
    except ValidationError as e:
        pytest.fail(f"Schema validation failed: {e}")

@pytest.mark.api
@pytest.mark.parametrize("payload, expected_status", [
    ([], 400), # Empty payload
    ([{"age": {"invalid": "dict"}}], 422), # Invalid field type for age
    ({}, 422), # Malformed dict instead of list
    ([{"name": None, "age": None, "score": None}], 200), # Null values are allowed
])
def test_ingest_edge_cases(payload, expected_status):
    response = client.post("/api/v1/ingest", json=payload)
    assert response.status_code == expected_status

@pytest.mark.api
@pytest.mark.schema
def test_predict_success_and_schema():
    payload = [{"name": "Alice", "age": 20, "score": 88}]
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["name"] == "Alice"
    
    # Schema validation
    try:
        validate(instance=data, schema=predict_schema)
    except ValidationError as e:
        pytest.fail(f"Schema validation failed: {e}")

@pytest.mark.api
@pytest.mark.parametrize("payload, expected_status", [
    ([{"name": "Bob"}], 422), # Missing required fields (age, score)
    ([{"name": "Bob", "age": "twenty", "score": 50}], 422), # Invalid field type
    ([], 200), # Empty list might be valid for predict (returns empty list)
])
def test_predict_edge_cases(payload, expected_status):
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == expected_status
