import os

with open("app/ml/feature_extractor.py", "r") as f:
    content = f.read()

new_extractor = """	@staticmethod
	def _extract_without_librosa(audio, sample_rate):
		if audio.ndim > 1:
			audio = np.mean(audio, axis=1)
		
		try:
			from python_speech_features import mfcc
			features_mfcc = mfcc(audio, sample_rate, numcep=40, nfft=2048)
			return np.mean(features_mfcc, axis=0).astype(np.float32)
		except ImportError:
			# Absolute fallback if python_speech_features is not installed
			return np.zeros(40, dtype=np.float32)"""

# replace the old method
import re
content = re.sub(r'\t@staticmethod\n\tdef _extract_without_librosa.*?astype\(np\.float32\)', new_extractor, content, flags=re.DOTALL)

with open("app/ml/feature_extractor.py", "w") as f:
    f.write(content)
