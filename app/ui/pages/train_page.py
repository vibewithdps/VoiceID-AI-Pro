import json
import threading
from pathlib import Path

import customtkinter as ctk

from app.ml.model_manager import ModelManager
from app.ml.trainer import DatasetBuilder
from app.ml.trainer import AudioTrainer
from app.ui.components.dialog import Dialog
from app.ui.theme import BODY_FONT, MUTED_TEXT, SUBTITLE_FONT


class TrainPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.trainer = AudioTrainer()
        self.result = None

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        ctk.CTkLabel(self, text="🧠 Train Model", font=("Segoe UI", 30, "bold")).pack(anchor="w", pady=(0, 6))
        ctk.CTkLabel(self, text="Train supervised speaker models from the current dataset and export reusable artifacts.", font=BODY_FONT, text_color=MUTED_TEXT).pack(anchor="w", pady=(0, 18))

        self.progress = ctk.CTkProgressBar(self, width=520)
        self.progress.pack(anchor="w", pady=(0, 10))
        self.progress.set(0)

        info = ctk.CTkFrame(self, corner_radius=18)
        info.pack(fill="x", pady=(0, 16))

        self.status_label = ctk.CTkLabel(info, text="Dataset status: waiting", font=SUBTITLE_FONT)
        self.status_label.pack(anchor="w", padx=18, pady=(16, 6))
        self.summary_label = ctk.CTkLabel(info, text="Samples: 0 | Features: 0 | Algorithm: - | Accuracy: -", font=BODY_FONT)
        self.summary_label.pack(anchor="w", padx=18, pady=(0, 16))

        self.output = ctk.CTkTextbox(self, height=280)
        self.output.pack(fill="both", expand=True, pady=(0, 16))

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(anchor="w")

        ctk.CTkButton(actions, text="Train", width=160, command=self.start_training).pack(side="left", padx=(0, 10))
        ctk.CTkButton(actions, text="Export Model", width=160, fg_color="#3E4A5A", command=self.export_model).pack(side="left")

    def refresh(self):
        sample_count = self._sample_count()
        self.status_label.configure(text=f"Dataset status: {sample_count} samples available")
        self.summary_label.configure(text=f"Samples: {sample_count} | Features: 0 | Algorithm: - | Accuracy: -")
        self.output.delete("1.0", "end")
        self.output.insert("end", "Training summary will appear here.\n")

    def _sample_count(self):
        return len(DatasetBuilder.discover(self.trainer.dataset_root))

    def start_training(self):
        self.progress.set(0.1)
        self.status_label.configure(text="Training in progress...")
        self.output.delete("1.0", "end")
        self.output.insert("end", "Building dataset and extracting features...\n")

        threading.Thread(target=self._train_worker, daemon=True).start()

    def _train_worker(self):
        try:
            result = self.trainer.train()
            self.result = result

            def update_ui():
                self.progress.set(1.0)
                self.status_label.configure(text="Training complete")
                self.summary_label.configure(
                    text=f"Samples: {result.metrics['classification_report'].get('accuracy', 0) and self._sample_count()} | Features: exported | Algorithm: {result.best_algorithm.replace('_', ' ').title()} | Accuracy: {result.accuracy * 100:.2f}%"
                )
                self.output.delete("1.0", "end")
                self.output.insert("end", json.dumps({
                    "best_algorithm": result.best_algorithm,
                    "accuracy": round(result.accuracy * 100.0, 2),
                    "model_path": result.model_path,
                    "label_encoder_path": result.label_encoder_path,
                    "scaler_path": result.scaler_path,
                    "metrics": result.metrics,
                }, indent=2))
                Dialog.info("Training Complete", f"Best model: {result.best_algorithm.replace('_', ' ').title()}\nAccuracy: {result.accuracy * 100:.2f}%")

            self.after(0, update_ui)
        except Exception as exc:
            error_message = str(exc)
            self.after(0, lambda: self.status_label.configure(text="Training failed"))
            self.after(0, lambda message=error_message: self.output.insert("end", f"\nError: {message}\n"))
            self.after(0, lambda message=error_message: Dialog.error("Training Failed", message))

    def export_model(self):
        if not ModelManager.exists():
            Dialog.warning("Export Model", "Train a model first.")
            return

        paths = ModelManager.model_paths()
        Dialog.info(
            "Export Model",
            "Model artifacts are saved in models/\n\n"
            + "\n".join(f"{name}: {path}" for name, path in paths.items())
        )


Train = TrainPage