from datetime import datetime
from pathlib import Path
import threading

import numpy as np
import sounddevice as sd
import soundfile as sf

from app.audio.audio_utils import ensure_directory, generate_sample_name
from app.audio.waveform import WaveformAnalyzer

SAMPLE_RATE = 44100
CHANNELS = 1


class VoiceRecorder:

    def __init__(self, sample_rate=SAMPLE_RATE, channels=CHANNELS):

        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = None
        self.is_recording = False
        self.is_paused = False
        self._stream = None
        self._frames = []
        self._lock = threading.Lock()
        self._target_duration = None
        self._start_time = None
        self._output_path = None

    def start(self, duration=None):

        self._target_duration = duration
        self._frames = []
        self.recording = None
        self.is_recording = True
        self.is_paused = False
        self._start_time = datetime.utcnow()

        def callback(indata, _frames, _time, status):
            if status:
                pass

            with self._lock:
                if self.is_recording and not self.is_paused:
                    self._frames.append(indata.copy())

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            callback=callback,
        ) as stream:
            self._stream = stream

            if duration is None:
                while self.is_recording:
                    sd.sleep(100)
            else:
                elapsed = 0.0
                while self.is_recording and elapsed < float(duration):
                    sd.sleep(100)
                    elapsed = (datetime.utcnow() - self._start_time).total_seconds()

        self.is_recording = False
        self.recording = self._combine_frames()
        return self.recording

    def pause(self):

        if self.is_recording:
            self.is_paused = True

    def resume(self):

        if self.is_recording:
            self.is_paused = False

    def stop(self):

        self.is_recording = False
        self.is_paused = False

        if self._stream is not None:
            try:
                sd.stop()
            except Exception:
                pass

    def _combine_frames(self):

        if not self._frames:
            return None

        audio = np.concatenate(self._frames, axis=0)

        if audio.ndim == 1:
            audio = audio.reshape(-1, self.channels)

        return audio

    def elapsed_seconds(self):

        if not self._start_time:
            return 0.0

        return max((datetime.utcnow() - self._start_time).total_seconds(), 0.0)

    def save(self, speaker):

        if self.recording is None:
            raise ValueError("No recording available to save.")

        folder = ensure_directory(Path("dataset") / speaker)
        filename = generate_sample_name(folder)
        filepath = folder / filename

        sf.write(filepath, self.recording, self.sample_rate)
        self._output_path = str(filepath)
        return self._output_path

    def save_to(self, destination_path):

        if self.recording is None:
            raise ValueError("No recording available to save.")

        destination = Path(destination_path)
        ensure_directory(destination.parent)
        sf.write(destination, self.recording, self.sample_rate)
        self._output_path = str(destination)
        return self._output_path

    def waveform(self, width=600):

        if self.recording is None:
            return []

        return WaveformAnalyzer.sample_envelope(self.recording, width=width)