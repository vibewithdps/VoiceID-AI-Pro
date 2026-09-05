import customtkinter as ctk

from app.database.database import Database
from app.database.history_repository import HistoryRepository
from app.ui.components.dialog import Dialog
from app.ui.theme import BODY_FONT, MUTED_TEXT


class HistoryPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.db = Database()
        self.history = HistoryRepository(self.db)

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        ctk.CTkLabel(self, text="📜 History", font=("Segoe UI", 30, "bold")).pack(anchor="w", pady=(0, 6))
        ctk.CTkLabel(self, text="Review prediction events and model activity across the workspace.", font=BODY_FONT, text_color=MUTED_TEXT).pack(anchor="w", pady=(0, 18))

        self.history_box = ctk.CTkTextbox(self, height=420)
        self.history_box.pack(fill="both", expand=True, pady=(0, 14))

        ctk.CTkButton(self, text="Refresh", width=150, command=self.refresh).pack(anchor="w")

    def refresh(self):
        self.history_box.delete("1.0", "end")
        entries = self.history.list_prediction_history()

        if not entries:
            self.history_box.insert("end", "No history entries yet.\n")
            return

        for row in entries:
            self.history_box.insert(
                "end",
                f"• {row['prediction_time']} | {row['file_name']} | {row['predicted_speaker']} | {row['confidence']:.2f}%\n"
            )


History = HistoryPage