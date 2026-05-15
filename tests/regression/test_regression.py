import pytest
import json
import os
from pipeline.core import run_pipeline
from utils.config import get_setting

DATA_DIR = get_setting("paths.data_dir", "tests/data")

@pytest.mark.regression
def test_pipeline_regression():
    # Since confidence is seeded now, outputs should be consistent
    result = run_pipeline()
    
    baseline_path = os.path.join(DATA_DIR, "pipeline_baseline.json")
    
    # If baseline doesn't exist, create it (usually done once)
    if not os.path.exists(baseline_path):
        with open(baseline_path, "w") as f:
            json.dump(result, f, indent=2)
        pytest.skip("Baseline created. Run again to test regression.")
        
    with open(baseline_path, "r") as f:
        baseline = json.load(f)
        
    assert result["total_records_out"] == baseline["total_records_out"]
    assert len(result["output"]) == len(baseline["output"])
    
    # Check that predictions and logic haven't drifted
    for i in range(len(result["output"])):
        assert result["output"][i]["prediction"] == baseline["output"][i]["prediction"]
        # Allow small float differences in confidence
        assert abs(result["output"][i]["confidence"] - baseline["output"][i]["confidence"]) < 0.01
