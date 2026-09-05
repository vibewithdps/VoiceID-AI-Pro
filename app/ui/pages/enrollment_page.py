import customtkinter as ctk
from tkinter import messagebox
import threading
from pathlib import Path

from app.audio.recorder import VoiceRecorder


from app.services.enrollment_service import EnrollmentService


class EnrollmentPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.service = EnrollmentService()
        self.recorder = VoiceRecorder()

        self.build_ui()

        self.refresh()

    # ---------------------------------

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="🎤 Voice Enrollment",
            font=("Segoe UI", 28, "bold")
        )

        title.pack(pady=(20, 10))

        self.user_label = ctk.CTkLabel(
            self,
            text="",
            font=("Segoe UI", 18)
        )

        self.user_label.pack()

        self.progress_label = ctk.CTkLabel(
            self,
            text="0 / 20 Samples",
            font=("Segoe UI", 18)
        )

        self.progress_label.pack(pady=(20, 5))

        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=500
        )

        self.progress_bar.pack()

        self.status_label = ctk.CTkLabel(
            self,
            text="Collect Voice Samples",
            font=("Segoe UI", 16)
        )

        self.status_label.pack(pady=15)

        buttons = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        buttons.pack(pady=10)

        self.record_btn = ctk.CTkButton(
            buttons,
            text="🎤 Record Sample",
            width=170,
            command=self.record_sample
        )

        self.record_btn.grid(row=0, column=0, padx=10)

        self.upload_btn = ctk.CTkButton(
            buttons,
            text="📂 Upload Audio",
            width=170,
            command=self.upload_audio
        )

        self.upload_btn.grid(row=0, column=1, padx=10)

        self.delete_btn = ctk.CTkButton(
            buttons,
            text="🗑 Delete Last",
            width=170,
            command=self.delete_last
        )

        self.delete_btn.grid(row=0, column=2, padx=10)

        ctk.CTkLabel(
            self,
            text="Recent Samples",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(25, 5))

        self.sample_list = ctk.CTkTextbox(
            self,
            width=650,
            height=220
        )

        self.sample_list.pack()

    # ---------------------------------

    def refresh(self):

        count = self.service.sample_count()

        self.user_label.configure(
            text=f"User : {self.service.full_name} (@{self.service.username})"
        )

        self.progress_label.configure(
            text=f"{count} / 20 Samples"
        )

        self.progress_bar.set(
            min(count / self.service.REQUIRED_SAMPLES, 1.0)
        )

        if self.service.is_ready_for_training():

            self.status_label.configure(
                text="✅ Ready For Training"
            )

        else:

            self.status_label.configure(
                text="🎙 Collect More Samples"
            )

        self.sample_list.delete("1.0", "end")

        samples = self.service.get_samples()

        if not samples:

            self.sample_list.insert(
                "end",
                "No recordings found."
            )

        else:

            for file in samples:

                self.sample_list.insert(
                    "end",
                    file.name + "\n"
                )

    # ---------------------------------

    def record_sample(self):

        threading.Thread(
            target=self._record,
            daemon=True
        ).start()

    def _record(self):
        try:
            self.status_label.configure(
                text="🎤 Recording..."
            )

            self.recorder.start(5)

            temp = self.recorder.save(self.service.username)

            final = self.service.save_recording(temp)

            self.after(
                0,
                lambda: self.finish_recording(final)
            )

        except Exception as e:

            error_message = str(e)
            self.after(
                0,
                lambda message=error_message: messagebox.showerror(
                    "Error",
                    message
                )
            )

    def finish_recording(self, path: Path):

        self.status_label.configure(
            text="✅ Recording Saved"
        )

        self.refresh()

        messagebox.showinfo(
            "Saved",
            f"Recording saved as\n\n{path.name}"
        )


    # ---------------------------------

    def upload_audio(self):

        messagebox.showinfo(
            "Upload",
            "Use the Upload page to add existing audio files to your enrollment folder."
        )

    # ---------------------------------

    def delete_last(self):

        if self.service.delete_last():

            messagebox.showinfo(
                "Success",
                "Last recording deleted."
            )

        else:

            messagebox.showwarning(
                "Empty",
                "No recordings available."
            )

        self.refresh()