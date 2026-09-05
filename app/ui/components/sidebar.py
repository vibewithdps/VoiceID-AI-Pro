import customtkinter as ctk

from app.auth.session import Session
from app.ui.theme import ACCENT, MUTED_TEXT, SIDEBAR_WIDTH, SURFACE, SURFACE_ALT


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, callback):
        super().__init__(master, width=SIDEBAR_WIDTH, corner_radius=0, fg_color=SURFACE)
        self.callback = callback
        self.pack_propagate(False)
        self._build_ui()

    def _build_ui(self):
        brand = ctk.CTkFrame(self, fg_color="transparent")
        brand.pack(fill="x", padx=18, pady=(20, 18))

        ctk.CTkLabel(brand, text="🎤 VoiceID AI Pro", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ctk.CTkLabel(brand, text=Session.display_name() or "Not signed in", font=("Segoe UI", 12), text_color=MUTED_TEXT).pack(anchor="w", pady=(4, 0))

        menu = [
            ("🏠 Dashboard", "dashboard"),
            ("🎤 Recorder", "recorder"),
            ("📂 Upload", "upload"),
            ("👥 Enrollment", "enrollment"),
            ("🧠 Train", "train"),
            ("🎯 Predict", "predict"),
            ("📊 Reports", "report"),
            ("📜 History", "history"),
            ("⚙ Settings", "settings"),
            ("👤 Profile", "profile"),
            ("↩ Logout", "logout"),
        ]

        self.buttons = {}

        for text, page in menu:
            button = ctk.CTkButton(
                self,
                text=text,
                height=42,
                corner_radius=10,
                anchor="w",
                fg_color=SURFACE_ALT,
                hover_color=ACCENT,
                command=lambda value=page: self.callback(value),
            )
            button.pack(fill="x", padx=14, pady=5)
            self.buttons[page] = button