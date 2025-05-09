# ui/widgets/preset_radio_group.py
import tkinter as tk
from ttkbootstrap import Frame, Radiobutton
from ttkbootstrap.constants import *

class PresetRadioGroup(Frame):
    def __init__(self, parent, target_entry, icons, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.var = tk.StringVar()
        self.target_entry = target_entry

        self.presets = {
            "5e-3 — Risky Fast": ("5e-3", "Red.TRadiobutton", icons["lr_risky"]),
            "1e-3 — Faster Tuning": ("1e-3", "Orange.TRadiobutton", icons["lr_fast"]),
            "5e-4 — Safe Default": ("5e-4", "Green.TRadiobutton", icons["lr_safe"]),
            "1e-4 — Very Careful": ("1e-4", "Blue.TRadiobutton", icons["lr_careful"]),
            "5e-5 — Very Low": ("5e-5", "Indigo.TRadiobutton", icons["lr_low"]),
            "1e-5 — Nano Steps": ("1e-5", "Violet.TRadiobutton", icons["lr_nano"])
        }

        self._build_presets()

    def _build_presets(self):
        for label, (value, style, icon) in self.presets.items():
            rb = Radiobutton(
                self,
                text=label,
                variable=self.var,
                value=value,
                style=style,
                image=icon,
                compound="left",
                command=lambda v=value: self._update_target(v)
            )
            rb.pack(anchor="w", padx=10, pady=0)

    def _update_target(self, value):
        self.target_entry.delete(0, "end")
        self.target_entry.insert(0, value)
