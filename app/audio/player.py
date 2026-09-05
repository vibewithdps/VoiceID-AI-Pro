from pathlib import Path
import threading

import numpy as np
import sounddevice as sd
import soundfile as sf

from app.audio.audio_utils import is_audio_file
from app.audio.converter import AudioConverter


class AudioPlayer:

    def __init__(self, volume=1.0):

        self.volume = max(0.0, min(float(volume), 1.0))
        self._data = None
        self._sample_rate = None
        self._position = 0
        self._stream = None
        self._lock = threading.Lock()
        self._paused = False
        self._playing = False
        self._source_path = None

    @staticmethod
    def play(filepath):

        player = AudioPlayer()
        player.load(filepath)
        player.play()
        return player

    def load(self, filepath):

        if not filepath:
            raise ValueError("No audio file selected.")

        source = Path(filepath)

        if not source.exists():
            raise FileNotFoundError(filepath)

        if not is_audio_file(source):
            raise ValueError(f"Unsupported audio file: {source.suffix}")

        if source.suffix.lower() in {".mp3", ".m4a"}:
            source = Path(AudioConverter.to_wav(source))

        data, sample_rate = sf.read(source, dtype="float32", always_2d=True)
        self._data = data
        self._sample_rate = sample_rate
        self._position = 0
        self._source_path = str(source)
        return self

    def play(self):

        if self._data is None:
            raise ValueError("No audio loaded.")

        if self._playing:
            return

        self._playing = True
        self._paused = False

        def callback(outdata, frames, _time, status):
            if status:
                pass

            with self._lock:
                if self._paused:
                    outdata.fill(0)
                    return

                end = min(self._position + frames, len(self._data))
                chunk = self._data[self._position:end]

                if len(chunk) < frames:
                    padding = np.zeros((frames - len(chunk), self._data.shape[1]), dtype=np.float32)
                    chunk = np.vstack([chunk, padding]) if len(chunk) else padding
                    outdata[:] = chunk * self.volume
                    self._position = len(self._data)
                    self._playing = False
                    raise sd.CallbackStop()

                outdata[:] = chunk * self.volume
                self._position = end

        with sd.OutputStream(
            samplerate=self._sample_rate,
            channels=self._data.shape[1],
            dtype="float32",
            callback=callback,
        ) as stream:
            self._stream = stream

            try:
                while self._playing and self._position < len(self._data):
                    sd.sleep(100)
            finally:
                self._playing = False
                self._paused = False

    def pause(self):

        if self._playing:
            self._paused = True

    def resume(self):

        if self._playing:
            self._paused = False

    def stop(self):

        self._playing = False
        self._paused = False
        self._position = 0

        if self._stream is not None:
            try:
                sd.stop()
            except Exception:
                pass

    def seek(self, seconds):

        if self._data is None or self._sample_rate is None:
            return

        sample_index = max(0, int(float(seconds) * self._sample_rate))
        self._position = min(sample_index, len(self._data))

    def set_volume(self, volume):

        self.volume = max(0.0, min(float(volume), 1.0))