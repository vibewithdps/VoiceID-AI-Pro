try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
except Exception:  # pragma: no cover
    RandomForestClassifier = None
    SVC = None


class Algorithms:

    @staticmethod
    def available():
        algorithms = {}
        if RandomForestClassifier is not None:
            algorithms["random_forest"] = RandomForestClassifier(n_estimators=300, random_state=42)
        if SVC is not None:
            algorithms["svm"] = SVC(kernel="rbf", probability=True, C=10.0, gamma="scale", random_state=42)
        return algorithms
