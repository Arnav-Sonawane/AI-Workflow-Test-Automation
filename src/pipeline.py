import logging
import time

logger = logging.getLogger(__name__)

# This is our raw student data coming into the pipeline
RAW_DATA = [
    {"name": "Alice", "age": "20", "score": "88"},
    {"name": "Bob", "age": None, "score": "72"}, 
    {"name": "Charlie", "age": "19", "score": "95"},
    {"name": "Diana", "age": "22", "score": "150"},
    {"name": "Eve", "age": "21", "score": "65"},
    {"name": "Frank", "name": None, "age": "23", "score": "78"}
]

# Remove any student that has missing (None) values
def clean_data(data):
    cleaned = [row for row in data if all(v is not None for v in row.values())]
    logger.info(f"Cleaning: {len(data)} rows in → {len(cleaned)} rows out")
    return cleaned

# Convert age and score from strings to actual numbers
def transform_data(data):
    transformed = []
    for row in data:
        transformed.append({
            "name": row.get("name"),
            "age": int(row.get("age")),
            "score": int(row.get("score"))
        })
    logger.info(f"Transforming: converted age and score to integers")
    return transformed

# Check that scores are between 0 and 100
def validate_data(data):
    valid = [row for row in data if 0 <= row["score"] <= 100]
    invalid = [row for row in data if not (0 <= row["score"] <= 100)]
    if invalid:
        logger.warning(f"Validation: removed {len(invalid)} rows with invalid scores")
    return valid

# This connects all 3 steps together
def run_pipeline(data=None):
    if data is None:
        data = RAW_DATA
    
    start = time.time()
    
    step1 = clean_data(data)
    step2 = transform_data(step1)
    step3 = validate_data(step2)
    
    end = time.time()
    
    result = {
        "output": step3,
        "total_records_in": len(data),
        "total_records_out": len(step3),
        "duration_seconds": round(end - start, 4)
    }
    
    return result