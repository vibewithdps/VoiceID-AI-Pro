from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import json

import joblib
import numpy as np

try:
	from sklearn.ensemble import RandomForestClassifier
	from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
	from sklearn.model_selection import train_test_split
	from sklearn.preprocessing import LabelEncoder, StandardScaler
	from sklearn.svm import SVC
except Exception:  # pragma: no cover - runtime fallback if sklearn is unavailable
	RandomForestClassifier = None
	SVC = None
	LabelEncoder = None
	StandardScaler = None

from app.audio.audio_utils import is_audio_file
from app.database.database import Database
from app.database.history_repository import HistoryRepository
from app.ml.feature_extractor import FeatureExtractor


MODELS_DIR = Path("models")


@dataclass
class TrainingResult:
	best_algorithm: str
	accuracy: float
	metrics: dict
	report: dict
	model_path: str
	label_encoder_path: str
	scaler_path: str


class DatasetBuilder:

	@staticmethod
	def discover(dataset_root="dataset"):
		root = Path(dataset_root)
		items = []

		if not root.exists():
			return items

		for speaker_dir in sorted(p for p in root.iterdir() if p.is_dir()):
			for audio_file in sorted(speaker_dir.glob("**/*")):
				if audio_file.is_file() and is_audio_file(audio_file):
					items.append((audio_file, speaker_dir.name))

		return items


class AudioTrainer:

	def __init__(self, dataset_root="dataset"):
		self.dataset_root = Path(dataset_root)
		self.db = Database()
		self.history = HistoryRepository(self.db)

	def build_dataset(self):
		samples = DatasetBuilder.discover(self.dataset_root)
		features = []
		labels = []

		for audio_path, label in samples:
			features.append(FeatureExtractor.extract(audio_path))
			labels.append(label)

		if not features:
			raise ValueError("No training samples found in dataset.")

		return np.asarray(features, dtype=np.float32), np.asarray(labels)

	def train(self):
		if RandomForestClassifier is None or StandardScaler is None or LabelEncoder is None:
			raise RuntimeError("scikit-learn is required for training.")

		MODELS_DIR.mkdir(exist_ok=True)

		x, y = self.build_dataset()
		label_encoder = LabelEncoder()
		y_encoded = label_encoder.fit_transform(y)

		scaler = StandardScaler()
		x_scaled = scaler.fit_transform(x)

		class_counts = Counter(y.tolist())
		stratify_target = y_encoded if len(class_counts) > 1 and min(class_counts.values()) >= 2 else None

		x_train, x_test, y_train, y_test = train_test_split(
			x_scaled,
			y_encoded,
			test_size=0.25,
			random_state=42,
			stratify=stratify_target,
		)

		models = {
			"random_forest": RandomForestClassifier(n_estimators=300, random_state=42),
		}

		if SVC is not None:
			models["svm"] = SVC(kernel="rbf", probability=True, C=10.0, gamma="scale", random_state=42)

		metrics = {}
		trained_models = {}

		for name, model in models.items():
			model.fit(x_train, y_train)
			predictions = model.predict(x_test)
			accuracy = accuracy_score(y_test, predictions)
			precision = precision_score(y_test, predictions, average="weighted", zero_division=0)
			recall = recall_score(y_test, predictions, average="weighted", zero_division=0)
			f1 = f1_score(y_test, predictions, average="weighted", zero_division=0)
			labels = list(range(len(label_encoder.classes_)))

			metrics[name] = {
				"accuracy": float(accuracy),
				"precision": float(precision),
				"recall": float(recall),
				"f1_score": float(f1),
				"confusion_matrix": confusion_matrix(y_test, predictions, labels=labels).tolist(),
				"classification_report": classification_report(y_test, predictions, labels=labels, target_names=label_encoder.classes_, output_dict=True, zero_division=0),
			}
			trained_models[name] = model

		best_algorithm = max(metrics, key=lambda key: metrics[key]["accuracy"])
		best_model = trained_models[best_algorithm]

		model_path = MODELS_DIR / "voice_model.pkl"
		label_encoder_path = MODELS_DIR / "label_encoder.pkl"
		scaler_path = MODELS_DIR / "scaler.pkl"

		joblib.dump(best_model, model_path)
		joblib.dump(label_encoder, label_encoder_path)
		joblib.dump(scaler, scaler_path)

		summary = {
			"best_algorithm": best_algorithm,
			"metrics": metrics,
			"class_counts": dict(class_counts),
			"sample_count": int(len(y)),
			"feature_count": int(x.shape[1]),
		}

		self.history.create_trained_model(best_algorithm, metrics[best_algorithm]["accuracy"] * 100.0, str(model_path))

		with open(MODELS_DIR / "training_summary.json", "w", encoding="utf-8") as handle:
			json.dump(summary, handle, indent=2)

		return TrainingResult(
			best_algorithm=best_algorithm,
			accuracy=metrics[best_algorithm]["accuracy"],
			metrics=metrics[best_algorithm],
			report=metrics[best_algorithm]["classification_report"],
			model_path=str(model_path),
			label_encoder_path=str(label_encoder_path),
			scaler_path=str(scaler_path),
		)

