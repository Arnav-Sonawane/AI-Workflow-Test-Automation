from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time
import random
from utils.logger import app_logger as logger


app = FastAPI(title="Mock AI Workflow API", version="1.0.0")

class StudentRecord(BaseModel):
    name: Optional[str] = None
    age: Optional[str | int] = None
    score: Optional[str | int] = None

class IngestResponse(BaseModel):
    status: str
    message: str
    records_received: int

class PredictRequest(BaseModel):
    name: str
    age: int
    score: int

class PredictResponse(BaseModel):
    name: str
    prediction: str
    confidence: float

@app.post("/api/v1/ingest", response_model=IngestResponse)
async def ingest_data(data: List[StudentRecord]):
    """Simulates data ingestion from external sources."""
    if not data:
        raise HTTPException(status_code=400, detail="Empty data payload")
    
    logger.info(f"Ingested {len(data)} records")
    return {
        "status": "success",
        "message": "Data successfully ingested into the pipeline.",
        "records_received": len(data)
    }

@app.post("/api/v1/predict", response_model=List[PredictResponse])
async def predict(data: List[PredictRequest]):
    """Simulates a deployed Machine Learning model inference."""
    results = []
    for row in data:
        # Simulate slight delay
        time.sleep(0.01)
        
        # Simple dummy logic
        prediction = "Pass" if row.score >= 50 else "Fail"
        confidence = round(random.uniform(0.70, 0.99), 2)
        
        results.append({
            "name": row.name,
            "prediction": prediction,
            "confidence": confidence
        })
    
    logger.info(f"Generated predictions for {len(data)} records")
    return results

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "uptime_seconds": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
