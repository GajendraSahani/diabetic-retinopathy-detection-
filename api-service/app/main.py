from fastapi import FastAPI, UploadFile, File, HTTPException
from predictor import ModelPredictor
import os

app = FastAPI(title="Diabetic Retinopathy Analysis API", version="1.0.0")

MODEL_PATH = os.getenv("MODEL_PATH", "./models/efficientnet_aptos.keras")
predictor = None

@app.on_event("startup")
def load_model_instance():
    global predictor
    if os.path.exists(MODEL_PATH):
        predictor = ModelPredictor(MODEL_PATH)
    else:
        print(f"Warning: Weights file target path not found at {MODEL_PATH}")

@app.post("/api/v1/predict")
async def predict_retinopathy(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Invalid extension file payload. Supports PNG/JPG.")
    
    try:
        contents = await file.read()
        if predictor is None:
            return {"status": "mock_mode", "diagnosis": "Moderate", "confidence": 0.88}
        
        result = predictor.predict(contents)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction Engine Failure: {str(e)}")
