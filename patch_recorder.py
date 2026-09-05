import re

with open("app/ui/pages/recorder_page.py", "r") as f:
    content = f.read()

# Add Predictor import
content = content.replace("from app.auth.session import Session", "from app.auth.session import Session\nfrom app.ml.predictor import SpeakerPredictor\nimport tkinter as tk")

# Add Predictor init
content = content.replace("self.speaker_lookup = {}", "self.speaker_lookup = {}\n        self.predictor = SpeakerPredictor()")

# Replace Waveform placeholder
waveform_placeholder = """        waveform = ctk.CTkFrame(self, height=120, corner_radius=15)
        waveform.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(
            waveform,
            text="📊 Audio Waveform\\n(Coming Soon)",
            font=("Segoe UI", 18)
        ).pack(expand=True)"""

waveform_new = """        self.waveform_frame = ctk.CTkFrame(self, height=120, corner_radius=15)
        self.waveform_frame.pack(fill="x", padx=30, pady=20)

        self.canvas = tk.Canvas(self.waveform_frame, height=120, highlightthickness=0, bg="#1E1E1E")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.create_text(300, 50, text="📊 Ready to Record", fill="#666666", font=("Segoe UI", 14))"""

content = content.replace(waveform_placeholder, waveform_new)

# Add Predict button
buttons_placeholder = """        self.delete_btn = ctk.CTkButton(buttons, text="🗑 Delete", width=140, state="disabled", command=self.delete_recording)
        self.delete_btn.grid(row=0, column=3, padx=10)"""

buttons_new = """        self.delete_btn = ctk.CTkButton(buttons, text="🗑 Delete", width=140, state="disabled", command=self.delete_recording)
        self.delete_btn.grid(row=0, column=3, padx=10)
        
        self.predict_btn = ctk.CTkButton(buttons, text="🎯 Predict", width=140, state="disabled", command=self.predict_recording, fg_color="#27ae60", hover_color="#219653")
        self.predict_btn.grid(row=0, column=4, padx=10)"""

content = content.replace(buttons_placeholder, buttons_new)

# Add Waveform draw and prediction logic
methods_new = """
    def draw_waveform(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 1:
            width = 600
        
        envelope = self.recorder.waveform(width=width)
        if not envelope:
            self.canvas.create_text(width//2, height//2, text="No Audio Data", fill="#666666", font=("Segoe UI", 14))
            return
            
        peak = max(envelope) if max(envelope) > 0 else 1.0
        
        for x, val in enumerate(envelope):
            bar_height = (val / peak) * (height - 10)
            y1 = (height - bar_height) / 2
            y2 = (height + bar_height) / 2
            self.canvas.create_line(x, y1, x, y2, fill="#4EA5FF", width=1)

    def predict_recording(self):
        if not self.filepath or not os.path.exists(self.filepath):
            messagebox.showwarning("No File", "Please record audio first.")
            return
            
        try:
            result = self.predictor.predict(self.filepath)
            messagebox.showinfo("Prediction Result", f"Speaker: {result.speaker}\\nConfidence: {result.confidence:.2f}%")
        except Exception as exc:
            messagebox.showerror("Prediction Failed", str(exc))
"""

content = content.replace("    def stop_recording(self):", methods_new + "\n    def stop_recording(self):")

# Update recording_finished to draw waveform and enable predict
rec_fin_old = """        self.play_btn.configure(state="normal" if self.filepath else "disabled")
        self.delete_btn.configure(state="normal" if self.filepath else "disabled")

        if self.filepath:"""
        
rec_fin_new = """        self.play_btn.configure(state="normal" if self.filepath else "disabled")
        self.delete_btn.configure(state="normal" if self.filepath else "disabled")
        self.predict_btn.configure(state="normal" if self.filepath else "disabled")

        if self.filepath:
            self.draw_waveform()"""

content = content.replace(rec_fin_old, rec_fin_new)

# Update reset_ui and delete
reset_old = """        self.play_btn.configure(state="normal" if self.filepath else "disabled")
        self.delete_btn.configure(state="normal" if self.filepath else "disabled")"""

reset_new = """        self.play_btn.configure(state="normal" if self.filepath else "disabled")
        self.delete_btn.configure(state="normal" if self.filepath else "disabled")
        self.predict_btn.configure(state="normal" if self.filepath else "disabled")"""
        
content = content.replace(reset_old, reset_new)

del_old = """            self.play_btn.configure(state="disabled")
            self.delete_btn.configure(state="disabled")"""

del_new = """            self.play_btn.configure(state="disabled")
            self.delete_btn.configure(state="disabled")
            self.predict_btn.configure(state="disabled")
            self.canvas.delete("all")
            self.canvas.create_text(300, 50, text="📊 Ready to Record", fill="#666666", font=("Segoe UI", 14))"""
            
content = content.replace(del_old, del_new)

with open("app/ui/pages/recorder_page.py", "w") as f:
    f.write(content)
