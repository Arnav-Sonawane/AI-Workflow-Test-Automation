import pytest
from fastapi.testclient import TestClient
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json
import os
import requests

from app.main import app
from utils.config import get_setting

ENVIRONMENT = get_setting("environment", "local")
BASE_URL = get_setting("api.base_url")

client = TestClient(app)

# Load schemas
SCHEMAS_DIR = get_setting(
    "paths.schemas_dir",
    "schemas"
)

with open(os.path.join(SCHEMAS_DIR, "ingest_schema.json")) as f:
    ingest_schema = json.load(f)

with open(os.path.join(SCHEMAS_DIR, "predict_schema.json")) as f:
    predict_schema = json.load(f)


def api_post(endpoint, payload):
    """
    Switch automatically between:
    - local TestClient
    - deployed Render API
    """

    if ENVIRONMENT == "deployed":
        return requests.post(
            f"{BASE_URL}{endpoint}",
            json=payload
        )

    return client.post(endpoint, json=payload)


@pytest.mark.api
@pytest.mark.schema
def test_ingest_success_and_schema():
    payload = [
        {
            "name": "Alice",
            "age": 20,
            "score": 88
        }
    ]

    response = api_post(
        "/api/v1/ingest",
        payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    try:
        validate(
            instance=data,
            schema=ingest_schema
        )
    except ValidationError as e:
        pytest.fail(
            f"Schema validation failed: {e}"
        )


@pytest.mark.api
@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ([], 400),
        ([{"age": {"invalid": "dict"}}], 422),
        ({}, 422),
        (
            [{
                "name": None,
                "age": None,
                "score": None
            }],
            200
        ),
    ]
)
def test_ingest_edge_cases(
    payload,
    expected_status
):
    response = api_post(
        "/api/v1/ingest",
        payload
    )

    assert response.status_code == expected_status


@pytest.mark.api
@pytest.mark.schema
def test_predict_success_and_schema():
    payload = [
        {
            "name": "Alice",
            "age": 20,
            "score": 88
        }
    ]

    response = api_post(
        "/api/v1/predict",
        payload
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Alice"

    try:
        validate(
            instance=data,
            schema=predict_schema
        )
    except ValidationError as e:
        pytest.fail(
            f"Schema validation failed: {e}"
        )


@pytest.mark.api
@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ([{"name": "Bob"}], 422),
        (
            [{
                "name": "Bob",
                "age": "twenty",
                "score": 50
            }],
            422
        ),
        ([], 200),
    ]
)
def test_predict_edge_cases(
    payload,
    expected_status
):
    response = api_post(
        "/api/v1/predict",
        payload
    )

    assert response.status_code == expected_status