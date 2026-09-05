from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from app.audio.converter import AudioConverter
from app.audio.player import AudioPlayer
from app.auth.session import Session
from app.services.enrollment_service import EnrollmentService


class UploadPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.service = EnrollmentService()
        self.uploaded_path = None

        self.build_ui()

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="📂 Upload Audio",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(30, 12))

        ctk.CTkLabel(
            self,
            text=f"Current user: {Session.display_name()} (@{Session.username()})",
            font=("Segoe UI", 16)
        ).pack(pady=(0, 18))

        self.progress_label = ctk.CTkLabel(
            self,
            text="Samples: 0 / 20",
            font=("Segoe UI", 16, "bold")
        )
        self.progress_label.pack(pady=(0, 8))

        self.progress_bar = ctk.CTkProgressBar(self, width=480)
        self.progress_bar.pack(pady=(0, 18))

        self.status = ctk.CTkLabel(
            self,
            text="Choose a .wav, .mp3, or .m4a file to import into your dataset.",
            font=("Segoe UI", 15)
        )
        self.status.pack(pady=(0, 20))

        ctk.CTkButton(
            self,
            text="Select Audio File",
            width=220,
            height=42,
            command=self.select_audio
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Play Uploaded File",
            width=220,
            height=42,
            command=self.play_uploaded
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Open Dataset Folder",
            width=220,
            height=42,
            command=self.open_folder
        ).pack(pady=10)

        self.file_label = ctk.CTkLabel(
            self,
            text="No file selected yet.",
            font=("Segoe UI", 14)
        )
        self.file_label.pack(pady=(20, 0))

        ctk.CTkLabel(
            self,
            text="Recent Files",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(24, 8))

        self.recent_files = ctk.CTkTextbox(self, width=640, height=180)
        self.recent_files.pack()

        self.refresh()

    def refresh(self):

        count = self.service.sample_count()
        self.progress_label.configure(text=f"Samples: {count} / {self.service.REQUIRED_SAMPLES}")
        self.progress_bar.set(min(count / self.service.REQUIRED_SAMPLES, 1.0))

        self.recent_files.delete("1.0", "end")

        samples = self.service.get_samples()
        if not samples:
            self.recent_files.insert("end", "No recent files yet.\n")
            return

        for sample in samples[-10:][::-1]:
            self.recent_files.insert("end", f"• {sample.name}\n")

    def select_audio(self):

        path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio files", "*.wav *.mp3 *.m4a"),
                ("All files", "*.*")
            ]
        )

        if not path:
            return

        destination = self.service.next_filename()

        try:
            AudioConverter.to_wav(path, destination)
        except Exception as exc:
            messagebox.showerror("Upload Failed", str(exc))
            return

        self.uploaded_path = str(destination)
        self.file_label.configure(text=f"Saved as: {destination.name}")
        self.status.configure(text="✅ File imported into the enrollment dataset.")

        self.refresh()

        messagebox.showinfo("Upload Complete", f"Audio saved to\n{destination}")

    def play_uploaded(self):

        if not self.uploaded_path:
            messagebox.showwarning("No File", "Select and upload a file first.")
            return

        try:
            AudioPlayer.play(self.uploaded_path)
        except Exception as exc:
            messagebox.showerror("Playback Error", str(exc))

    def open_folder(self):

        folder = self.service.get_dataset_path()
        messagebox.showinfo("Dataset Folder", str(folder))