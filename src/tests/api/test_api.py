import pytest
from fastapi.testclient import TestClient
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json
import os
import sys

# Add src directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app import app

client = TestClient(app)

def load_schema(schema_name):
    schema_path = os.path.join(os.path.dirname(__file__), '../data', schema_name)
    with open(schema_path, 'r') as file:
        return json.load(file)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_ingest_data():
    payload = [
        {"name": "Alice", "age": 20, "score": 88},
        {"name": "Bob", "age": 21, "score": 75}
    ]
    response = client.post("/api/v1/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["records_received"] == 2

def test_predict_schema_validation():
    payload = [
        {"name": "Alice", "age": 20, "score": 88},
        {"name": "Bob", "age": 21, "score": 40}
    ]
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    schema = load_schema("predict_schema.json")
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        pytest.fail(f"JSON Schema validation failed: {e.message}")

def test_ingest_empty_data():
    response = client.post("/api/v1/ingest", json=[])
    assert response.status_code == 400