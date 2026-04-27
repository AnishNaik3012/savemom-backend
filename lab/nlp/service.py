import os
import pickle
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

class LabNLPService:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), "model.h5")
        self.tokenizer_path = os.path.join(os.path.dirname(__file__), "tokenizer.pkl")
        self.model = None
        self.tokenizer = None
        self.label_map = {
            0: "None",
            1: "view_lab_results",
            2: "request_lab_test",
            3: "add_lab_reading",
            4: "interpret_report"
        }
        self._load_artifacts()

    def _load_artifacts(self):
        if os.path.exists(self.model_path) and os.path.exists(self.tokenizer_path):
            try:
                self.model = tf.keras.models.load_model(self.model_path)
                with open(self.tokenizer_path, 'rb') as f:
                    self.tokenizer = pickle.load(f)
                print("Lab NLP Model and Tokenizer loaded successfully.")
            except Exception as e:
                print(f"Error loading Lab NLP artifacts: {e}")
        else:
            print(f"Warning: Lab NLP artifacts not found at {self.model_path} or {self.tokenizer_path}")

    def clean_text(self, text):
        text = str(text).lower().strip()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def predict_intent(self, text: str):
        if self.model is None or self.tokenizer is None:
            return "None", 0.0

        try:
            cleaned = self.clean_text(text)
            seq = self.tokenizer.texts_to_sequences([cleaned])
            padded = pad_sequences(seq, maxlen=25, padding='post')
            
            prediction = self.model.predict(padded, verbose=0)
            intent_id = int(np.argmax(prediction[0]))
            confidence = float(np.max(prediction[0]))
            
            return self.label_map.get(intent_id, "None"), confidence
        except Exception as e:
            print(f"Lab Prediction error: {e}")
            return "None", 0.0

# Singleton instance
nlp_service = LabNLPService()
