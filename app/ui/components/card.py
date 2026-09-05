import customtkinter as ctk

from app.ui.theme import BODY_FONT, SUBTITLE_FONT, SURFACE, SURFACE_ALT


class MetricCard(ctk.CTkFrame):

    def __init__(self, master, title, value, subtitle=""):
        super().__init__(master, fg_color=SURFACE, corner_radius=18)

        self.configure(border_width=1, border_color=SURFACE_ALT)

        ctk.CTkLabel(self, text=title, font=BODY_FONT).pack(anchor="w", padx=18, pady=(16, 4))
        self.value_label = ctk.CTkLabel(self, text=value, font=SUBTITLE_FONT)
        self.value_label.pack(anchor="w", padx=18)

        if subtitle:
            ctk.CTkLabel(self, text=subtitle, font=("Segoe UI", 12), text_color="#9CA3AF").pack(anchor="w", padx=18, pady=(6, 16))

    def set_value(self, value):
        self.value_label.configure(text=value)