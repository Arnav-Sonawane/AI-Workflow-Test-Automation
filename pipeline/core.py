import time
import random
from utils.logger import pipeline_logger as logger
from utils.config import get_setting

# This is our raw data coming into the pipeline
RAW_DATA = [
    {"name": "Alice", "age": "20", "score": "88"},
    {"name": "Bob", "age": None, "score": "72"}, 
    {"name": "Charlie", "age": "19", "score": "95"},
    {"name": "Diana", "age": "22", "score": "150"},
    {"name": "Eve", "age": "21", "score": "65"},
    {"name": "Frank", "name": None, "age": "23", "score": "78"}
]

# 1. Data Ingestion
def data_ingestion(data=None):
    data = data if data is not None else RAW_DATA
    logger.info(f"Ingested {len(data)} records")
    return data

# 2. Preprocessing
def preprocessing(data):
    cleaned = [row for row in data if all(v is not None for v in row.values())]
    logger.info(f"Preprocessing: {len(data)} rows in → {len(cleaned)} rows out")
    return cleaned

# 3. Feature Transformation
def feature_transformation(data):
    transformed = []
    for row in data:
        transformed.append({
            "name": row.get("name"),
            "age": int(row.get("age")),
            "score": int(row.get("score"))
        })
    logger.info(f"Feature Transformation: converted age and score to integers")
    return transformed

# 4. Model Inference
def model_inference(data):
    predictions = []
    for row in data:
        prediction = "Pass" if row["score"] >= 50 else "Fail"
        # Seed the random based on score for stable tests if needed, or just keep it random.
        # But wait, regression tests compare baselines! If confidence is random, baseline equality checks will fail.
        # I should use a seeded random or a deterministic value for confidence for testability, or just random with seed.
        random.seed(row["score"] + row["age"])
        confidence = round(random.uniform(0.70, 0.99), 2)
        
        predictions.append({
            **row,
            "prediction": prediction,
            "confidence": confidence
        })
    logger.info(f"Model Inference: generated predictions for {len(data)} records")
    return predictions

# 5. Prediction Validation
def prediction_validation(data):
    min_score = get_setting("pipeline.score_min", 0)
    max_score = get_setting("pipeline.score_max", 100)
    conf_thresh = get_setting("pipeline.confidence_threshold", 0.70)
    
    valid = []
    for row in data:
        if min_score <= row["score"] <= max_score and row["confidence"] >= conf_thresh:
            valid.append(row)
        else:
            logger.warning(f"Validation failure for record: {row['name']} (Score: {row['score']}, Conf: {row['confidence']})")
    return valid

# 6. Output Generation
def output_generation(data, start_time, total_in):
    end_time = time.time()
    result = {
        "output": data,
        "total_records_in": total_in,
        "total_records_out": len(data),
        "duration_seconds": round(end_time - start_time, 4)
    }
    logger.info(f"Output Generation: {result['total_records_out']} valid records out of {total_in}. Took {result['duration_seconds']}s")
    return result

def run_pipeline(data=None):
    start = time.time()
    
    step1 = data_ingestion(data)
    total_in = len(step1)
    
    step2 = preprocessing(step1)
    step3 = feature_transformation(step2)
    step4 = model_inference(step3)
    step5 = prediction_validation(step4)
    
    return output_generation(step5, start, total_in)