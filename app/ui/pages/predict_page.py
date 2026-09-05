from tkinter import filedialog

import customtkinter as ctk

from app.audio.player import AudioPlayer
from app.database.database import Database
from app.database.history_repository import HistoryRepository
from app.ml.predictor import SpeakerPredictor
from app.ui.components.dialog import Dialog
from app.ui.theme import BODY_FONT, MUTED_TEXT, SUBTITLE_FONT


class PredictPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.predictor = SpeakerPredictor()
        self.db = Database()
        self.history = HistoryRepository(self.db)
        self.audio_path = None

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        ctk.CTkLabel(self, text="🎯 Prediction", font=("Segoe UI", 30, "bold")).pack(anchor="w", pady=(0, 6))
        ctk.CTkLabel(self, text="Browse an audio file, predict the speaker, and review the confidence score.", font=BODY_FONT, text_color=MUTED_TEXT).pack(anchor="w", pady=(0, 18))

        top = ctk.CTkFrame(self, corner_radius=18)
        top.pack(fill="x", pady=(0, 14))

        self.selected_label = ctk.CTkLabel(top, text="No file selected", font=BODY_FONT)
        self.selected_label.pack(anchor="w", padx=18, pady=(16, 8))

        actions = ctk.CTkFrame(top, fg_color="transparent")
        actions.pack(anchor="w", padx=18, pady=(0, 16))

        ctk.CTkButton(actions, text="Browse", width=150, command=self.browse_audio).pack(side="left", padx=(0, 10))
        ctk.CTkButton(actions, text="Predict", width=150, command=self.run_prediction).pack(side="left", padx=(0, 10))
        ctk.CTkButton(actions, text="Play Audio", width=150, fg_color="#3E4A5A", command=self.play_audio).pack(side="left")

        result_box = ctk.CTkFrame(self, corner_radius=18)
        result_box.pack(fill="x", pady=(0, 14))

        self.speaker_label = ctk.CTkLabel(result_box, text="Speaker: -", font=SUBTITLE_FONT)
        self.speaker_label.pack(anchor="w", padx=18, pady=(16, 4))
        self.confidence_label = ctk.CTkLabel(result_box, text="Confidence: -", font=BODY_FONT)
        self.confidence_label.pack(anchor="w", padx=18, pady=(0, 16))

        self.history_box = ctk.CTkTextbox(self, height=260)
        self.history_box.pack(fill="both", expand=True)

    def refresh(self):
        self.history_box.delete("1.0", "end")
        entries = self.history.list_prediction_history()

        if not entries:
            self.history_box.insert("end", "No prediction history yet.\n")
            return

        for row in entries[:20]:
            self.history_box.insert(
                "end",
                f"• {row['prediction_time']} | {row['file_name']} -> {row['predicted_speaker']} ({row['confidence']:.2f}% )\n"
            )

    def browse_audio(self):
        path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio files", "*.wav *.mp3 *.m4a"), ("All files", "*.*")],
        )

        if not path:
            return

        self.audio_path = path
        self.selected_label.configure(text=path)

    def run_prediction(self):
        if not self.audio_path:
            Dialog.warning("Prediction", "Please select an audio file first.")
            return

        try:
            result = self.predictor.predict(self.audio_path)
            self.speaker_label.configure(text=f"Speaker: {result.speaker}")
            self.confidence_label.configure(text=f"Confidence: {result.confidence:.2f}%")
            self.refresh()
            Dialog.info("Prediction", f"Speaker: {result.speaker}\nConfidence: {result.confidence:.2f}%")
        except Exception as exc:
            Dialog.error("Prediction Failed", str(exc))

    def play_audio(self):
        if not self.audio_path:
            Dialog.warning("Playback", "Select an audio file first.")
            return

        try:
            AudioPlayer.play(self.audio_path)
        except Exception as exc:
            Dialog.error("Playback Failed", str(exc))


Predict = PredictPage