import joblib
import numpy as np

class IntentModel:
    def __init__(self, path="model/artifacts/intent_model.pkl", threshold=0.5):
        self.pipeline = joblib.load(path)
        self.threshold = threshold  # The minimum confidence required

    def predict(self, text):
        # Get probabilities for all classes
        probs = self.pipeline.predict_proba([text])[0]
        
        # Find the index of the highest probability
        max_idx = np.argmax(probs)
        confidence = probs[max_idx]
        
        # Check if the highest probability meets our requirement
        if confidence < self.threshold:
            return {
                "intent": "unknown", 
                "confidence": round(float(confidence), 4),
                "message": "I'm not quite sure what you mean."
            }
        
        # Otherwise, return the predicted class
        pred = self.pipeline.classes_[max_idx]
        return {
            "intent": pred, 
            "confidence": round(float(confidence), 4)
        }

# --- Quick Test ---
# model = IntentModel(threshold=0.5)
# print(model.predict("blue bananas fly fast")) 
# Result: {'intent': 'unknown', 'confidence': 0.22, ...}