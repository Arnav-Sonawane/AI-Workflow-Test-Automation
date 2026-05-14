import pytest
from fastapi.testclient import TestClient
import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app import app

client = TestClient(app)

BASELINE_MEAN_CONFIDENCE = 0.85
DRIFT_TOLERANCE = 0.15

def test_prediction_confidence_drift():
    payload = [
        {"name": "Student1", "age": 20, "score": 90},
        {"name": "Student2", "age": 21, "score": 85},
        {"name": "Student3", "age": 19, "score": 40},
        {"name": "Student4", "age": 22, "score": 60},
        {"name": "Student5", "age": 20, "score": 50}
    ]
    
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200, "API request failed"
    
    data = response.json()
    confidences = [item["confidence"] for item in data]
    
    mean_confidence = np.mean(confidences)
    
    drift = abs(mean_confidence - BASELINE_MEAN_CONFIDENCE)
    
    assert drift <= DRIFT_TOLERANCE, \
        f"Data Drift Detected! Mean confidence {mean_confidence:.2f} drifted from baseline {BASELINE_MEAN_CONFIDENCE} by {drift:.2f} (Tolerance: {DRIFT_TOLERANCE})"
