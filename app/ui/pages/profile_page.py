import customtkinter as ctk

from app.auth.session import Session
from app.database.database import Database
from app.database.history_repository import HistoryRepository
from app.database.user_repository import UserRepository
from app.ui.components.card import MetricCard
from app.ui.theme import BODY_FONT, MUTED_TEXT, TITLE_FONT


class ProfilePage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.users = UserRepository(self.db)
        self.history = HistoryRepository(self.db)
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="👤 User Profile", font=TITLE_FONT).pack(anchor="w", pady=(0, 8))
        ctk.CTkLabel(self, text="Account overview and voice enrollment summary.", font=BODY_FONT, text_color=MUTED_TEXT).pack(anchor="w", pady=(0, 18))

        user = Session.current_user()
        user_box = ctk.CTkFrame(self, corner_radius=18)
        user_box.pack(fill="x", pady=(0, 16))

        rows = [
            ("Name", Session.full_name()),
            ("Username", Session.username()),
            ("Email", Session.email()),
            ("Last Login", self._last_login()),
        ]

        for label, value in rows:
            row = ctk.CTkFrame(user_box, fg_color="transparent")
            row.pack(fill="x", padx=18, pady=7)
            ctk.CTkLabel(row, text=label, width=140, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=value or "-", anchor="w").pack(side="left")

        stats = ctk.CTkFrame(self, fg_color="transparent")
        stats.pack(fill="x")

        samples = self._sample_count(user[0] if user else None)
        predictions = len(self.history.list_prediction_history(user[0] if user else None))

        MetricCard(stats, "Total Samples", str(samples), "Across dataset folders").pack(side="left", expand=True, fill="x", padx=8)
        MetricCard(stats, "Predictions", str(predictions), "Recorded history entries").pack(side="left", expand=True, fill="x", padx=8)

    def _last_login(self):
        user = Session.current_user()
        if not user:
            return "-"

        fetched = self.users.get_by_id(user[0])
        return fetched["last_login"] if fetched and fetched["last_login"] else "-"

    def _sample_count(self, user_id):
        if not user_id:
            return 0

        samples = self.history.list_voice_samples(user_id)
        return len(samples)