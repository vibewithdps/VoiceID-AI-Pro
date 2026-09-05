class HistoryRepository:

    def __init__(self, database):
        self.database = database

    def create_voice_sample(self, user_id, audio_path, duration=None, sample_number=None):
        return self.database.execute(
            """
            INSERT INTO voice_samples (user_id, audio_path, duration, sample_number)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, audio_path, duration, sample_number),
        )

    def list_voice_samples(self, user_id=None):
        if user_id is None:
            return self.database.execute(
                """
                SELECT id, user_id, audio_path, duration, sample_number, created_at
                FROM voice_samples
                ORDER BY created_at DESC
                """
            ).fetchall()

        return self.database.execute(
            """
            SELECT id, user_id, audio_path, duration, sample_number, created_at
            FROM voice_samples
            WHERE user_id = ?
            ORDER BY sample_number ASC, created_at DESC
            """,
            (user_id,),
        ).fetchall()

    def create_trained_model(self, algorithm, accuracy=None, model_path=None):
        return self.database.execute(
            """
            INSERT INTO trained_models (algorithm, accuracy, model_path)
            VALUES (?, ?, ?)
            """,
            (algorithm, accuracy, model_path),
        )

    def list_trained_models(self):
        return self.database.execute(
            """
            SELECT id, algorithm, accuracy, model_path, trained_at
            FROM trained_models
            ORDER BY trained_at DESC
            """
        ).fetchall()

    def create_prediction(self, user_id, file_name, predicted_speaker, confidence=None):
        return self.database.execute(
            """
            INSERT INTO prediction_history (user_id, file_name, predicted_speaker, confidence)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, file_name, predicted_speaker, confidence),
        )

    def list_prediction_history(self, user_id=None):
        if user_id is None:
            return self.database.execute(
                """
                SELECT id, user_id, file_name, predicted_speaker, confidence, prediction_time
                FROM prediction_history
                ORDER BY prediction_time DESC
                """
            ).fetchall()

        return self.database.execute(
            """
            SELECT id, user_id, file_name, predicted_speaker, confidence, prediction_time
            FROM prediction_history
            WHERE user_id = ?
            ORDER BY prediction_time DESC
            """,
            (user_id,),
        ).fetchall()