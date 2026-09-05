from pathlib import Path

import numpy as np
from scipy.signal import butter, filtfilt, resample_poly

from app.audio.audio_utils import ensure_directory, read_audio_file, write_audio_file
from app.audio.converter import AudioConverter
from app.audio.noise_reduction import reduce_noise


class AudioProcessor:

	@staticmethod
	def load(source_path):
		return read_audio_file(source_path)

	@staticmethod
	def normalize(audio):
		peak = np.max(np.abs(audio))
		if peak == 0:
			return audio
		return audio / peak

	@staticmethod
	def remove_dc_offset(audio):
		return audio - np.mean(audio, axis=0, keepdims=True)

	@staticmethod
	def trim_silence(audio, sample_rate, threshold=0.02, min_silence_ms=300):
		if audio.size == 0:
			return audio

		mono = np.mean(np.abs(audio), axis=1) if audio.ndim > 1 else np.abs(audio)
		window = max(int(sample_rate * min_silence_ms / 1000), 1)
		active = np.where(mono > threshold)[0]

		if active.size == 0:
			return audio[:0]

		start = max(active[0] - window, 0)
		end = min(active[-1] + window, len(audio))
		return audio[start:end]

	@staticmethod
	def resample(audio, original_rate, target_rate):
		if original_rate == target_rate:
			return audio

		gcd = np.gcd(original_rate, target_rate)
		up = target_rate // gcd
		down = original_rate // gcd
		return resample_poly(audio, up, down, axis=0)

	@staticmethod
	def bandpass_filter(audio, sample_rate, low_cut=80, high_cut=7600, order=4):
		nyquist = 0.5 * sample_rate
		low = max(low_cut / nyquist, 0.001)
		high = min(high_cut / nyquist, 0.99)

		if low >= high:
			return audio

		b, a = butter(order, [low, high], btype="band")
		return filtfilt(b, a, audio, axis=0)

	@staticmethod
	def process(source_path, target_rate=44100, output_path=None):
		source = Path(source_path)
		wav_path = AudioConverter.ensure_wav(source)
		audio, sample_rate = AudioProcessor.load(wav_path)

		audio = AudioProcessor.remove_dc_offset(audio)
		audio = reduce_noise(audio, sample_rate)
		audio = AudioProcessor.bandpass_filter(audio, sample_rate)
		audio = AudioProcessor.normalize(audio)
		audio = AudioProcessor.trim_silence(audio, sample_rate)
		audio = AudioProcessor.resample(audio, sample_rate, target_rate)

		destination = Path(output_path) if output_path else Path(wav_path).with_name(f"processed_{Path(wav_path).name}")
		ensure_directory(destination.parent)
		write_audio_file(destination, audio, target_rate)
		return str(destination)
