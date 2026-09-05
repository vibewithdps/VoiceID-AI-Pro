from pathlib import Path

import numpy as np

try:
	import librosa
except Exception:  # pragma: no cover - runtime fallback if librosa is unavailable
	librosa = None

from app.audio.audio_utils import is_audio_file
from app.audio.converter import AudioConverter
from app.audio.processor import AudioProcessor


class FeatureExtractor:

	DEFAULT_SAMPLE_RATE = 22050

	@staticmethod
	def _ensure_wav(path):
		source = Path(path)
		if source.suffix.lower() == ".wav":
			return source
		return Path(AudioConverter.ensure_wav(source))

	@staticmethod
	def extract(path, target_sample_rate=None):
		source = Path(path)

		if not source.exists():
			raise FileNotFoundError(source)

		if not is_audio_file(source):
			raise ValueError(f"Unsupported audio file: {source.suffix}")

		wav_path = FeatureExtractor._ensure_wav(source)
		audio, sample_rate = AudioProcessor.load(wav_path)
		audio = np.squeeze(audio)

		if target_sample_rate and sample_rate != target_sample_rate:
			audio = AudioProcessor.resample(audio, sample_rate, target_sample_rate)
			sample_rate = target_sample_rate

		if librosa is not None:
			return FeatureExtractor._extract_with_librosa(audio, sample_rate)

		return FeatureExtractor._extract_without_librosa(audio, sample_rate)

	@staticmethod
	def _extract_with_librosa(audio, sample_rate):
		if audio.ndim > 1:
			audio = np.mean(audio, axis=1)

		mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
		chroma = librosa.feature.chroma_stft(y=audio, sr=sample_rate)
		mel = librosa.feature.melspectrogram(y=audio, sr=sample_rate)
		zcr = librosa.feature.zero_crossing_rate(audio)
		centroid = librosa.feature.spectral_centroid(y=audio, sr=sample_rate)
		rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sample_rate)
		rms = librosa.feature.rms(y=audio)

		features = np.hstack(
			[
				np.mean(mfcc.T, axis=0),
				np.mean(chroma.T, axis=0),
				np.mean(mel.T, axis=0),
				np.mean(zcr.T, axis=0),
				np.mean(centroid.T, axis=0),
				np.mean(rolloff.T, axis=0),
				np.mean(rms.T, axis=0),
			]
		)

		return features.astype(np.float32)

	@staticmethod
	def _extract_without_librosa(audio, sample_rate):
		if audio.ndim > 1:
			audio = np.mean(audio, axis=1)
		
		try:
			from python_speech_features import mfcc
			features_mfcc = mfcc(audio, sample_rate, numcep=40, nfft=2048)
			return np.mean(features_mfcc, axis=0).astype(np.float32)
		except ImportError:
			# Absolute fallback if python_speech_features is not installed
			return np.zeros(40, dtype=np.float32)

