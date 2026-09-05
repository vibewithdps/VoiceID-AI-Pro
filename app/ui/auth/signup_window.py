import customtkinter as ctk
from tkinter import messagebox

from app.auth.auth_manager import AuthManager


class SignupWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.auth = AuthManager()

        self.title("VoiceID AI Pro - Sign Up")
        self.geometry("500x700")
        self.resizable(False, False)

        self.build_ui()

    # ======================================================

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="🎤 VoiceID AI Pro",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            self,
            text="Create New Account",
            font=("Segoe UI", 18)
        ).pack(pady=(0, 20))

        self.full_name = ctk.CTkEntry(
            self,
            width=360,
            placeholder_text="Full Name"
        )
        self.full_name.pack(pady=8)

        self.username = ctk.CTkEntry(
            self,
            width=360,
            placeholder_text="Username"
        )
        self.username.pack(pady=8)

        self.email = ctk.CTkEntry(
            self,
            width=360,
            placeholder_text="Email"
        )
        self.email.pack(pady=8)

        self.password = ctk.CTkEntry(
            self,
            width=360,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=8)

        self.confirm_password = ctk.CTkEntry(
            self,
            width=360,
            placeholder_text="Confirm Password",
            show="*"
        )
        self.confirm_password.pack(pady=8)

        self.show_password = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(
            self,
            text="Show Password",
            variable=self.show_password,
            command=self.toggle_password
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Create Account",
            width=360,
            height=45,
            command=self.signup
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Already have an account? Login",
            fg_color="transparent",
            hover=False,
            text_color="#4EA5FF",
            command=self.back_to_login
        ).pack()

    # ======================================================

    def toggle_password(self):

        if self.show_password.get():
            self.password.configure(show="")
            self.confirm_password.configure(show="")
        else:
            self.password.configure(show="*")
            self.confirm_password.configure(show="*")

    # ======================================================

    def signup(self):

        status, message = self.auth.register(

            self.full_name.get(),

            self.username.get(),

            self.email.get(),

            self.password.get(),

            self.confirm_password.get()

        )

        if status:

            messagebox.showinfo(
                "Success",
                message
            )

            self.back_to_login()

        else:

            messagebox.showerror(
                "Registration Failed",
                message
            )

    # ======================================================

    def back_to_login(self):

        self.destroy()

        from app.ui.auth.login_window import LoginWindow

        LoginWindow().mainloop()


if __name__ == "__main__":

    SignupWindow().mainloop()