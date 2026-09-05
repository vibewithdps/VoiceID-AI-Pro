import customtkinter as ctk

from app.auth.session import Session
from app.ui.components.dialog import Dialog
from app.ui.theme import ACCENT, MUTED_TEXT, SMALL_FONT, SURFACE, SURFACE_ALT


class Topbar(ctk.CTkFrame):

    def __init__(self, master, on_logout, on_toggle_theme, on_profile):
        super().__init__(master, height=72, fg_color=SURFACE, corner_radius=0)
        self.pack_propagate(False)

        self.on_logout = on_logout
        self.on_toggle_theme = on_toggle_theme
        self.on_profile = on_profile

        self._build_ui()

    def _build_ui(self):
        left = ctk.CTkFrame(self, fg_color="transparent")
        left.pack(side="left", padx=18)

        ctk.CTkLabel(left, text="VoiceID AI Pro", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ctk.CTkLabel(left, text="Professional Voice Authentication Workspace", font=SMALL_FONT, text_color=MUTED_TEXT).pack(anchor="w")

        right = ctk.CTkFrame(self, fg_color="transparent")
        right.pack(side="right", padx=18)

        ctk.CTkButton(right, text="Profile", width=88, fg_color=SURFACE_ALT, hover_color=ACCENT, command=self.on_profile).pack(side="left", padx=6)
        ctk.CTkButton(right, text="Theme", width=84, fg_color=SURFACE_ALT, hover_color=ACCENT, command=self.on_toggle_theme).pack(side="left", padx=6)
        ctk.CTkButton(right, text="Logout", width=88, fg_color="#5B2431", hover_color="#7B2D3F", command=self._logout).pack(side="left", padx=6)

        avatar = ctk.CTkLabel(right, text="👤", width=36, height=36, fg_color=ACCENT, corner_radius=18)
        avatar.pack(side="left", padx=(12, 8))

        self.user_label = ctk.CTkLabel(right, text=Session.display_name() or "Guest", font=("Segoe UI", 15, "bold"))
        self.user_label.pack(side="left")

    def refresh_user(self):
        self.user_label.configure(text=Session.display_name() or "Guest")

    def _logout(self):
        if Dialog.confirm("Logout", "Do you want to sign out now?"):
            self.on_logout()