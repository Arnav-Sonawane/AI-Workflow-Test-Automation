import pytest
from jsonschema import validate, ValidationError

# Example schema for AI workflow output
prediction_schema = {
    "type": "object",
    "properties": {
        "student_id": {"type": "integer"},
        "prediction": {
            "type": "string",
            "enum": ["Pass", "Fail"]
        },
        "confidence_score": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0
        },
        "risk_level": {
            "type": "string",
            "enum": ["Low", "Medium", "High"]
        }
    },
    "required": [
        "student_id",
        "prediction",
        "confidence_score",
        "risk_level"
    ]
}


@pytest.mark.schema
def test_valid_prediction_schema():
    """
    Validate correct AI workflow output structure.
    """

    sample_output = {
        "student_id": 101,
        "prediction": "Pass",
        "confidence_score": 0.89,
        "risk_level": "Low"
    }

    validate(instance=sample_output, schema=prediction_schema)


@pytest.mark.schema
def test_invalid_prediction_schema():
    """
    Validate incorrect schema fails properly.
    """

    invalid_output = {
        "student_id": "101",  # wrong type
        "prediction": "Unknown",  # invalid enum
        "confidence_score": 1.5,  # out of range
    }

    with pytest.raises(ValidationError):
        validate(instance=invalid_output, schema=prediction_schema)