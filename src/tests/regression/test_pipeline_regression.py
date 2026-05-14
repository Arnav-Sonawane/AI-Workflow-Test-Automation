import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from pipeline import clean_data, transform_data, validate_data, run_pipeline

PIPELINE_BASELINE_FILE = "pipeline_baseline.json"

# ---- HELPER FUNCTIONS ----

def save_pipeline_baseline(data):
    with open(PIPELINE_BASELINE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n Pipeline baseline saved successfully")

def load_pipeline_baseline():
    with open(PIPELINE_BASELINE_FILE, "r") as f:
        return json.load(f)

# ---- TESTS ----

# Test 1: Save current pipeline output as baseline
def test_create_pipeline_baseline():
    result = run_pipeline()
    save_pipeline_baseline(result)
    assert os.path.exists(PIPELINE_BASELINE_FILE), \
        "Pipeline baseline file was not created"

# Test 2: Check total records in hasnt changed
def test_pipeline_records_in_regression():
    current = run_pipeline()
    baseline = load_pipeline_baseline()

    assert current["total_records_in"] == baseline["total_records_in"], \
        f"Records in changed! Expected {baseline['total_records_in']}, got {current['total_records_in']}"

# Test 3: Check total records out hasnt changed
def test_pipeline_records_out_regression():
    current = run_pipeline()
    baseline = load_pipeline_baseline()

    assert current["total_records_out"] == baseline["total_records_out"], \
        f"Records out changed! Expected {baseline['total_records_out']}, got {current['total_records_out']}"

# Test 4: Check output structure hasnt changed
def test_pipeline_output_structure_regression():
    current = run_pipeline()
    baseline = load_pipeline_baseline()

    current_keys = set(current.keys())
    baseline_keys = set(baseline.keys())

    assert current_keys == baseline_keys, \
        f"Pipeline output structure changed! Missing: {baseline_keys - current_keys}, New: {current_keys - baseline_keys}"

# Test 5: Check each student record structure hasnt changed
def test_pipeline_student_structure_regression():
    current = run_pipeline()
    baseline = load_pipeline_baseline()

    current_student_keys = set(current["output"][0].keys())
    baseline_student_keys = set(baseline["output"][0].keys())

    assert current_student_keys == baseline_student_keys, \
        f"Student record structure changed! Missing: {baseline_student_keys - current_student_keys}"

# Test 6: Check number of students in output hasnt changed
def test_pipeline_output_count_regression():
    current = run_pipeline()
    baseline = load_pipeline_baseline()

    assert len(current["output"]) == len(baseline["output"]), \
        f"Output count changed! Expected {len(baseline['output'])}, got {len(current['output'])}"

# Test 7: Check actual student data hasnt changed
def test_pipeline_output_data_regression():
    current = run_pipeline()
    baseline = load_pipeline_baseline()

    for i, (current_student, baseline_student) in enumerate(
        zip(current["output"], baseline["output"])
    ):
        assert current_student["name"] == baseline_student["name"], \
            f"Student {i} name changed! Expected {baseline_student['name']}, got {current_student['name']}"
        assert current_student["score"] == baseline_student["score"], \
            f"Student {i} score changed! Expected {baseline_student['score']}, got {current_student['score']}"
        assert current_student["age"] == baseline_student["age"], \
            f"Student {i} age changed! Expected {baseline_student['age']}, got {current_student['age']}"