from dataclasses import dataclass


@dataclass(slots=True)
class User:
    id: int | None
    full_name: str
    username: str
    email: str
    password: str
    role: str = "user"
    created_at: str | None = None
    last_login: str | None = None


@dataclass(slots=True)
class VoiceSample:
    id: int | None
    user_id: int
    audio_path: str
    duration: float | None = None
    sample_number: int | None = None
    created_at: str | None = None


@dataclass(slots=True)
class TrainedModel:
    id: int | None
    algorithm: str
    accuracy: float | None = None
    model_path: str | None = None
    trained_at: str | None = None


@dataclass(slots=True)
class PredictionHistory:
    id: int | None
    user_id: int | None
    file_name: str
    predicted_speaker: str
    confidence: float | None = None
    prediction_time: str | None = None


@dataclass(slots=True)
class Setting:
    key: str
    value: str