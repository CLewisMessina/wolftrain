# main.py
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ui.app_frame import AppFrame
import tkinter as tk  # <-- Added to handle the app icon

def main():
    app = ttkb.Window(themename="simplex")  # or "flatly", "minty", etc.
    app.title("Wolftrain")
    app.geometry("800x600")
    app.minsize(600, 400)
    
    # Set custom wolfkit app icon
    app.iconphoto(False, tk.PhotoImage(file="assets/wolftrain-icon.png"))

    frame = AppFrame(app)
    frame.pack(fill=BOTH, expand=YES)

    app.mainloop()

if __name__ == "__main__":
    main()
