import customtkinter as ctk

class ReportPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(
            self,
            text="📊 Reports",
            font=("Segoe UI",28,"bold")
        ).pack(pady=30)