from pathlib import Path

try:
    import joblib
except Exception:  # pragma: no cover
    joblib = None


MODELS_DIR = Path("models")


class ModelManager:

    @staticmethod
    def model_paths():
        return {
            "model": MODELS_DIR / "voice_model.pkl",
            "label_encoder": MODELS_DIR / "label_encoder.pkl",
            "scaler": MODELS_DIR / "scaler.pkl",
        }

    @staticmethod
    def save(model, label_encoder, scaler):
        if joblib is None:
            raise RuntimeError("joblib is required to save model artifacts.")

        MODELS_DIR.mkdir(exist_ok=True)
        paths = ModelManager.model_paths()
        joblib.dump(model, paths["model"])
        joblib.dump(label_encoder, paths["label_encoder"])
        joblib.dump(scaler, paths["scaler"])
        return paths

    @staticmethod
    def load():
        if joblib is None:
            raise RuntimeError("joblib is required to load model artifacts.")

        paths = ModelManager.model_paths()
        return {
            key: joblib.load(path) for key, path in paths.items()
        }

    @staticmethod
    def exists():
        paths = ModelManager.model_paths()
        return all(path.exists() for path in paths.values())
