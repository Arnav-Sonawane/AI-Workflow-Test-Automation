import requests
import json
import os

BASE_URL = "https://jsonplaceholder.typicode.com"
BASELINE_FILE = "baseline.json"

def save_baseline(data):
    with open(BASELINE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n Baseline saved successfully")

def load_baseline():
    with open(BASELINE_FILE, "r") as f:
        return json.load(f)

def test_create_baseline():
    response = requests.get(f"{BASE_URL}/posts/1")
    data = response.json()
    save_baseline(data)
    assert os.path.exists(BASELINE_FILE), "Baseline file was not created"

def test_regression_check():
    response = requests.get(f"{BASE_URL}/posts/1")
    current_data = response.json()
    baseline_data = load_baseline()

    assert current_data["id"] == baseline_data["id"], \
        f"ID changed! Expected {baseline_data['id']}, got {current_data['id']}"
    
    assert current_data["title"] == baseline_data["title"], \
        f"Title changed! Expected '{baseline_data['title']}', got '{current_data['title']}'"
    
    assert current_data["userId"] == baseline_data["userId"], \
        f"userId changed! Expected {baseline_data['userId']}, got {current_data['userId']}"
    
    print(f"\n No regression detected - current output matches baseline")

def test_structure_regression():
    response = requests.get(f"{BASE_URL}/posts/1")
    current_data = response.json()
    baseline_data = load_baseline()

    current_keys = set(current_data.keys())
    baseline_keys = set(baseline_data.keys())

    assert current_keys == baseline_keys, \
        f"Structure changed! Missing: {baseline_keys - current_keys}, New: {current_keys - baseline_keys}"
    
    print(f"\n Structure unchanged - all fields match baseline")