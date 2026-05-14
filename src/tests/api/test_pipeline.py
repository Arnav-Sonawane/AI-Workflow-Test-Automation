import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline import clean_data, transform_data, validate_data, run_pipeline


# Clean valid data
VALID_DATA = [
    {"name": "Alice", "age": "20", "score": "88"},
    {"name": "Charlie", "age": "19", "score": "95"},
    {"name": "Eve", "age": "21", "score": "65"}
]

# data with missing values
DIRTY_DATA = [
    {"name": "Alice", "age": "20", "score": "88"},
    {"name": "Bob", "age": None, "score": "72"},      
    {"name": "Charlie", "age": "19", "score": "95"},
]

# Data with invalid scores
INVALID_SCORE_DATA = [
    {"name": "Alice", "age": 20, "score": 88},
    {"name": "Diana", "age": 22, "score": 150},       
    {"name": "Eve", "age": 21, "score": -10},         
]

# Test 1: Check that rows with missing values are removed
def test_clean_removes_missing_values():
    result = clean_data(DIRTY_DATA)
    assert len(result) == 2, f"Expected 2 clean rows, got {len(result)}"

# Test 2: Check that clean data passes through untouched
def test_clean_keeps_valid_rows():
    result = clean_data(VALID_DATA)
    assert len(result) == 3, f"Expected 3 rows, got {len(result)}"

# Test 3: Check that empty data returns empty list
def test_clean_handles_empty_data():
    result = clean_data([])
    assert result == [], "Expected empty list for empty input"

# Test 4: Check that age is converted from string to integer
def test_transform_converts_age_to_int():
    result = transform_data(VALID_DATA)
    for row in result:
        assert isinstance(row["age"], int), f"Age should be int, got {type(row['age'])}"

# Test 5: Check that score is converted from string to integer
def test_transform_converts_score_to_int():
    result = transform_data(VALID_DATA)
    for row in result:
        assert isinstance(row["score"], int), f"Score should be int, got {type(row['score'])}"

# Test 6: Check that name is kept as a string
def test_transform_keeps_name_as_string():
    result = transform_data(VALID_DATA)
    for row in result:
        assert isinstance(row["name"], str), f"Name should be string, got {type(row['name'])}"

# ---- STEP 3 TESTS — validate_data ----

# Test 7: Check that scores above 100 are removed
def test_validate_removes_high_scores():
    result = validate_data(INVALID_SCORE_DATA)
    for row in result:
        assert row["score"] <= 100, f"Score {row['score']} should have been removed"

# Test 8: Check that scores below 0 are removed
def test_validate_removes_negative_scores():
    result = validate_data(INVALID_SCORE_DATA)
    for row in result:
        assert row["score"] >= 0, f"Score {row['score']} should have been removed"

# Test 9: Check that valid scores pass through
def test_validate_keeps_valid_scores():
    result = validate_data(INVALID_SCORE_DATA)
    assert len(result) == 1, f"Expected 1 valid row, got {len(result)}"

# ---- FULL PIPELINE TESTS ----

# Test 10: Check full pipeline runs without crashing
def test_pipeline_runs_successfully():
    result = run_pipeline()
    assert result is not None, "Pipeline returned nothing"

# Test 11: Check pipeline output has required fields
def test_pipeline_output_has_required_fields():
    result = run_pipeline()
    assert "output" in result, "Missing field: output"
    assert "total_records_in" in result, "Missing field: total_records_in"
    assert "total_records_out" in result, "Missing field: total_records_out"
    assert "duration_seconds" in result, "Missing field: duration_seconds"

# Test 12: Check pipeline removes bad records
def test_pipeline_filters_bad_records():
    result = run_pipeline()
    assert result["total_records_out"] < result["total_records_in"], \
        "Pipeline should have filtered out some bad records"

# Test 13: Check every output record has valid score
def test_pipeline_output_scores_are_valid():
    result = run_pipeline()
    for student in result["output"]:
        assert 0 <= student["score"] <= 100, \
            f"Invalid score in output: {student['score']}"

# Test 14: Check every output record has correct data types
def test_pipeline_output_correct_types():
    result = run_pipeline()
    for student in result["output"]:
        assert isinstance(student["name"], str), "Name should be string"
        assert isinstance(student["age"], int), "Age should be integer"
        assert isinstance(student["score"], int), "Score should be integer"