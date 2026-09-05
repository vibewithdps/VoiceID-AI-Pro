import tkinter as tk

import customtkinter as ctk

from app.ui.theme import SURFACE, SURFACE_ALT


class MiniBarChart(ctk.CTkFrame):

    def __init__(self, master, title, values, labels=None):
        super().__init__(master, fg_color=SURFACE, corner_radius=18)

        self.values = values
        self.labels = labels or [str(index + 1) for index in range(len(values))]

        ctk.CTkLabel(self, text=title, font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=18, pady=(16, 8))

        self.canvas = tk.Canvas(self, height=180, highlightthickness=0, bg=SURFACE_ALT)
        self.canvas.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.bind("<Configure>", lambda _event: self.draw())
        self.draw()

    def draw(self):
        self.canvas.delete("all")

        if not self.values:
            self.canvas.create_text(220, 90, text="No data available", fill="#9CA3AF", font=("Segoe UI", 13))
            return

        width = max(self.canvas.winfo_width(), 400)
        height = max(self.canvas.winfo_height(), 180)
        margin = 26
        bar_area = width - margin * 2
        bar_width = bar_area / len(self.values)
        peak = max(self.values) if max(self.values) else 1

        for index, value in enumerate(self.values):
            x1 = margin + index * bar_width + 12
            x2 = x1 + max(bar_width - 24, 14)
            bar_height = (height - 60) * (value / peak)
            y1 = height - 26 - bar_height
            y2 = height - 26

            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#4EA5FF", outline="")
            self.canvas.create_text((x1 + x2) / 2, height - 14, text=self.labels[index], fill="#9CA3AF", font=("Segoe UI", 11))