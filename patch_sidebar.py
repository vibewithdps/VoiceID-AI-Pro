with open("app/ui/components/sidebar.py", "r") as f:
    content = f.read()

# Add a spacer and developer details at the bottom of the sidebar
developer_footer = """
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(fill="y", expand=True)

        dev_frame = ctk.CTkFrame(self, fg_color="transparent")
        dev_frame.pack(side="bottom", fill="x", padx=18, pady=20)
        
        ctk.CTkLabel(dev_frame, text="Developed by", font=("Segoe UI", 10), text_color=MUTED_TEXT).pack(anchor="w")
        ctk.CTkLabel(dev_frame, text="Dipendra Pratap Singh", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ctk.CTkLabel(dev_frame, text="github.com/vibewithdps", font=("Segoe UI", 10)).pack(anchor="w")
"""

content = content + developer_footer

with open("app/ui/components/sidebar.py", "w") as f:
    f.write(content)
