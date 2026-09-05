import numpy as np


class Augmentation:

    @staticmethod
    def add_noise(audio, noise_factor=0.005):
        if audio.size == 0:
            return audio
        noise = np.random.normal(0, 1, audio.shape)
        return audio + noise_factor * noise

    @staticmethod
    def time_shift(audio, shift_max=0.2):
        if audio.size == 0:
            return audio
        shift = int(np.random.uniform(-shift_max, shift_max) * len(audio))
        return np.roll(audio, shift, axis=0)
