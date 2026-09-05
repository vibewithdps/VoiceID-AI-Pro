import customtkinter as ctk
from tkinter import messagebox

from app.auth.auth_manager import AuthManager
from app.auth.session import Session


class LoginWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.auth = AuthManager()

        self.title("VoiceID AI Pro - Login")
        self.geometry("500x600")
        self.resizable(False, False)

        self.build_ui()

    # ======================================================

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="🎤 VoiceID AI Pro",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(40, 10))

        ctk.CTkLabel(
            self,
            text="Login to your account",
            font=("Segoe UI", 18)
        ).pack(pady=(0, 30))

        self.email = ctk.CTkEntry(
            self,
            width=360,
            placeholder_text="Email"
        )
        self.email.pack(pady=10)

        self.password = ctk.CTkEntry(
            self,
            width=360,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        self.show_password = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(
            self,
            text="Show Password",
            variable=self.show_password,
            command=self.toggle_password
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Login",
            width=360,
            height=45,
            command=self.login
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Create New Account",
            fg_color="transparent",
            hover=False,
            text_color="#4EA5FF",
            command=self.open_signup
        ).pack()

        ctk.CTkButton(
            self,
            text="Forgot Password?",
            fg_color="transparent",
            hover=False,
            text_color="#A0A0A0",
            command=self.open_forgot_password
        ).pack(pady=(8, 0))

    # ======================================================

    def toggle_password(self):

        if self.show_password.get():
            self.password.configure(show="")
        else:
            self.password.configure(show="*")

    # ======================================================

    def login(self):

        status, result = self.auth.login(
            self.email.get(),
            self.password.get()
        )

        if not status:
            messagebox.showerror(
                "Login Failed",
                result
            )
            return

        Session.login(result)

        self.destroy()

        from app.ui.main_window import MainWindow

        app = MainWindow()
        app.mainloop()

    # ======================================================

    def open_signup(self):

        self.destroy()

        from app.ui.auth.signup_window import SignupWindow

        SignupWindow().mainloop()

    def open_forgot_password(self):

        self.destroy()

        from app.ui.auth.forgot_password import ForgotPasswordWindow

        ForgotPasswordWindow().mainloop()


if __name__ == "__main__":

    LoginWindow().mainloop()