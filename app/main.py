import customtkinter as ctk

from app.auth.session import Session
from app.ui.auth.login_window import LoginWindow
from app.ui.main_window import MainWindow

def configure_theme():

    ctk.set_appearance_mode("Dark")      
    ctk.set_default_color_theme("blue") 


def main():

    configure_theme()

    app = MainWindow() if Session.is_logged_in() else LoginWindow()

    app.mainloop()


if __name__ == "__main__":
    main()