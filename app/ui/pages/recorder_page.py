import os
import threading
import time
from tkinter import messagebox

import customtkinter as ctk

from app.audio.player import AudioPlayer
from app.audio.recorder import VoiceRecorder
from app.auth.auth_manager import AuthManager
from app.auth.session import Session
from app.ml.predictor import SpeakerPredictor
import tkinter as tk


class RecorderPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.recorder = VoiceRecorder()
        self.auth = AuthManager()
        self.current_user = Session.current_user()

        self.filepath = None
        self.recording = False
        self.seconds = 0
        self.speaker_lookup = {}
        self.predictor = SpeakerPredictor()

        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(
            self,
            text="🎤 Voice Recorder",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(20, 10))

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=30)

        ctk.CTkLabel(top, text="Speaker").pack(side="left", padx=10)

        users = self.auth.get_all_users()
        if not users and self.current_user:
            users = [self.current_user]

        speaker_labels = []
        for user in users:
            label = f"{user[1]} ({user[2]})" if user[2] and user[2] != user[1] else user[1]
            self.speaker_lookup[label] = user[2] or user[1]
            speaker_labels.append(label)

        if self.current_user:
            current_label = f"{self.current_user[1]} ({self.current_user[2]})" if self.current_user[2] and self.current_user[2] != self.current_user[1] else self.current_user[1]
        elif speaker_labels:
            current_label = speaker_labels[0]
        else:
            current_label = "No Users"

        self.speaker = ctk.StringVar(value=current_label)

        self.speaker_menu = ctk.CTkOptionMenu(
            top,
            values=speaker_labels or [current_label],
            variable=self.speaker,
            width=260,
        )
        self.speaker_menu.pack(side="left", padx=10)

        self.status = ctk.CTkLabel(
            self,
            text="🟢 Ready",
            font=("Segoe UI", 18)
        )
        self.status.pack(pady=15)

        self.timer = ctk.CTkLabel(
            self,
            text="00:00",
            font=("Consolas", 42, "bold")
        )
        self.timer.pack()

        self.waveform_frame = ctk.CTkFrame(self, height=120, corner_radius=15)
        self.waveform_frame.pack(fill="x", padx=30, pady=20)

        self.canvas = tk.Canvas(self.waveform_frame, height=120, highlightthickness=0, bg="#1E1E1E")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.create_text(300, 50, text="📊 Ready to Record", fill="#666666", font=("Segoe UI", 14))

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(pady=20)

        self.record_btn = ctk.CTkButton(buttons, text="🎤 Record", width=140, command=self.start_recording)
        self.record_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = ctk.CTkButton(buttons, text="⏹ Stop", width=140, state="disabled", command=self.stop_recording)
        self.stop_btn.grid(row=0, column=1, padx=10)

        self.play_btn = ctk.CTkButton(buttons, text="▶ Play", width=140, state="disabled", command=self.play_recording)
        self.play_btn.grid(row=0, column=2, padx=10)

        self.delete_btn = ctk.CTkButton(buttons, text="🗑 Delete", width=140, state="disabled", command=self.delete_recording)
        self.delete_btn.grid(row=0, column=3, padx=10)
        
        self.predict_btn = ctk.CTkButton(buttons, text="🎯 Predict", width=140, state="disabled", command=self.predict_recording, fg_color="#27ae60", hover_color="#219653")
        self.predict_btn.grid(row=0, column=4, padx=10)

        self.last_file = ctk.CTkLabel(self, text="Last Recording : None", font=("Segoe UI", 15))
        self.last_file.pack(pady=10)

    def start_recording(self):
        if self.recording:
            return

        self.recording = True
        self.seconds = 0

        self.status.configure(text="🔴 Recording...")
        self.record_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        threading.Thread(target=self.update_timer, daemon=True).start()
        threading.Thread(target=self.record_process, daemon=True).start()

    def update_timer(self):
        while self.recording:
            mins = self.seconds // 60
            secs = self.seconds % 60

            self.timer.configure(text=f"{mins:02}:{secs:02}")
            time.sleep(1)
            self.seconds += 1

    def record_process(self):
        try:
            self.recorder.start(5)

            speaker_label = self.speaker.get()
            speaker = self.speaker_lookup.get(speaker_label, speaker_label)
            self.filepath = self.recorder.save(speaker)
        except Exception as exc:
            error_message = str(exc)
            self.after(0, lambda message=error_message: messagebox.showerror("Recording Error", message))
            self.filepath = None
        finally:
            self.recording = False
            self.after(0, self.recording_finished)

    def recording_finished(self):
        self.status.configure(text="✅ Recording Saved")
        self.record_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.play_btn.configure(state="normal" if self.filepath else "disabled")
        self.delete_btn.configure(state="normal" if self.filepath else "disabled")
        self.predict_btn.configure(state="normal" if self.filepath else "disabled")
        self.predict_btn.configure(state="normal" if self.filepath else "disabled")

        if self.filepath:
            self.draw_waveform()
            self.last_file.configure(text=f"Last Recording : {self.filepath}")
            messagebox.showinfo("Success", "Recording Saved Successfully!")
        else:
            self.last_file.configure(text="Last Recording : None")


    def draw_waveform(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 1:
            width = 600
        
        envelope = self.recorder.waveform(width=width)
        if not envelope:
            self.canvas.create_text(width//2, height//2, text="No Audio Data", fill="#666666", font=("Segoe UI", 14))
            return
            
        peak = max(envelope) if max(envelope) > 0 else 1.0
        
        for x, val in enumerate(envelope):
            bar_height = (val / peak) * (height - 10)
            y1 = (height - bar_height) / 2
            y2 = (height + bar_height) / 2
            self.canvas.create_line(x, y1, x, y2, fill="#4EA5FF", width=1)

    def predict_recording(self):
        if not self.filepath or not os.path.exists(self.filepath):
            messagebox.showwarning("No File", "Please record audio first.")
            return
            
        try:
            result = self.predictor.predict(self.filepath)
            messagebox.showinfo("Prediction Result", f"Speaker: {result.speaker}\nConfidence: {result.confidence:.2f}%")
        except Exception as exc:
            messagebox.showerror("Prediction Failed", str(exc))

    def stop_recording(self):
        self.status.configure(text="Stopping...")
        self.recording = False
        self.recorder.stop()

    def play_recording(self):
        if not self.filepath:
            messagebox.showwarning("No Recording", "Please record audio first.")
            return

        if not os.path.exists(self.filepath):
            messagebox.showerror("Missing File", "Recording file not found.")
            return

        self.status.configure(text="▶ Playing...")
        self.play_btn.configure(state="disabled")

        threading.Thread(target=self.play_process, daemon=True).start()

    def play_process(self):
        try:
            AudioPlayer.play(self.filepath)
        except Exception as exc:
            error_message = str(exc)
            self.after(0, lambda message=error_message: messagebox.showerror("Playback Error", message))
        finally:
            self.after(0, lambda: self.status.configure(text="🟢 Ready"))
            self.after(0, lambda: self.play_btn.configure(state="normal"))

    def delete_recording(self):
        if not self.filepath:
            return

        answer = messagebox.askyesno("Delete Recording", "Are you sure you want to delete this recording?")
        if not answer:
            return

        try:
            if os.path.exists(self.filepath):
                os.remove(self.filepath)

            self.filepath = None
            self.last_file.configure(text="Last Recording : None")
            self.play_btn.configure(state="disabled")
            self.delete_btn.configure(state="disabled")
            self.predict_btn.configure(state="disabled")
            self.canvas.delete("all")
            self.canvas.create_text(300, 50, text="📊 Ready to Record", fill="#666666", font=("Segoe UI", 14))
            self.status.configure(text="🗑 Recording Deleted")
            self.timer.configure(text="00:00")

            messagebox.showinfo("Deleted", "Recording deleted successfully.")
        except Exception as exc:
            messagebox.showerror("Delete Error", str(exc))

    def reset_ui(self):
        self.recording = False
        self.seconds = 0

        self.timer.configure(text="00:00")
        self.status.configure(text="🟢 Ready")
        self.record_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.play_btn.configure(state="normal" if self.filepath else "disabled")
        self.delete_btn.configure(state="normal" if self.filepath else "disabled")
        self.predict_btn.configure(state="normal" if self.filepath else "disabled")
