# main.py
from tkinterdnd2 import TkinterDnD  # New import
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from ui.app_frame import AppFrame
from ui.styles import apply_hover_style

def main():
    # Use TkinterDnD-capable root window
    root = TkinterDnD.Tk()
    style = ttkb.Style(theme="simplex")
    apply_hover_style(style)
    style.master = root  # Link ttkbootstrap theme to the root window

    root.title("Wolftrain")
    root.geometry("800x600")
    root.minsize(600, 400)

    try:
        root.iconphoto(False, tk.PhotoImage(file="assets/wolftrain-icon.png"))
    except:
        pass  # fallback silently if no icon found

    frame = AppFrame(root)
    frame.pack(fill=BOTH, expand=YES)

    root.mainloop()

if __name__ == "__main__":
    main()
