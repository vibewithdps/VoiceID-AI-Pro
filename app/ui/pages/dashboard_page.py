from pathlib import Path

import customtkinter as ctk

from app.auth.session import Session
from app.database.database import Database
from app.database.history_repository import HistoryRepository
from app.database.settings_repository import SettingsRepository
from app.database.user_repository import UserRepository
from app.ui.components.card import MetricCard
from app.ui.components.chart import MiniBarChart
from app.ui.theme import BODY_FONT, MUTED_TEXT, SUBTITLE_FONT, TITLE_FONT


class DashboardPage(ctk.CTkFrame):

    def __init__(self, master, show_page):
        super().__init__(master, fg_color="transparent")
        self.show_page = show_page
        self.db = Database()
        self.users = UserRepository(self.db)
        self.history = HistoryRepository(self.db)
        self.settings = SettingsRepository(self.db)
        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(header, text=f"Welcome, {Session.display_name() or 'Guest'}", font=TITLE_FONT).pack(anchor="w")
        ctk.CTkLabel(header, text="Monitor the system, manage workflows, and launch core actions from one workspace.", font=BODY_FONT, text_color=MUTED_TEXT).pack(anchor="w", pady=(6, 0))

        stats_row = ctk.CTkFrame(self, fg_color="transparent")
        stats_row.pack(fill="x", pady=(4, 14))

        users = self.users.get_all_users()
        total_users = len(users)
        total_samples = self._count_samples()
        latest_model = self.history.list_trained_models()
        accuracy = latest_model[0]["accuracy"] if latest_model and latest_model[0]["accuracy"] is not None else None
        status_text = "Ready" if total_samples else "Waiting for samples"

        MetricCard(stats_row, "Total Voice Samples", str(total_samples), "From dataset and enrollment storage").pack(side="left", expand=True, fill="x", padx=8)
        MetricCard(stats_row, "Total Speakers", str(total_users), "Registered team members").pack(side="left", expand=True, fill="x", padx=8)
        MetricCard(stats_row, "Model Accuracy", f"{accuracy:.1f}%" if accuracy is not None else "N/A", "Latest trained model").pack(side="left", expand=True, fill="x", padx=8)
        MetricCard(stats_row, "Model Status", status_text, "Operational readiness").pack(side="left", expand=True, fill="x", padx=8)

        action_box = ctk.CTkFrame(self, fg_color="transparent")
        action_box.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(action_box, text="Quick Actions", font=SUBTITLE_FONT).pack(anchor="w", pady=(0, 10))

        button_row = ctk.CTkFrame(action_box, fg_color="transparent")
        button_row.pack(fill="x")

        actions = [
            ("🎙 Record Voice", "recorder"),
            ("📂 Upload Audio", "upload"),
            ("🧠 Train Model", "train"),
            ("🎯 Predict Speaker", "predict"),
        ]

        for label, page in actions:
            ctk.CTkButton(button_row, text=label, height=44, command=lambda value=page: self.show_page(value)).pack(side="left", expand=True, fill="x", padx=6)

        middle = ctk.CTkFrame(self, fg_color="transparent")
        middle.pack(fill="both", expand=True)

        recent = ctk.CTkFrame(middle, corner_radius=18)
        recent.pack(side="left", fill="both", expand=True, padx=(0, 8))

        ctk.CTkLabel(recent, text="Recent Activity", font=SUBTITLE_FONT).pack(anchor="w", padx=18, pady=(16, 10))

        activity = ctk.CTkTextbox(recent, height=240)
        activity.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        activity.insert("end", f"• Logged in as {Session.display_name()}\n")
        activity.insert("end", f"• {total_users} registered users detected\n")
        activity.insert("end", f"• {total_samples} voice samples available\n")
        activity.insert("end", f"• Theme setting: {self.settings.get('appearance', 'dark')}\n")
        activity.configure(state="disabled")

        chart_values = [max(total_samples, 1), max(total_users, 1), max(len(self.history.list_prediction_history()), 1), max(len(latest_model), 1)]
        chart_labels = ["Samples", "Speakers", "Predictions", "Models"]
        MiniBarChart(middle, "Workspace Overview", chart_values, chart_labels).pack(side="left", fill="both", expand=True, padx=(8, 0))

    def _count_samples(self):
        total = 0
        dataset_dir = Path("dataset")
        if dataset_dir.exists():
            for ext in ("*.wav", "*.mp3", "*.m4a"):
                total += len(list(dataset_dir.glob(f"**/{ext}")))
        return total


Dashboard = DashboardPage
