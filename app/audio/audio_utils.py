from pathlib import Path

import numpy as np
import soundfile as sf


SUPPORTED_AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}


def ensure_directory(path):
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def is_audio_file(path):
    return Path(path).suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS


def generate_sample_name(folder):
    folder = Path(folder)
    existing = sorted(folder.glob("voice_*.wav"))
    next_index = len(existing) + 1
    return f"voice_{next_index:03}.wav"


def read_audio_file(path):
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(source)

    audio, sample_rate = sf.read(source, dtype="float32", always_2d=True)
    return audio, sample_rate


def write_audio_file(path, audio, sample_rate):
    destination = Path(path)
    ensure_directory(destination.parent)

    data = np.asarray(audio, dtype=np.float32)
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    sf.write(destination, data, sample_rate)
    return str(destination)