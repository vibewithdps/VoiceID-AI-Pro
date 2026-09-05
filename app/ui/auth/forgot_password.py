import customtkinter as ctk
from tkinter import messagebox

from app.auth.auth_manager import AuthManager


class ForgotPasswordWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.auth = AuthManager()

        self.title("VoiceID AI Pro - Reset Password")
        self.geometry("500x620")
        self.resizable(False, False)

        self.build_ui()

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="🎤 VoiceID AI Pro",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(40, 10))

        ctk.CTkLabel(
            self,
            text="Reset your password",
            font=("Segoe UI", 18)
        ).pack(pady=(0, 25))

        self.email = ctk.CTkEntry(
            self,
            width=360,
            placeholder_text="Email"
        )
        self.email.pack(pady=8)

        self.new_password = ctk.CTkEntry(
            self,
            width=360,
            placeholder_text="New Password",
            show="*"
        )
        self.new_password.pack(pady=8)

        self.confirm_password = ctk.CTkEntry(
            self,
            width=360,
            placeholder_text="Confirm New Password",
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
            text="Update Password",
            width=360,
            height=45,
            command=self.reset_password
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Back to Login",
            fg_color="transparent",
            hover=False,
            text_color="#4EA5FF",
            command=self.back_to_login
        ).pack()

    def toggle_password(self):

        show_value = "" if self.show_password.get() else "*"
        self.new_password.configure(show=show_value)
        self.confirm_password.configure(show=show_value)

    def reset_password(self):

        status, message = self.auth.reset_password(
            self.email.get(),
            self.new_password.get(),
            self.confirm_password.get(),
        )

        if status:
            messagebox.showinfo("Success", message)
            self.back_to_login()
        else:
            messagebox.showerror("Reset Failed", message)

    def back_to_login(self):

        self.destroy()

        from app.ui.auth.login_window import LoginWindow

        LoginWindow().mainloop()


if __name__ == "__main__":

    ForgotPasswordWindow().mainloop()