import customtkinter as ctk
from tkinter import messagebox

from app.auth.session import Session
from app.database.database import Database
from app.database.settings_repository import SettingsRepository
from app.ui.components.sidebar import Sidebar
from app.ui.components.statusbar import StatusBar
from app.ui.components.topbar import Topbar

from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.enrollment_page import EnrollmentPage
from app.ui.pages.history_page import HistoryPage
from app.ui.pages.predict_page import PredictPage
from app.ui.pages.profile_page import ProfilePage
from app.ui.pages.recorder_page import RecorderPage
from app.ui.pages.report_page import ReportPage
from app.ui.pages.settings_page import SettingsPage
from app.ui.pages.train_page import TrainPage
from app.ui.pages.upload_page import UploadPage
from app.ui.theme import BACKGROUND, WINDOW_HEIGHT, WINDOW_WIDTH, apply_theme


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ---------------------------------
        # Check Login Session
        # ---------------------------------

        if not Session.is_logged_in():

            messagebox.showerror(
                "Access Denied",
                "Please login first."
            )

            self.destroy()
            return

        # ---------------------------------
        # Current Logged In User
        # ---------------------------------

        self.db = Database()
        self.settings_repo = SettingsRepository(self.db)
        self.current_theme = self.settings_repo.get("appearance", "dark")

        apply_theme(self.current_theme)

        self.title(f"VoiceID AI Pro | {Session.full_name() or Session.display_name()}")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(1240, 760)
        self.configure(fg_color=BACKGROUND)

        self.sidebar = Sidebar(self, self.navigate)
        self.sidebar.pack(side="left", fill="y")

        self.workspace = ctk.CTkFrame(self, fg_color="transparent")
        self.workspace.pack(side="right", fill="both", expand=True)

        self.topbar = Topbar(self.workspace, self.logout, self.toggle_theme, self.open_profile)
        self.topbar.pack(side="top", fill="x")

        self.content = ctk.CTkFrame(self.workspace, fg_color="transparent")
        self.content.pack(side="top", fill="both", expand=True, padx=18, pady=(14, 10))

        self.statusbar = StatusBar(self, text="Ready")
        self.statusbar.pack(side="bottom", fill="x")

        self.pages = {
            "dashboard": DashboardPage(self.content, self.show_page),
            "enrollment": EnrollmentPage(self.content),
            "recorder": RecorderPage(self.content),
            "upload": UploadPage(self.content),
            "train": TrainPage(self.content),
            "report": ReportPage(self.content),
            "predict": PredictPage(self.content),
            "history": HistoryPage(self.content),
            "settings": SettingsPage(self.content, self.settings_repo, self.on_settings_saved),
            "profile": ProfilePage(self.content),
        }

        self.show_page("dashboard")
        self.protocol("WM_DELETE_WINDOW", self.close_app)

    # =========================================

    def show_page(self, page_name):

        if page_name not in self.pages:
            return

        for page in self.pages.values():
            page.pack_forget()

        page = self.pages[page_name]
        page.pack(fill="both", expand=True)

        if hasattr(page, "refresh"):
            page.refresh()

    def on_settings_saved(self, message="Settings updated"):

        self.statusbar.set_text(message)
        self.topbar.refresh_user()

    def navigate(self, page_name):

        if page_name == "logout":
            self.logout()
            return

        if page_name == "profile":
            self.open_profile()
            return

        self.show_page(page_name)

    def open_profile(self):

        self.show_page("profile")

    def toggle_theme(self):

        self.current_theme = "light" if str(self.current_theme).lower() == "dark" else "dark"
        self.settings_repo.set("appearance", self.current_theme)
        apply_theme(self.current_theme)
        self.statusbar.set_text(f"Theme changed to {self.current_theme.title()}")
        self.destroy()

        from app.ui.main_window import MainWindow

        MainWindow().mainloop()

    def logout(self):

        Session.logout()
        self.destroy()

        from app.ui.auth.login_window import LoginWindow

        LoginWindow().mainloop()

    def close_app(self):

        Session.logout()
        self.destroy()


if __name__ == "__main__":

    app = MainWindow()
    app.mainloop()