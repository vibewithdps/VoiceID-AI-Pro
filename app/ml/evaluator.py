from dataclasses import dataclass

try:
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
except Exception:  # pragma: no cover
    accuracy_score = classification_report = confusion_matrix = f1_score = precision_score = recall_score = None


@dataclass
class EvaluationResult:
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: list
    classification_report: dict


class ModelEvaluator:

    @staticmethod
    def evaluate(model, x_test, y_test, label_encoder=None):
        if accuracy_score is None:
            raise RuntimeError("scikit-learn is required for evaluation.")

        predictions = model.predict(x_test)
        target_names = label_encoder.classes_ if label_encoder is not None else None

        return EvaluationResult(
            accuracy=float(accuracy_score(y_test, predictions)),
            precision=float(precision_score(y_test, predictions, average="weighted", zero_division=0)),
            recall=float(recall_score(y_test, predictions, average="weighted", zero_division=0)),
            f1_score=float(f1_score(y_test, predictions, average="weighted", zero_division=0)),
            confusion_matrix=confusion_matrix(y_test, predictions).tolist(),
            classification_report=classification_report(y_test, predictions, target_names=target_names, output_dict=True, zero_division=0),
        )
