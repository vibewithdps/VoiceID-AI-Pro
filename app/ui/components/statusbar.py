import customtkinter as ctk

from app.ui.theme import MUTED_TEXT, SMALL_FONT, SURFACE


class StatusBar(ctk.CTkFrame):

    def __init__(self, master, text="Ready"):
        super().__init__(master, height=34, fg_color=SURFACE, corner_radius=0)
        self.pack_propagate(False)

        self.label = ctk.CTkLabel(self, text=text, font=SMALL_FONT, text_color=MUTED_TEXT)
        self.label.pack(side="left", padx=16)

    def set_text(self, text):
        self.label.configure(text=text)