import cv2
import numpy as np
import tensorflow as tf

class ProductionPredictor:
    def __init__(self, model_path: str):
        self.model = tf.keras.models.load_model(model_path)
        self.img_size = (224, 224)
        self.classes = {
            0: "No Diabetic Retinopathy",
            1: "Mild",
            2: "Moderate",
            3: "Severe",
            4: "Proliferative Diabetic Retinopathy"
        }

    def execute_inference_preprocessing(self, image_bytes) -> np.ndarray:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Black border cropping
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        mask = gray > 10
        if np.any(mask):
            img = img[np.ix_(mask.any(1), mask.any(0))]
            
        lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        lab = cv2.merge((l, a, b))
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        
        img = cv2.GaussianBlur(img, (5, 5), 0)
        img = cv2.resize(img, self.img_size)
        img = img.astype(np.float32) / 255.0
        
        return np.expand_dims(img, axis=0)

    def generate_prediction_output(self, image_bytes) -> dict:
        processed_tensor = self.execute_inference_preprocessing(image_bytes)
        predictions = self.model.predict(processed_tensor)
        class_id = int(np.argmax(predictions, axis=1)[0])
        confidence_score = float(np.max(predictions))
        
        return {
            "class_id": class_id,
            "diagnosis": self.classes.get(class_id, "Unknown"),
            "confidence": confidence_score,
            "raw_scores": predictions.tolist()[0]
        }
