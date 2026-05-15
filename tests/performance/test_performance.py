import pytest
import time
from fastapi.testclient import TestClient
from app.main import app
from pipeline.core import run_pipeline
from utils.config import get_setting

client = TestClient(app)

MAX_API_LATENCY = get_setting("performance.max_api_latency_seconds", 0.5)
MAX_PIPELINE_DURATION = get_setting("performance.max_pipeline_duration_seconds", 1.0)

@pytest.mark.performance
def test_api_predict_latency():
    payload = [{"name": "Alice", "age": 20, "score": 88} for _ in range(10)]
    start = time.time()
    response = client.post("/api/v1/predict", json=payload)
    end = time.time()
    
    assert response.status_code == 200
    latency = end - start
    assert latency < MAX_API_LATENCY, f"API latency {latency}s exceeded threshold {MAX_API_LATENCY}s"

@pytest.mark.performance
def test_pipeline_execution_time():
    result = run_pipeline()
    duration = result["duration_seconds"]
    
    assert duration < MAX_PIPELINE_DURATION, f"Pipeline duration {duration}s exceeded threshold {MAX_PIPELINE_DURATION}s"
