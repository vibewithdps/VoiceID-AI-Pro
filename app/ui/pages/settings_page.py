import customtkinter as ctk

from app.ui.components.card import MetricCard
from app.ui.components.dialog import Dialog
from app.ui.theme import BODY_FONT, MUTED_TEXT, SUBTITLE_FONT


class SettingsPage(ctk.CTkFrame):

    def __init__(self, master, settings_repo=None, on_saved=None):
        super().__init__(master, fg_color="transparent")
        self.settings_repo = settings_repo
        self.on_saved = on_saved or (lambda _message=None: None)

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        ctk.CTkLabel(self, text="⚙ Settings", font=("Segoe UI", 30, "bold")).pack(anchor="w", pady=(0, 6))
        ctk.CTkLabel(self, text="Control theme, recording defaults, and model preferences from one place.", font=BODY_FONT, text_color=MUTED_TEXT).pack(anchor="w", pady=(0, 18))

        cards = ctk.CTkFrame(self, fg_color="transparent")
        cards.pack(fill="x", pady=(0, 16))

        self.theme_card = MetricCard(cards, "Appearance", "Dark", "Current UI mode")
        self.theme_card.pack(side="left", expand=True, fill="x", padx=8)
        self.duration_card = MetricCard(cards, "Recording Duration", "5 seconds", "Default capture window")
        self.duration_card.pack(side="left", expand=True, fill="x", padx=8)
        self.sample_rate_card = MetricCard(cards, "Sample Rate", "44100", "Default export rate")
        self.sample_rate_card.pack(side="left", expand=True, fill="x", padx=8)

        form = ctk.CTkFrame(self, corner_radius=18)
        form.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(form, text="General Settings", font=SUBTITLE_FONT).pack(anchor="w", padx=18, pady=(16, 10))

        self.appearance_var = ctk.StringVar(value="dark")
        self.duration_var = ctk.StringVar(value="5")
        self.sample_rate_var = ctk.StringVar(value="44100")
        self.model_var = ctk.StringVar(value="random_forest")

        self._row(form, "Appearance", ctk.CTkOptionMenu, variable=self.appearance_var, values=["dark", "light"])
        self._row(form, "Recording Duration", ctk.CTkEntry, textvariable=self.duration_var)
        self._row(form, "Default Sample Rate", ctk.CTkEntry, textvariable=self.sample_rate_var)
        self._row(form, "Default ML Model", ctk.CTkOptionMenu, variable=self.model_var, values=["random_forest", "svm", "knn"])

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x")

        ctk.CTkButton(actions, text="Save Settings", width=180, command=self.save).pack(side="left", padx=(0, 10))
        ctk.CTkButton(actions, text="Export Settings", width=180, fg_color="#3E4A5A", command=self.export_settings).pack(side="left")

    def _row(self, master, label, widget_cls, **kwargs):
        row = ctk.CTkFrame(master, fg_color="transparent")
        row.pack(fill="x", padx=18, pady=8)
        ctk.CTkLabel(row, text=label, width=180, anchor="w").pack(side="left")
        widget = widget_cls(row, **kwargs)
        widget.pack(side="left", fill="x", expand=True)
        return widget

    def refresh(self):
        if not self.settings_repo:
            return

        appearance = self.settings_repo.get("appearance", "dark")
        duration = self.settings_repo.get("recording_duration", "5")
        sample_rate = self.settings_repo.get("default_sample_rate", "44100")
        model = self.settings_repo.get("model_selection", "random_forest")

        self.appearance_var.set(appearance)
        self.duration_var.set(duration)
        self.sample_rate_var.set(sample_rate)
        self.model_var.set(model)

        self.theme_card.set_value(appearance.title())
        self.duration_card.set_value(f"{duration} seconds")
        self.sample_rate_card.set_value(sample_rate)

    def save(self):
        if not self.settings_repo:
            Dialog.warning("Settings", "Settings repository is not available.")
            return

        self.settings_repo.update_many(
            {
                "appearance": self.appearance_var.get(),
                "recording_duration": self.duration_var.get(),
                "default_sample_rate": self.sample_rate_var.get(),
                "model_selection": self.model_var.get(),
            }
        )
        self.on_saved("Settings saved")
        Dialog.info("Settings", "Settings were updated successfully.")

    def export_settings(self):
        if not self.settings_repo:
            Dialog.warning("Export Settings", "Settings repository is not available.")
            return

        settings = self.settings_repo.get_all()
        text = "\n".join(f"{key}: {value}" for key, value in settings.items())
        Dialog.info("Export Settings", text)


Settings = SettingsPage