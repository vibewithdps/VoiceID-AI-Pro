from dataclasses import dataclass
from pathlib import Path

import numpy as np

try:
	import joblib
except Exception:  # pragma: no cover
	joblib = None

from app.database.database import Database
from app.database.history_repository import HistoryRepository
from app.ml.feature_extractor import FeatureExtractor


MODELS_DIR = Path("models")


@dataclass
class PredictionResult:
	speaker: str
	confidence: float
	probabilities: dict
	model_name: str


class SpeakerPredictor:

	def __init__(self, model_path=None, label_encoder_path=None, scaler_path=None):
		self.model_path = Path(model_path) if model_path else MODELS_DIR / "voice_model.pkl"
		self.label_encoder_path = Path(label_encoder_path) if label_encoder_path else MODELS_DIR / "label_encoder.pkl"
		self.scaler_path = Path(scaler_path) if scaler_path else MODELS_DIR / "scaler.pkl"

		self.db = Database()
		self.history = HistoryRepository(self.db)

		self.model = None
		self.label_encoder = None
		self.scaler = None

	def load(self):
		if joblib is None:
			raise RuntimeError("joblib is required to load trained model artifacts.")

		if not self.model_path.exists() or not self.label_encoder_path.exists() or not self.scaler_path.exists():
			raise FileNotFoundError("Trained model artifacts are missing.")

		self.model = joblib.load(self.model_path)
		self.label_encoder = joblib.load(self.label_encoder_path)
		self.scaler = joblib.load(self.scaler_path)
		return self

	def predict(self, audio_path):
		if self.model is None:
			self.load()

		features = FeatureExtractor.extract(audio_path)
		features = np.asarray(features, dtype=np.float32).reshape(1, -1)
		scaled = self.scaler.transform(features)

		prediction_index = self.model.predict(scaled)[0]
		speaker = self.label_encoder.inverse_transform([prediction_index])[0]

		probabilities = self._probabilities(scaled)[0]
		confidence = float(np.max(probabilities)) * 100.0

		result = PredictionResult(
			speaker=speaker,
			confidence=confidence,
			probabilities={self.label_encoder.inverse_transform([index])[0]: float(probability) for index, probability in enumerate(probabilities)},
			model_name=self.model_path.name,
		)

		self.history.create_prediction(None, Path(audio_path).name, result.speaker, result.confidence)
		return result

	def _probabilities(self, scaled_features):
		if hasattr(self.model, "predict_proba"):
			return self.model.predict_proba(scaled_features)

		decision = self.model.decision_function(scaled_features)
		if decision.ndim == 1:
			decision = np.vstack([-decision, decision]).T
		exp = np.exp(decision - np.max(decision, axis=1, keepdims=True))
		return exp / np.sum(exp, axis=1, keepdims=True)

