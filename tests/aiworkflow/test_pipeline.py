import pytest
from pipeline.core import (
    data_ingestion,
    preprocessing,
    feature_transformation,
    model_inference,
    prediction_validation,
    run_pipeline
)

@pytest.mark.pipeline
def test_data_ingestion():
    data = data_ingestion()
    assert len(data) > 0

@pytest.mark.pipeline
@pytest.mark.aiworkflow
def test_preprocessing():
    raw = [{"name": "A", "age": "20", "score": "80"}, {"name": "B", "age": None, "score": "70"}]
    cleaned = preprocessing(raw)
    assert len(cleaned) == 1
    assert cleaned[0]["name"] == "A"

@pytest.mark.pipeline
@pytest.mark.aiworkflow
def test_feature_transformation():
    cleaned = [{"name": "A", "age": "20", "score": "80"}]
    transformed = feature_transformation(cleaned)
    assert transformed[0]["age"] == 20
    assert transformed[0]["score"] == 80

@pytest.mark.pipeline
@pytest.mark.aiworkflow
def test_model_inference():
    transformed = [{"name": "A", "age": 20, "score": 80}, {"name": "B", "age": 21, "score": 40}]
    predictions = model_inference(transformed)
    assert len(predictions) == 2
    assert predictions[0]["prediction"] == "Pass"
    assert predictions[1]["prediction"] == "Fail"
    assert "confidence" in predictions[0]

@pytest.mark.pipeline
@pytest.mark.aiworkflow
def test_prediction_validation():
    preds = [
        {"name": "A", "score": 80, "confidence": 0.85}, # Valid
        {"name": "B", "score": -10, "confidence": 0.90}, # Invalid score
        {"name": "C", "score": 50, "confidence": 0.50}, # Low confidence
    ]
    valid = prediction_validation(preds)
    assert len(valid) == 1
    assert valid[0]["name"] == "A"

@pytest.mark.pipeline
@pytest.mark.aiworkflow
def test_run_pipeline():
    result = run_pipeline()
    assert "output" in result
    assert "total_records_in" in result
    assert "total_records_out" in result
    assert "duration_seconds" in result
    assert result["total_records_in"] >= result["total_records_out"]
