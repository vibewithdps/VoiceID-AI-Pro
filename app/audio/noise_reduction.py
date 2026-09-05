import numpy as np


def reduce_noise(audio, sample_rate, strength=0.02):

    if audio.size == 0:
        return audio

    noise_floor = np.percentile(np.abs(audio), 10)
    threshold = max(noise_floor * (1.0 + strength * 10), strength)
    cleaned = np.where(np.abs(audio) < threshold, 0.0, audio)
    return cleaned