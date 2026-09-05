import numpy as np


class SilenceDetector:

    @staticmethod
    def detect(audio, sample_rate, threshold=0.02, min_silence_ms=300):

        if audio.size == 0:
            return []

        mono = np.mean(np.abs(audio), axis=1) if audio.ndim > 1 else np.abs(audio)
        min_samples = max(int(sample_rate * min_silence_ms / 1000), 1)
        silent = mono < threshold

        regions = []
        start = None

        for index, is_silent in enumerate(silent):
            if is_silent and start is None:
                start = index
            elif not is_silent and start is not None:
                if index - start >= min_samples:
                    regions.append((start, index))
                start = None

        if start is not None and len(silent) - start >= min_samples:
            regions.append((start, len(silent)))

        return regions