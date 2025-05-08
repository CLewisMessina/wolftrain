# ui/app_frame.py
import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Text, PhotoImage
from tkinterdnd2 import DND_FILES
from ttkbootstrap import Frame, Label, Button, Entry, Scrollbar
from ttkbootstrap.constants import *
from controller import (
    set_base_model,
    set_dataset,
    clear_base_model,
    clear_dataset,
    start_training
)

MAX_DATASET_SIZE_BYTES = 1 * 1024 * 1024 * 1024  # 1GB

class AppFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, padding=(20, 10))

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=750)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        self.icon = lambda name: PhotoImage(file=f"assets/icons/{name}")
        self.icons = {
            "model": self.icon("icon-model-select.png"),
            "clear": self.icon("icon-model-clear.png"),
            "dataset": self.icon("icon-dataset-select.png"),
            "dataset_clear": self.icon("icon-dataset-clear.png"),
            "train": self.icon("icon-train-start.png"),
            "clear_console": self.icon("icon-console-clear.png")
        }

        content = self.scrollable_frame

        # === Model Selection Section ===
        Label(content, text="Model Selection", font=("Arial", 16, "bold")).pack(anchor="w", padx=10)

        self.base_model_label = Label(content, text="📦 No base model selected", anchor="w")
        self.base_model_label.pack(fill=X, padx=10, pady=(0, 10))

        Button(content, image=self.icons["model"], text=" Select Model", compound="left",
               command=self.select_model, style="Hover.TButton").pack(fill=X, padx=10, pady=(0, 6))
        Button(content, image=self.icons["clear"], text=" Clear Model", compound="left",
               command=self.clear_model, style="Hover.TButton").pack(fill=X, padx=10, pady=(0, 16))

        # === Dataset Section ===
        Label(content, text="Dataset Upload", font=("Arial", 16, "bold")).pack(anchor="w", padx=10)

        self.dataset_label = Label(content, text="📁 No dataset selected", anchor="w")
        self.dataset_label.pack(fill=X, padx=10, pady=(0, 10))

        Button(content, image=self.icons["dataset"], text=" Select Dataset", compound="left",
               command=self.select_dataset, style="Hover.TButton").pack(fill=X, padx=10, pady=(0, 6))
        Button(content, image=self.icons["dataset_clear"], text=" Clear Dataset", compound="left",
               command=self.clear_dataset, style="Hover.TButton").pack(fill=X, padx=10, pady=(0, 16))

        # === Training Settings Section ===
        Label(content, text="Training Settings", font=("Arial", 16, "bold")).pack(anchor="w", padx=10)

        self.epochs_entry = self._create_labeled_entry(content, "Epochs:", "1")
        self.batch_size_entry = self._create_labeled_entry(content, "Batch Size:", "4")
        self.learning_rate_entry = self._create_labeled_entry(content, "Learning Rate:", "5e-4")

        Button(content, image=self.icons["train"], text=" Start Training", compound="left",
               command=self.start_training, style="Hover.TButton").pack(fill=X, padx=10, pady=(10, 16))

        self.progress_bar = tk.ttk.Progressbar(content, maximum=100)
        self.progress_bar.pack(fill=X, padx=10, pady=(0, 16))

        # === Console Section ===
        Label(content, text="Training Console", font=("Arial", 16, "bold")).pack(anchor="w", padx=10)

        Button(content, image=self.icons["clear_console"], text=" Clear Console", compound="left",
               command=self.clear_console, style="Hover.TButton").pack(fill=X, padx=10, pady=(0, 6))

        self.console_text = Text(content, wrap="word", height=20)
        self.console_text.pack(fill=BOTH, expand=YES, padx=10, pady=(0, 10))

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.handle_file_drop)

    def _create_labeled_entry(self, parent, label_text, default_value):
        frame = Frame(parent)
        frame.pack(fill=X, pady=4, padx=10)

        label = Label(frame, text=label_text, width=12, anchor="w")
        label.pack(side=LEFT)

        entry = Entry(frame)
        entry.insert(0, default_value)
        entry.pack(side=LEFT, fill=X, expand=YES)

        return entry

    def select_model(self):
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
            try:
                file_size = os.path.getsize(path)
                if file_size > MAX_DATASET_SIZE_BYTES:
                    raise ValueError("Dataset file too large (max 1GB).")
                if not path.endswith((".txt", ".csv")):
                    raise ValueError("Only .txt or .csv files are supported.")
                set_dataset(path)
                self.dataset_label.config(text=f"📁 {os.path.basename(path)}")
                self._write_console("✅ Dataset valid and ready!")
            except Exception as e:
                messagebox.showerror("Invalid Dataset", str(e))
                self._write_console(f"❌ Dataset validation failed: {str(e)}")

    def clear_dataset(self):
        clear_dataset()
        self.dataset_label.config(text="📁 No dataset selected")

    def handle_file_drop(self, event):
        path = event.data.strip("{}")
        if os.path.isfile(path) and path.lower().endswith((".txt", ".csv")):
            set_dataset(path)
            self.dataset_label.config(text=os.path.basename(path))
            self._write_console("✅ Dataset loaded via drag-and-drop")
        else:
            messagebox.showerror("Invalid File", "Please drop a valid .txt or .csv file.")

    def start_training(self):
        self.progress_bar['value'] = 0

        try:
            epochs = int(self.epochs_entry.get())
            batch_size = int(self.batch_size_entry.get())
            learning_rate = float(self.learning_rate_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Settings", "Please enter valid numbers for training settings.")
            return

        success, message = start_training(self._training_update, epochs, batch_size, learning_rate)
        if not success:
            self._write_console(message)
            messagebox.showerror("Error", message)

    def _training_update(self, text):
        self._write_console(text)

    def _write_console(self, text):
        self.console_text.config(state="normal")
        self.console_text.insert("end", text + "\n")
        self.console_text.see("end")
        self.console_text.config(state="disabled")

    def clear_console(self):
        self.console_text.config(state="normal")
        self.console_text.delete("1.0", "end")
        self.console_text.config(state="disabled")
