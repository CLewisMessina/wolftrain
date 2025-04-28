# ui/app_frame.py
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from ttkbootstrap import Frame, Label, Button, Text, Progressbar, Scrollbar
from ttkbootstrap.constants import *
from controller import (
    set_base_model,
    set_dataset,
    clear_base_model,
    clear_dataset,
    start_training
)

class AppFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)

        self.base_model_path = None
        self.dataset_path = None

        self.base_model_label = Label(self, text="📦 No base model selected", anchor="w")
        self.base_model_label.pack(fill=X, pady=(0, 10))

        self.dataset_label = Label(self, text="📁 No dataset selected", anchor="w")
        self.dataset_label.pack(fill=X, pady=(0, 10))

        # Model and dataset selection buttons
        select_frame = Frame(self)
        select_frame.pack(fill=X, pady=(0, 10))

        self.select_model_btn = Button(select_frame, text="Select Model", command=self.select_model)
        self.select_model_btn.pack(side=LEFT, padx=(0, 5))

        self.clear_model_btn = Button(select_frame, text="Clear", command=self.clear_model)
        self.clear_model_btn.pack(side=LEFT, padx=(0, 10))

        self.select_dataset_btn = Button(select_frame, text="Select Dataset", command=self.select_dataset)
        self.select_dataset_btn.pack(side=LEFT, padx=(0, 5))

        self.clear_dataset_btn = Button(select_frame, text="Clear", command=self.clear_dataset)
        self.clear_dataset_btn.pack(side=LEFT)

        # Start training button
        self.train_btn = Button(self, text="🚀 Start Training", bootstyle="primary", command=self.start_training)
        self.train_btn.pack(fill=X, pady=(10, 10))

        # Progress bar
        self.progress_bar = Progressbar(self, bootstyle="info-striped", maximum=100)
        self.progress_bar.pack(fill=X, pady=(0, 10))

        # Console output
        console_label = Label(self, text="📈 Training Console:")
        console_label.pack(anchor="w")

        console_frame = Frame(self)
        console_frame.pack(fill=BOTH, expand=YES)

        self.console_text = Text(console_frame, wrap="word", height=20)
        self.console_text.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = Scrollbar(console_frame, command=self.console_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.console_text.config(yscrollcommand=scrollbar.set)

    # def select_model(self):
        # path = filedialog.askopenfilename(title="Select Base Model")
        # if path:
            # set_base_model(path)
            # self.base_model_label.config(text=f"📦 {os.path.basename(path)}")

    def select_model(self):
        # Instead of file dialog, simple text entry popup
        model_name = tk.simpledialog.askstring("Select Base Model", "Enter Hugging Face model name (e.g., sshleifer/tiny-gpt2):")
        if model_name:
            set_base_model(model_name)
            self.base_model_label.config(text=f"📦 {model_name}")



    def clear_model(self):
        clear_base_model()
        self.base_model_label.config(text="📦 No base model selected")

    def select_dataset(self):
        path = filedialog.askopenfilename(title="Select Dataset")
        if path:
            set_dataset(path)
            self.dataset_label.config(text=f"📁 {os.path.basename(path)}")

    def clear_dataset(self):
        clear_dataset()
        self.dataset_label.config(text="📁 No dataset selected")

    def start_training(self):
        self.progress_bar['value'] = 0
        success, message = start_training(self._training_update)
        if not success:
            self._write_console(message)
            messagebox.showerror("Error", message)

    def _training_update(self, text):
        self._write_console(text)
        if "Step" in text:
            try:
                parts = text.split()
                current_step, total_steps = map(int, parts[2].split("/"))
                percent = (current_step / total_steps) * 100
                self.progress_bar['value'] = percent
            except:
                pass

    def _write_console(self, text):
        self.console_text.config(state="normal")
        self.console_text.insert("end", text + "\n")
        self.console_text.see("end")
        self.console_text.config(state="disabled")
