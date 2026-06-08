from fastapi import FastAPI, UploadFile, File, HTTPException
from predictor import ProductionPredictor
import os

app = FastAPI(title="Diabetic Retinopathy Microservice API Layer", version="2.0.0")

MODEL_PATH = os.getenv("MODEL_PATH", "./models/efficientnet_aptos.keras")
ai_engine = None

@app.on_event("startup")
def verify_and_load_model():
    global ai_engine
    if os.path.exists(MODEL_PATH):
        ai_engine = ProductionPredictor(MODEL_PATH)
    else:
        print(f"Warning: Production weights asset file not found locally at {MODEL_PATH}. Active simulation mode fallback.")

@app.post("/api/v1/predict")
async def register_inference_request(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Invalid data type. Retinal scans must be PNG or JPG.")
    
    try:
        content_stream = await file.read()
        if ai_engine is None:
            return {"class_id": 0, "diagnosis": "No Diabetic Retinopathy (Simulated)", "confidence": 0.94}
        
        return ai_engine.generate_prediction_output(content_stream)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Inference Engine Error: {str(e)}")
