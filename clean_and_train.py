import os
import soundfile as sf
from pathlib import Path

for root, _, files in os.walk("dataset"):
    for f in files:
        if f.endswith(".wav"):
            path = os.path.join(root, f)
            try:
                sf.read(path)
            except:
                print(f"Removing corrupted file: {path}")
                os.remove(path)

from app.ml.trainer import AudioTrainer
trainer = AudioTrainer()
result = trainer.train()
print(f"Trained successfully! Best Algorithm: {result.best_algorithm} (Accuracy: {result.accuracy*100:.2f}%)")
