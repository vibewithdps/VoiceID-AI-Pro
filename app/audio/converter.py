from pathlib import Path
import shutil
import subprocess

from app.audio.audio_utils import ensure_directory, is_audio_file


class AudioConverter:

	@staticmethod
	def to_wav(source_path, target_path=None, sample_rate=44100, channels=1):

		source = Path(source_path)

		if not source.exists():
			raise FileNotFoundError(source)

		if not is_audio_file(source):
			raise ValueError(f"Unsupported audio file: {source.suffix}")

		target = Path(target_path) if target_path else source.with_suffix(".wav")
		ensure_directory(target.parent)

		ffmpeg = shutil.which("ffmpeg")
		if ffmpeg is None:
			raise RuntimeError("FFmpeg is required to convert MP3/M4A files to WAV.")

		command = [
			ffmpeg,
			"-y",
			"-i",
			str(source),
			"-ac",
			str(channels),
			"-ar",
			str(sample_rate),
			str(target),
		]

		subprocess.run(command, check=True, capture_output=True)
		return str(target)

	@staticmethod
	def ensure_wav(source_path, **kwargs):

		source = Path(source_path)

		if source.suffix.lower() == ".wav":
			return str(source)

		return AudioConverter.to_wav(source, **kwargs)
