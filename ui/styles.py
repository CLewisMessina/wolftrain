# ui/styles.py
from ttkbootstrap import Style

def apply_hover_style(style: Style):
    style.configure("Hover.TButton",
        font=("Arial", 10),
        background="#f7f7f7",
        foreground="#222",
        borderwidth=1,
        relief="flat"
    )
    style.map("Hover.TButton",
        background=[("active", "#b91c1c")],  # Deep red
        foreground=[("active", "#ffffff")]
    )

def apply_radio_styles(style: Style):
    style.configure("Red.TRadiobutton", foreground="#dc2626")      # 🔥 High
    style.configure("Orange.TRadiobutton", foreground="#ea580c")   # ⚡ Medium
    style.configure("Green.TRadiobutton", foreground="#16a34a")    # ✅ Safe Default
    style.configure("Blue.TRadiobutton", foreground="#0ea5e9")     # 🧘 Very Careful
    style.configure("Indigo.TRadiobutton", foreground="#6366f1")   # 🐢 Very Low
    style.configure("Violet.TRadiobutton", foreground="#9333ea")   # 🧊 Nano Steps
