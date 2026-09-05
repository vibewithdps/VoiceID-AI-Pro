from tkinter import messagebox


class Dialog:

    @staticmethod
    def info(title, message):
        messagebox.showinfo(title, message)

    @staticmethod
    def warning(title, message):
        messagebox.showwarning(title, message)

    @staticmethod
    def error(title, message):
        messagebox.showerror(title, message)

    @staticmethod
    def confirm(title, message):
        return messagebox.askyesno(title, message)