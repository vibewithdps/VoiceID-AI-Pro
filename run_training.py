from app.ml.trainer import AudioTrainer
trainer = AudioTrainer()
result = trainer.train()
print(f"Trained successfully! Best Algorithm: {result.best_algorithm} (Accuracy: {result.accuracy*100:.2f}%)")
