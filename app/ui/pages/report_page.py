import csv
import os
from pathlib import Path
from tkinter import messagebox
from datetime import datetime

import customtkinter as ctk

from app.database.database import Database
from app.database.history_repository import HistoryRepository
from app.database.user_repository import UserRepository
from app.ui.components.dialog import Dialog
from app.ui.theme import BODY_FONT, MUTED_TEXT, SURFACE, SUBTITLE_FONT

class ReportPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.db = Database()
        self.history = HistoryRepository(self.db)
        self.users = UserRepository(self.db)
        
        # Ensure exports directory exists
        self.exports_dir = Path("exports")
        self.exports_dir.mkdir(exist_ok=True)

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        ctk.CTkLabel(self, text="📊 System Reports", font=("Segoe UI", 30, "bold")).pack(anchor="w", pady=(0, 6))
        ctk.CTkLabel(self, text="Generate and export system usage, models, and prediction metrics.", font=BODY_FONT, text_color=MUTED_TEXT).pack(anchor="w", pady=(0, 18))

        top_cards = ctk.CTkFrame(self, fg_color="transparent")
        top_cards.pack(fill="x", pady=(0, 14))
        
        self.stats_frame = ctk.CTkFrame(top_cards, corner_radius=18, fg_color=SURFACE)
        self.stats_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        ctk.CTkLabel(self.stats_frame, text="System Summary", font=SUBTITLE_FONT).pack(anchor="w", padx=18, pady=(16, 10))
        self.summary_text = ctk.CTkTextbox(self.stats_frame, height=180, fg_color="transparent")
        self.summary_text.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        actions_frame = ctk.CTkFrame(top_cards, corner_radius=18, fg_color=SURFACE)
        actions_frame.pack(side="left", fill="both", expand=True, padx=(8, 0))
        
        ctk.CTkLabel(actions_frame, text="Export Actions", font=SUBTITLE_FONT).pack(anchor="w", padx=18, pady=(16, 10))
        ctk.CTkButton(actions_frame, text="📥 Export Predictions (CSV)", height=40, command=self.export_predictions).pack(fill="x", padx=18, pady=(10, 5))
        ctk.CTkButton(actions_frame, text="📥 Export Models (CSV)", height=40, command=self.export_models).pack(fill="x", padx=18, pady=5)
        ctk.CTkButton(actions_frame, text="📥 Export Users (CSV)", height=40, command=self.export_users).pack(fill="x", padx=18, pady=5)

    def refresh(self):
        self.summary_text.configure(state="normal")
        self.summary_text.delete("1.0", "end")
        
        users_count = len(self.users.get_all_users())
        models = self.history.list_trained_models()
        predictions = self.history.list_prediction_history()
        
        avg_conf = sum(p['confidence'] for p in predictions if p.get('confidence')) / len(predictions) if predictions else 0.0
        
        summary = (
            f"• Total Registered Users: {users_count}\n"
            f"• Total Models Trained: {len(models)}\n"
            f"• Total Predictions Made: {len(predictions)}\n"
            f"• Average Confidence: {avg_conf:.2f}%\n"
        )
        if models:
            summary += f"• Best Model Accuracy: {models[0]['accuracy']:.1f}%\n"
            
        self.summary_text.insert("end", summary)
        self.summary_text.configure(state="disabled")

    def export_predictions(self):
        data = self.history.list_prediction_history()
        if not data:
            Dialog.info("Export", "No prediction data to export.")
            return
            
        filepath = self.exports_dir / f"predictions_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "User ID", "File Name", "Predicted Speaker", "Confidence", "Time"])
                for row in data:
                    writer.writerow([row['id'], row['user_id'], row['file_name'], row['predicted_speaker'], f"{row['confidence']:.2f}%", row['prediction_time']])
            Dialog.info("Export Success", f"Predictions exported to:\n{filepath}")
        except Exception as e:
            Dialog.error("Export Failed", str(e))

    def export_models(self):
        data = self.history.list_trained_models()
        if not data:
            Dialog.info("Export", "No models data to export.")
            return
            
        filepath = self.exports_dir / f"models_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Algorithm", "Accuracy", "Model Path", "Time"])
                for row in data:
                    writer.writerow([row['id'], row['algorithm'], f"{row['accuracy']:.2f}%" if row['accuracy'] else "N/A", row['model_path'], row['trained_at']])
            Dialog.info("Export Success", f"Models exported to:\n{filepath}")
        except Exception as e:
            Dialog.error("Export Failed", str(e))

    def export_users(self):
        data = self.users.get_all_users()
        if not data:
            Dialog.info("Export", "No users to export.")
            return
            
        filepath = self.exports_dir / f"users_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Username", "Full Name", "Email", "Role", "Created At"])
                for row in data:
                    writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])
            Dialog.info("Export Success", f"Users exported to:\n{filepath}")
        except Exception as e:
            Dialog.error("Export Failed", str(e))

