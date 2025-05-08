# main.py
from tkinterdnd2 import TkinterDnD
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from ui.app_frame import AppFrame
from ui.styles import apply_hover_style, apply_radio_styles  # Added radio styles

def main():
    root = TkinterDnD.Tk()
    style = ttkb.Style(theme="simplex")

    # Apply both hover button and radio button styles
    apply_hover_style(style)
    apply_radio_styles(style)

    style.master = root  # Link theme to the main root

    root.title("Wolftrain")
    root.geometry("800x600")
    root.minsize(600, 400)

    try:
        root.iconphoto(False, tk.PhotoImage(file="assets/wolftrain-icon.png"))
    except:
        pass  # Fallback silently if icon is missing

    frame = AppFrame(root)
    frame.pack(fill=BOTH, expand=YES)

    root.mainloop()

if __name__ == "__main__":
    main()
