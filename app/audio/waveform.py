import numpy as np


class WaveformAnalyzer:

    @staticmethod
    def sample_envelope(audio, width=600):

        if audio is None or audio.size == 0:
            return []

        mono = np.mean(np.abs(audio), axis=1) if audio.ndim > 1 else np.abs(audio)

        if len(mono) <= width:
            return mono.tolist()

        chunk_size = max(len(mono) // width, 1)
        envelope = []

        for index in range(0, len(mono), chunk_size):
            chunk = mono[index:index + chunk_size]
            envelope.append(float(np.max(chunk)))

        return envelope[:width]

    @staticmethod
    def peak_points(audio, points=120):
        return WaveformAnalyzer.sample_envelope(audio, width=points)