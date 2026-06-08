import cv2
import numpy as np
import tensorflow as tf

class ModelPredictor:
    def __init__(self, model_path: str):
        self.model = tf.keras.models.load_model(model_path)
        self.img_size = (224, 224)

    def preprocess(self, image_bytes) -> np.ndarray:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        mask = gray > 10
        img = img[np.ix_(mask.any(1), mask.any(0))]
        
        img = cv2.resize(img, self.img_size)
        img = img.astype(np.float32) / 255.0
        return np.expand_dims(img, axis=0)

    def predict(self, image_bytes):
        processed_img = self.preprocess(image_bytes)
        predictions = self.model.predict(processed_img)
        class_idx = int(np.argmax(predictions, axis=1)[0])
        confidence = float(np.max(predictions))
        
        classes = {
            0: "No Diabetic Retinopathy",
            1: "Mild",
            2: "Moderate",
            3: "Severe",
            4: "Proliferative Diabetic Retinopathy"
        }
        return {"class_id": class_idx, "diagnosis": classes.get(class_idx), "confidence": confidence}
