import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from pipeline import clean_data, transform_data, validate_data, run_pipeline

# Maximum allowed time for each operation (in seconds)
MAX_PIPELINE_TIME = 2.0
MAX_STEP_TIME = 0.5

# Large dataset to stress test the pipeline
LARGE_DATA = [
    {"name": f"Student_{i}", "age": str(18 + (i % 10)), "score": str(50 + (i % 50))}
    for i in range(1000)
]

# ---- TESTS ----

# Test 1: Check full pipeline completes within time limit
def test_full_pipeline_performance():
    start = time.time()
    result = run_pipeline()
    end = time.time()

    duration = end - start
    print(f"\n Full pipeline completed in: {duration:.4f} seconds")

    assert duration < MAX_PIPELINE_TIME, \
        f"Pipeline too slow! Took {duration:.2f}s, limit is {MAX_PIPELINE_TIME}s"

# Test 2: Check cleaning step is fast enough
def test_clean_step_performance():
    start = time.time()
    clean_data(LARGE_DATA)
    end = time.time()

    duration = end - start
    print(f"\n Clean step completed in: {duration:.4f} seconds for 1000 records")

    assert duration < MAX_STEP_TIME, \
        f"Clean step too slow! Took {duration:.2f}s, limit is {MAX_STEP_TIME}s"

# Test 3: Check transform step is fast enough
def test_transform_step_performance():
    cleaned = clean_data(LARGE_DATA)

    start = time.time()
    transform_data(cleaned)
    end = time.time()

    duration = end - start
    print(f"\n Transform step completed in: {duration:.4f} seconds for 1000 records")

    assert duration < MAX_STEP_TIME, \
        f"Transform step too slow! Took {duration:.2f}s, limit is {MAX_STEP_TIME}s"

# Test 4: Check validate step is fast enough
def test_validate_step_performance():
    cleaned = clean_data(LARGE_DATA)
    transformed = transform_data(cleaned)

    start = time.time()
    validate_data(transformed)
    end = time.time()

    duration = end - start
    print(f"\n Validate step completed in: {duration:.4f} seconds for 1000 records")

    assert duration < MAX_STEP_TIME, \
        f"Validate step too slow! Took {duration:.2f}s, limit is {MAX_STEP_TIME}s"

# Test 5: Check pipeline performance across 10 runs
def test_pipeline_consistent_performance():
    times = []

    for i in range(10):
        start = time.time()
        run_pipeline()
        end = time.time()
        times.append(end - start)

    average = sum(times) / len(times)
    fastest = min(times)
    slowest = max(times)

    print(f"\n Pipeline over 10 runs:")
    print(f"   Average: {average:.4f}s")
    print(f"   Fastest: {fastest:.4f}s")
    print(f"   Slowest: {slowest:.4f}s")

    assert average < MAX_PIPELINE_TIME, \
        f"Average too slow: {average:.2f}s"